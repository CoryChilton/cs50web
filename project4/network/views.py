from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post

class PostForm(forms.Form):
    content = forms.CharField(label='Content', widget=forms.Textarea, required=True)


def index(request, page=1):
    post_form = PostForm()
    posts = Post.objects.all().order_by('-created_timestamp')
    posts_paginated = Paginator(posts, 2)
    page_nums = range(1, posts_paginated.num_pages + 1)
    page = int(page)
    return render(request, "network/index.html", {
        'post_form': post_form,
        'posts': posts_paginated.page(page).object_list,
        'page_nums': page_nums,
        'next_page': page + 1 if page + 1 <= posts_paginated.num_pages else posts_paginated.num_pages,
        'prev_page': page - 1 if page - 1 > 0 else 1,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            p = Post(
                user=request.user,
                content=request.POST['content'],
            )
            p.save()
            return redirect('index')
    else:
        return redirect('index')


def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    num_followers = profile_user.followers.count()
    num_following = profile_user.following.count()
    posts = Post.objects.filter(user=user_id).order_by('-created_timestamp')
    currently_following = False
    if profile_user in request.user.following.all():
        currently_following = True
    return render(request, 'network/profile.html', {
        'profile_user': profile_user,
        'num_followers': num_followers,
        'num_following': num_following,
        'posts': posts,
        'currently_following': currently_following,
    })


@csrf_exempt
@login_required
def follow(request, user_id):
    if request.method == "POST":
        followee = User.objects.get(pk=user_id)
        request.user.following.add(followee)
        data = {"status": "ok", "message": "Successfully followed!"}
        return JsonResponse(data)
    
    

@csrf_exempt
@login_required
def unfollow(request, user_id):
    if request.method == "POST":
        followee = User.objects.get(pk=user_id)
        if followee in request.user.following.all():
            request.user.following.remove(followee)
            data = {"status": "ok", "message": "Successfully unfollowed!"}
            return JsonResponse(data)

        data = {"status": "bad", "message": "Not following this user already."}
        return JsonResponse(data)


@login_required
def following(request):
    followed_users = request.user.following.all()
    posts = Post.objects.filter(user__in=followed_users).order_by('-created_timestamp')
    return render(request, "network/index.html", {
        'posts': posts
    })
    
