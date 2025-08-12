from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .choices import CATEGORIES
from .models import Listing, Bid, Comment


from .models import User


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class ListingForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255)
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False)
    starting_bid = forms.DecimalField(label='Starting Bid ($)', decimal_places=2)
    image_url = forms.URLField(label='Image URL', required=False)
    category = forms.ChoiceField(label='category', required=False, choices=CATEGORIES)
    
@login_required
def new_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            l = Listing(title=request.POST['title'], 
                        description=request.POST['description'], 
                        bid_price=request.POST['starting_bid'], 
                        image_url=request.POST['image_url'], 
                        category=request.POST['category'],
                        creator=request.user)
            l.save()
            return HttpResponseRedirect(reverse('listing', kwargs={"listing_id": l.pk}))
    else:
        form = ListingForm()
        return render(request, "auctions/new_listing.html", {
            'form': form
        })

class BidForm(forms.Form):
    bid_price = forms.DecimalField(label='Bid ($)', decimal_places=2)

class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment', widget=forms.Textarea)

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        request.user.listings.add(listing)
        return HttpResponseRedirect(reverse('watchlist'))
    # else:  
    bid_form = BidForm()
    comment_form = CommentForm()
    winning_bid = Bid.objects.filter(listing=listing.pk).order_by("-timestamp").first()
    is_winner = winning_bid and winning_bid.user == request.user
    comments = Comment.objects.filter(listing=listing)
    
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_form": bid_form,
            "comment_form": comment_form,
            "is_winner": is_winner,
            "comments": comments
        })

@login_required
def comment(request, listing_id):
    l = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = Comment(comment=form.cleaned_data['comment'],
                        writer=request.user,
                        listing=l)
            c.save()
        return redirect('listing', listing_id=l.pk)

@login_required
def close_listing(request, listing_id):
    l = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        l.active = False
        l.save()
        return redirect('listing', listing_id=l.pk)

@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['bid_price'] <= listing.bid_price:
                return render(request, "auctions/error.html", {
                    'error_message': 'Your bid must be greater than the current bid'
                })
            
            b = Bid(listing=listing, 
                    user=request.user, 
                    bid_price=form.cleaned_data['bid_price'])
            b.save()
            listing.bid_price = form.cleaned_data['bid_price']
            listing.save()
            return redirect('listing', listing_id=listing.pk)
    

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.listings.all()
    })

@login_required
def delete_from_watchlist(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        request.user.listings.remove(listing)
        return HttpResponseRedirect(reverse('watchlist'))

class CategoryForm(forms.Form):
    category = forms.ChoiceField(label='Category', required=False, choices=CATEGORIES)

def categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            return redirect('category', category=category)
    else:
        category_form = CategoryForm()
        return render(request, 'auctions/categories.html', {
            "category_form": category_form,
        })

def category(request, category):
    listings = Listing.objects.filter(category=category)
    for c_short, c_readable in CATEGORIES:
        if c_short == category:
            category_readable = c_readable
    return render(request, 'auctions/category.html', {
        'category': category,
        'listings': listings,
        'category_readable': category_readable,
    })
