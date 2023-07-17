from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from decimal import *
from django.db.models import Max
from .models import User, Listing, Bid, Comment, UserHistory, WatchlistItem
from .forms import ListingForm
from .decorators import Unauthenticated_user, Authenticated_user
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.apps import apps
from django.contrib import messages

# dictionary variable to keep track of individual's watchlist
watch_list = dict()

def index(request):
    listings = []
    items = Listing.objects.filter(status="Pending")
    for item in items:
        try:
            bid = Bid.objects.get(listing=item)
        except:
            bid = None
        listings.append({
            'listing': item,
            'bid': bid,
        })
    context = {
        'listings': listings,
    }
    return render(request, "auctions/index.html", context)

@Unauthenticated_user
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@Authenticated_user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


@Unauthenticated_user
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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@Authenticated_user
def listing(request, listing_id):
    item = get_object_or_404(Listing, pk=listing_id)
    old_bid = Bid.objects.filter(listing=item)

    if item.status == 'Closed':
        try:
            bid = old_bid[0]
            if bid.user == request.user:
                context = {
                    'listing': item,
                    'bid': bid,
                }
                return render(request, 'auctions/success.html', context)
        except IndexError:
            return render(request, 'auctions/closed.html')

    comments = Comment.objects.filter(listing=item)
    
    if old_bid.count() == 1:
        default_bid = old_bid[0].highest_bid + 10
    else:
        default_bid = item.initial + 10

    try:
        bid_info = Bid.objects.get(listing=item)
    except Bid.DoesNotExist:
        bid_info = None

    form = ListingForm(instance=item)

    if request.method == 'POST':
        form = ListingForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return render(request, 'auctions/success.html')
    
    context = {
        'listing': item,
        'bid': bid_info,
        'comments': comments,
        'default_bid': default_bid,
        'form': form,
    }
    return render(request, "auctions/listing.html", context)

def update_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.user != request.user:
        return redirect('auctions:listing', listing_id=listing_id)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('auctions:listing', listing_id=listing_id)
    else:
        form = ListingForm(instance=listing)
    
    context = {
        'form': form,
        'listing': listing,
    }
    return render(request, 'auctions/update_listing.html', context)

@Authenticated_user
def bid(request):
    if request.method == "POST":
        new_bid = request.POST.get("bid")  # Use get() instead of indexing to handle missing bid value gracefully
        item_id = request.POST.get("list_id")

        if new_bid is not None and new_bid.strip():  # Check if bid value is not empty or None
            try:
                new_bid_decimal = Decimal(new_bid)  # Convert bid value to Decimal

                item = Listing.objects.get(pk=item_id)
                old_bid = Bid.objects.filter(listing=item)

                if old_bid.count() < 1:
                    bid = Bid(user=request.user, listing=item, highest_bid=new_bid_decimal)
                    bid.save()
                    messages.success(request, 'Bid Placed Successfully!', fail_silently=True)
                elif new_bid_decimal < old_bid[0].highest_bid:
                    messages.warning(request, 'The bid you placed was lower than needed.', fail_silently=True)
                elif new_bid_decimal == old_bid[0].highest_bid:
                    messages.warning(request, 'The bid you placed was the same as the current bid', fail_silently=True)
                else:
                    old_bid = Bid.objects.get(listing=item)
                    old_bid.highest_bid = new_bid_decimal
                    old_bid.user = request.user
                    old_bid.save()
                    messages.success(request, 'Bid Placed Successfully!', fail_silently=True)
            except ValueError:
                messages.warning(request, 'Invalid bid value. Please enter a valid number.', fail_silently=True)
        else:
            messages.warning(request, 'Bid value is required.', fail_silently=True)

    return redirect("auctions:listing", item_id)


@Authenticated_user
def comment(request):
    if request.method == "POST":
        content = request.POST["content"]
        item_id = request.POST["list_id"]
        item = Listing.objects.get(pk=item_id)
        newComment = Comment(user=request.user, comment=content, listing=item)
        newComment.save()
        return redirect("auctions:listing", item_id)
    return redirect("auctions:index")

@Authenticated_user
def watchlist(request):
    watchlist_items = WatchlistItem.objects.filter(user=request.user)

    context = {
        'listings': watchlist_items,
    }
    return render(request, "auctions/watchlist.html", context)

@Authenticated_user
def add_to_watchlist(request, item_id):
    item = Listing.objects.get(pk=item_id)

    if WatchlistItem.objects.filter(user=request.user, listing=item).exists():
        messages.warning(request, 'Item already present in your WatchList.', fail_silently=True)
    else:
        watchlist_item = WatchlistItem(user=request.user, listing=item)
        watchlist_item.save()
        messages.success(request, 'Successfully added item to your WatchList.', fail_silently=True)

    return redirect("auctions:index")

@Authenticated_user
def remove_from_watchlist(request, item_id):
    item = Listing.objects.get(pk=item_id)

    try:
        watchlist_item = WatchlistItem.objects.get(user=request.user, listing=item)
        watchlist_item.delete()
        messages.success(request, 'Successfully removed item from your WatchList.', fail_silently=True)
    except WatchlistItem.DoesNotExist:
        messages.warning(request, 'Item not found in your WatchList.', fail_silently=True)

    return redirect("auctions:index")

def categories(request):
    category = dict()
    listings = Listing.objects.filter(status="Pending")
    for item in listings:
        try:
            bid = Bid.objects.get(listing=item)
        except:
            bid = None
        if item.category not in category:
            category[item.category] = []
        category[item.category].append({
            'listing': item,
            'bid': bid,
        })
    context = {
        'category_list': category,
    }
    return render(request, "auctions/category.html", context)

@Authenticated_user
def success(request):
    return render(request, "auctions/success.html")

@Authenticated_user
def addListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES or None)

        if form.is_valid():
            newListing = form.save(commit=False)
            newListing.user = request.user
            newListing.save()
            messages.success(request, 'Successfully created your listing.', fail_silently=True)
        else:
            messages.error(request, 'PLEASE select correct date', fail_silently=True)
            return redirect("auctions:add_listing")
        return redirect("auctions:index")
    form = ListingForm()
    context = {
        'form': form,
    }
    return render(request, "auctions/addListing.html", context)

def closeExpiredAuctions():
    current_time = timezone.now()
    expired_listings = Listing.objects.filter(end_time__lte=current_time, bid__isnull=True)

    for listing in expired_listings:
        listing.delete()

@Authenticated_user
def user_listings(request):
    category = dict()
    current_user_listings = Listing.objects.filter(user=request.user, status='Pending')
    
    for item in current_user_listings:
        try:
            bid = Bid.objects.get(listing=item)
        except Bid.DoesNotExist:
            bid = None
        
        if item.category not in category:
            category[item.category] = []
        
        category[item.category].append({
            'listing': item,
            'bid': bid,
        })
    
    context = {
        'category_list': category,
    }
    
    return render(request, "auctions/userlistings.html", context)


@Authenticated_user
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing.user == request.user:
        listing.status = 'Closed'
        listing.save()
        messages.success(request, 'Listing successfully closed.', fail_silently=True)
    else:
        messages.warning(request, 'Unable to close listing! Authentication error.', fail_silently=True)
    return redirect("auctions:user_listings")

def search_results(request):
    query = request.GET.get('query')
    if query:
        listings = Listing.objects.filter(name__icontains=query)
    else:
        listings = []
    context = {
        'listings': listings,
        'query': query
    }
    return render(request, 'auctions/search_results.html', context)

@Authenticated_user
def user_history(request):
    user = request.user
    history = UserHistory.objects.filter(user=user).order_by('-timestamp')
    history_with_details = []
    for item in history:
        listing = item.listing
        highest_bid = UserHistory.objects.filter(listing=listing).aggregate(Max('bid'))['bid__max']
        is_highest_bidder = item.bid == highest_bid
        listing_image_url = listing.image.url if listing.image else '/static/auctions/uploads/None/NIA.png'
        history_with_details.append({
            'listing_name': listing.name,
            'listing_image_url': listing_image_url,
            'category': listing.category,
            'price': listing.initial,
            'bid': listing.bid,
            'timestamp': item.timestamp,
            'is_highest_bidder': is_highest_bidder
        })
    return render(request, 'auctions/user_history.html', {'history': history_with_details})



