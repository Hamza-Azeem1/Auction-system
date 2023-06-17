from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class User(AbstractUser):
    pass

# stores the Listings
class Listing(models.Model):
    CATEGORIES = [
        ('Accessories', 'Accessories'),
        ('Antiques', 'Antiques'),
        ('Clothes', 'Clothes'),
        ('Decoration', 'Decoration'),
        ('Electronics', 'Electronics'),
        ('Valuables', 'Valuables'),
        ('Other', 'Other'),
    ]
    STATUS = [
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    ]
    DEFAULT_USER = 1
    name = models.CharField(max_length=100, blank=False)
    initial = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, default=DEFAULT_USER)
    image = models.ImageField(default='None/NIA.png')
    category = models.CharField(max_length=11, choices=CATEGORIES, default='Other')
    status = models.CharField(max_length=7, choices=STATUS, default='Pending')
    created = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - starts at ${self.initial}"

    @property
    def search_name(self):
        return self.name.lower()

    def is_valid_listing(self):
        return len(self.name) > 0 and self.initial > 0

    auction_end_time = models.DateTimeField(null=True, blank=True)

    def is_auction_expired(self):
        return self.auction_end_time and timezone.now() >= self.auction_end_time

    def save(self, *args, **kwargs):
        if not self.auction_end_time:
            self.auction_end_time = timezone.now() + timedelta(days=1)
        super().save(*args, **kwargs)
   


# stores the bids for the Listings
class Bid(models.Model):
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    highest_bid = models.DecimalField(max_digits = 10, decimal_places = 2)
    added = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"${self.highest_bid} - {self.user} on {self.listing.name}"


# stores the comments on the Listings
class Comment(models.Model):
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, blank = False, on_delete = models.CASCADE)
    comment = models.CharField(max_length = 400, blank = False)
    added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.comment} - by {self.user}"


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Add other fields as needed from the Listing model
    listing_name = models.CharField(max_length=100)
    listing_image = models.ImageField(upload_to='listing_images')
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        listing = self.listing
        self.listing_name = listing.name
        self.listing_image = listing.image
        self.category = listing.category
        self.price = listing.initial
        self.bid = listing.bid
        super().save(*args, **kwargs)

class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Watchlist: {self.listing.name}"