from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from enum import Enum

class Category(Enum):
    ACCESSORIES = 'Accessories'
    ANTIQUES = 'Antiques'
    CLOTHES = 'Clothes'
    DECORATION = 'Decoration'
    ELECTRONICS = 'Electronics'
    VALUABLES = 'Valuables'
    OTHER = 'Other'

class Status(Enum):
    PENDING = 'Pending'
    CLOSED = 'Closed'

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=100, blank=False)
    initial = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='listings')
    image = models.ImageField(upload_to='listing_images', default='None/NIA.png')
    category = models.CharField(max_length=11, choices=[(cat.name, cat.value) for cat in Category], default=Category.OTHER.value)
    status = models.CharField(max_length=7, choices=[(stat.name, stat.value) for stat in Status], default=Status.PENDING.value)
    created = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='won_listings')

    def __str__(self):
        return f"{self.name} - starts at ${self.initial}"

    @property
    def search_name(self):
        return self.name.lower()

    def is_valid_listing(self):
        return len(self.name) > 0 and self.initial > 0

    def is_auction_expired(self):
        return self.end_time <= timezone.now()

    def close_auction(self):
        if self.status == Status.CLOSED.value:
            return

        if not self.bid:
            self.status = Status.CLOSED.value
            self.save()
            return

        self.highest_bid = self.bids.order_by('-highest_bid').first().highest_bid
        self.winner = self.bids.filter(highest_bid=self.highest_bid).first().user
        self.status = Status.CLOSED.value
        self.save()

    def save(self, *args, **kwargs):
        if self.is_auction_expired() and self.status == Status.PENDING.value:
            self.close_auction()

        super().save(*args, **kwargs)

class Bid(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2)
    added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"${self.highest_bid} - {self.user} on {self.listing.name}"

class Comment(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, blank=False, on_delete=models.CASCADE)
    comment = models.CharField(max_length=400, blank=False)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment} - by {self.user}"

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

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
