from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from django.contrib import messages

from .models import User, Listing, Comment, Category

def index(request):
    
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isActive=True),
        "title": "Active Listings"
    }
)  

def listing(request, id):
    listing = Listing.objects.get(pk=id)
    current_user = request.user
    watchlisted = False

    if current_user.is_authenticated:
        current_user_watchlist = current_user.watchlist.all()

        if listing in current_user_watchlist:
            watchlisted = True

    return render(request, "auctions/item.html", {
        "listing": listing,
        "logged_in_user": request.user.id,
    "comments": listing.listing_comments.all(),
        "watchlisted": watchlisted
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

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def watchlist(request):
    current_user = request.user
    
    return render(request, "auctions/index.html", {
        "listings": current_user.watchlist.all(),
        "title": "Watchlist"
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        photo_url = request.POST["photo_url"]
        starting_bid = request.POST["starting_bid"]
        category_id = int(request.POST["category"])
        category = Category.objects.get(pk=category_id)
        owner = request.user

        if title and desc and starting_bid:

            # Create the Listing object
            listing = Listing.objects.create(title=title, desc=desc, photo_url=photo_url, startingBid=starting_bid, owner=owner, category=category)

            return render(request, "auctions/create.html", {
                "success": "Successfully created listing!",
                "categories": Category.objects.all()
            })

        else:
            return render(request, "auctions/create.html", {
                "failure": "Please fill all compulsory fields!",
                "categories": Category.objects.all()
            })
            
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


def add_comment(request, id):
    if request.method == "POST":
        current_user = request.user

        if current_user.is_authenticated:
            text = request.POST["comment"]
            listing = Listing.objects.get(pk=id)
            
            comment = Comment.objects.create(
                commenter=current_user,
                text=text,
                listing=listing
            )

            return HttpResponseRedirect(reverse("item", args=(id,)))
        else:
            return HttpResponseRedirect(reverse("login"))

def edit_listing(request, id):
    listing = Listing.objects.get(pk=id)
   

    if request.method == 'POST':
        listing.title = request.POST["title"]
        listing.desc = request.POST["desc"]
        listing.photo_url = request.POST["photo_url"]
        category_id = int(request.POST["category"])
        listing.category = Category.objects.get(pk=category_id)

        listing.save()

        return HttpResponseRedirect(reverse("item", args=(id,)))
    else:
        return render(request, "auctions/edit.html", {
            "listing": listing,
            "categories": Category.objects.exclude()
        })  

def listings_category(request, category):
    category = Category.objects.get(name=category)
    return render(request, "auctions/index.html", {
        "listings": category.listings.all(),
        "category": category.name
    })

def add_to_watchlist(request, id):   
    current_user = request.user

    if current_user.is_authenticated: 
        listing = Listing.objects.get(pk=id)
        listing.watchlisted_by.add(current_user)
        return HttpResponseRedirect(reverse("item", args=(id,)))
    else:
        return HttpResponseRedirect(reverse("login"))

def remove_from_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    listing.watchlisted_by.remove(request.user)
    return HttpResponseRedirect(reverse("item", args=(id,)))

def place_bid(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            listing = Listing.objects.get(pk=id)
            highestBid = listing.highestBid

            try:
                currentBid = float(request.POST["bid"])
            except:
                messages.error(request, "Bid field cannot be empty.")
                return HttpResponseRedirect(reverse("item", args=(id,)))

            if currentBid > highestBid:
                listing.highestBid = currentBid
                listing.winner = request.user
                listing.save()
                messages.success(request, "Your bid was placed successfully.")
                
                return HttpResponseRedirect(reverse("item", args=(id,)))
            else:
                messages.error(request, "Your bid must be higher than the current highest bid.")
                return HttpResponseRedirect(reverse("item", args=(id,)))
 
    else:
        messages.error(request, "You must be logged in to place a bid.")
        return HttpResponseRedirect(reverse("login"))

def close_listing(request, id):
    listing = Listing.objects.get(pk=id)
    listing.isActive = False
    listing.save()
    return HttpResponseRedirect(reverse("item", args=(id,)))