from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from datetime import datetime

from .models import Bid, Category, Comment, Item, Post, User
from .forms import AddForm, BidForm, CommentForm


def index(request):
    posts = Post.objects.filter(winner__isnull=True)
    return render(request, "auctions/index.html", {
        "current_page": "index",
        "posts": posts,
        "header": "Active Listings",
    })


@login_required
def add_bid(request, post_id):
    if request.method == "POST":
        # Create a bid object from form submission.
        target = Post.objects.get(pk=post_id)
        new_bid = BidForm(request.POST, instance=Bid(
            bidder=request.user,
            bid_datetime=datetime.now(),
            post=target,
        ))

        # Catch errors and send message back to view.post
        try:
            new_bid.save()
            messages.success(request, "Bid submitted successfully!")
        except Exception as e:
            messages.warning(request, f"Failed to submit bid. Error: {e}")

    # Redirect back to view.post
    return HttpResponseRedirect(reverse("post", kwargs={"post_id": post_id,}))


@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        # Create a comment object from form submission
        target = Post.objects.get(pk=post_id)
        new_comment = CommentForm(request.POST, instance=Comment(
            user=request.user,
            comment_datetime=datetime.now(),
            posting=target,
        ))

        # Catch errors and send message back to view.post in case of an error
        try:
            new_comment.save()
        except Exception as e:
            messages.warning(request, f"Failed to submit comment. Error: {e}")

    #Redirect back to view.post
    return HttpResponseRedirect(reverse("post", kwargs={"post_id": post_id,}))


@login_required
@transaction.atomic
def add_view(request):
    if request.method == "POST":
        form = AddForm(request.POST)

        # Handle Invalid form answers
        if not form.is_valid():
            return render(request, "auctions/add.html", {
                "form": form,
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
            post_datetime=datetime.now()
        )

        try:
            with transaction.atomic():
                new_item.save()
                # Item needs to have an id before .set() can be used
                new_item.categories.set(cform["item_categories"])
                new_post.save()
        except Exception as e:
            messages.warning(request, f"Failed to save posting. Error: {e}")
            return HttpResponseRedirect(reverse("add"))

        return HttpResponseRedirect(reverse("post", kwargs={"post_id": new_post.id,}))

    # If request method is GET
    else:
        return render(request, "auctions/add.html", {
            "form": AddForm(),
            "current_page": "add",
            "message": messages.get_messages(request),
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
        return render(request, "auctions/login.html", {
            "current_page": "login",
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def post(request, post_id):
    if request.method == "POST":
        target_post = Post.objects.get(id=post_id)
        if not target_post.winner and request.user.is_authenticated and request.user == target_post.seller:
            winning = Bid.objects.filter(post=target_post).order_by('-bid_datetime').first()
            target_post.winner = winning.bidder
            target_post.save()
            return HttpResponseRedirect(reverse("post", kwargs={"post_id": post_id,}))

        else:
            return HttpResponseRedirect(reverse("post", kwargs={"post_id": post_id,}))
    
    else:
        # If request.method is GET
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
            "current_page": "post",
            "messages": messages.get_messages(request),
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
        return render(request, "auctions/register.html", {
            "current_page": "register",
        })


def view_all(request, category):
    if category == "all":
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(item__categories__cat_name=category)
    
    return render(request, "auctions/index.html", {
        "posts": posts,
        "header": category.capitalize(),
        "current_page": category
    })