from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Category, Comment, Item, Post, User
from .forms import AddForm, BidForm, CommentForm


def index(request):
    posts = Post.objects.all()
    return render(request, "auctions/index.html", {
        "posts": posts,
    })

@login_required
def add_view(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if not form.is_valid():
            # If form answers are invalid
            return render(request, "users/login.html", {
                "form": AddForm(),
            })
        
        cform = form.cleaned_data

        # Assign data to instance of Item
        new_item = Item(
            name=cform["item_name"],
            description=cform["item_description"],
            img_url=cform["item_img"],
        )

        # Assign data to instance of Post
        new_post = Post(
            item=new_item,
            seller=request.user,
            initial_p=cform["initial_bid"],
        )

        new_item.save()
        # Item needs to have an id before .set() can be used
        new_item.categories.set(cform["item_categories"])
        new_post.save()

        return HttpResponseRedirect(reverse("index"))

    # If request method is GET
    else:
        return render(request, "auctions/add.html", {
            "form": AddForm(),
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

def post(request, post_id):
    post = Post.objects.get(id=post_id)
    # "-fieldname" is used instead of .reverse() because .reverse() fetches the query list then reverses it.
    bids = Bid.objects.filter(post__id=post_id).order_by("-bid_datetime")
    comments = Comment.objects.filter(posting__id=post_id).order_by("-comment_datetime")
    
    return render(request, "auctions/post.html", {
        "post": post,
        "bids": bids,
        "bidform": BidForm(),
        "commentform": CommentForm(),
        "comments": comments,
    })

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
