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
from django.core.exceptions import PermissionDenied
from django.http import Http404
from decimal import Decimal
from django.http import JsonResponse
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

# dictionary variable to keep track of individual's watchlist
watch_list = dict()

def checkout(request):
    listing_id = request.GET.get('listing_id')
    if not listing_id:
        return redirect("auctions:index")

    try:
        listing = Listing.objects.get(pk=listing_id, status='Closed', highest_bid__isnull=False)
    except Listing.DoesNotExist:
        return redirect("auctions:index")

    # Get the amount to charge the user (you may want to handle currency conversion, etc.)
    amount = int(listing.highest_bid * 100)  # Amount in cents

    if request.method == "POST":
        # Token is created by Stripe.js
        token = request.POST.get("stripeToken")

        try:
            # Create a charge: this will charge the user's card
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description="Auction Payment",
            )

            # Update the listing to mark it as paid or perform any other necessary actions
            listing.paid = True
            listing.save()

            return redirect("auctions:thank_you")
        except stripe.error.CardError as e:
            # Display error to the user
            return render(request, "auctions/checkout.html", {"error": str(e)})

    return render(request, "auctions/checkout.html", {"listing": listing, "amount": amount})

def view_winner(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    # Get the highest bid for this listing
    highest_bid = Bid.objects.filter(listing=listing).order_by('-highest_bid').first()

    winner = None
    if highest_bid:
        winner = highest_bid.user

    context = {
        'listing': listing,
        'winner': winner,
    }

    return render(request, 'auctions/winner.html', context)    

def index(request):
    listings = []
    items = Listing.objects.all()
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
        'listings': listings,  # Make sure the variable name here is 'listings'
    }
    return render(request, "auctions/index.html", context)



@Unauthenticated_user
def login_view(request):
        return render(request, "auctions/login.html")


@Authenticated_user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
            return render(request, 'auctions/closed.html')
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
                    item.bid = new_bid_decimal
                    item.save()
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
                    item.bid = new_bid_decimal
                    item.save()
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
    try:
        # Get the user's highest bid and the related listing
        highest_bid = Bid.objects.filter(user=request.user).order_by('-highest_bid').first()
        if not highest_bid:
            raise Http404("You haven't placed any bids yet.")
        
        listing = highest_bid.listing
        
        # Check if the auction is closed
        if listing.status != 'Closed':
            raise Http404("The auction is still active.")
        
        # Check if the user is the highest bidder
        if highest_bid == listing.highest_bid:
            context = {
                'listing': listing,
            }
            return render(request, 'auctions/success.html', context)
        else:
            raise Http404("You are not the highest bidder.")
    except Http404 as e:
        messages.error(request, str(e), fail_silently=True)
        return redirect("auctions:index")

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
            return redirect("auctions:addListing")
        return redirect("auctions:index")
    form = ListingForm()
    context = {
        'form': form,
    }
    return render(request, "auctions/addListing.html", context)

@Authenticated_user
def user_listings(request):
    category = dict()
    current_user_listings = Listing.objects.filter(user=request.user)
    
    for item in current_user_listings:
        # try:
        #     bid = Bid.objects.get(listing=item)
        # except Bid.DoesNotExist:
        #     bid = None
        
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
    return redirect("auctions:index")


def closeExpiredAuctions():
    current_time = timezone.now()
    expired_listings = Listing.objects.filter(end_time__lte=current_time, status='Pending')

    for listing in expired_listings:
        listing.status = 'Closed'
        listing.close_auction()
        listing.save()

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