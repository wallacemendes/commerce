from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CommentForm, ListingForm
from .models import Bid, Category, Listing, User


def index(request):
    category = request.GET.get("category", "")
    if category:
        listing = Listing.objects.filter(
            category__name=category, is_active=True
        )
    else:
        listing = Listing.objects.filter(is_active=True)
    return render(
        request,
        "auctions/index.html",
        {"listing": listing, "category": category},
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
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
            return render(
                request,
                "auctions/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "auctions/register.html")


def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, "auctions/create.html", {"form": form})


def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        listing_id = request.POST["listing-id"]
        if request.POST.get("remove") == "yes":
            request.user.watchlist.remove(listing_id)
            return HttpResponseRedirect(reverse("watchlist"))
        request.user.watchlist.add(listing_id)
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        context = {"watchlist": request.user.watchlist.all()}
        return render(request, "auctions/watchlist.html", context)


def categories_view(request):
    context = {"categories": Category.objects.all()}
    return render(request, "auctions/categories.html", context)


def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if request.user.is_authenticated:
        in_watchlist = request.user.watchlist.contains(listing)
        user_bids = listing.bids.filter(user=request.user)
        comment_form = add_comment(request)
    else:
        in_watchlist = False
        user_bids = []
        comment_form = None

    is_owner = True if listing.created_by == request.user else False
    comments = listing.comments.all()

    return render(
        request,
        "auctions/page.html",
        {
            "listing": listing,
            "in_watchlist": in_watchlist,
            "is_owner": is_owner,
            "user_bids": user_bids,
            "comment_form": comment_form,
            "comments": comments,
        },
    )


def bid(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    bid_amount = float(request.POST["bid-amount"])
    listing = Listing.objects.get(id=request.POST["listing-id"])
    if request.user == listing.created_by:
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    if bid_amount <= listing.current_bid:
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    b = Bid(value=bid_amount, user=request.user, listing=listing)
    try:
        b.clean()
    except ValidationError as e:
        print(e.message_dict)

    b.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def open_or_close_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listing = Listing.objects.get(id=request.POST["listing-id"])
    listing.is_active = not listing.is_active
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def add_comment(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        listing_id = request.POST["listing-id"]
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = Listing.objects.get(id=listing_id)
            comment.save()
            return HttpResponseRedirect(
                reverse("listing", args=([listing_id]))
            )
    else:
        return CommentForm()


def my_bids(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listings = set(Listing.objects.filter(bids__user=request.user))

    print(listings)
    return render(request, "auctions/mybids.html", {"listings": listings})
