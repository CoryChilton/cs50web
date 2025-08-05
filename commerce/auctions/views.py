from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .choices import CATEGORIES
from .models import Listing


from .models import User


def index(request):
    listings = Listing.objects.all()
    print(listings)
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
                        bid_price_cents=float(request.POST['starting_bid']) * 100, 
                        image_url=request.POST['image_url'], 
                        category=request.POST['category'])
            l.save()
            return HttpResponseRedirect(reverse('listing', kwargs={"listing_id": l.pk}))
    else:
        form = ListingForm()
        return render(request, "auctions/new_listing.html", {
            'form': form
        })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "price": float(listing.bid_price_cents) / 100
    })
