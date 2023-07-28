from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
import atexit
from threading import Lock
from .models import Listing, Status, Bid

job_id = 'close_expired_auctions'  # Unique ID for the job
lock = Lock()

def close_auctions(current_time):
    # Your close_auctions logic goes here
    # Get all active listings that have already ended (closing_time <= current_time)
    active_listings = Listing.objects.filter(status=Status.PENDING, end_time__lte=current_time)

    for listing in active_listings:
        bids_exist = Bid.objects.filter(listing=listing).exists()

        if bids_exist:
            # If there are bids, update the status to 'Closed'
            listing.status = Status.CLOSED
            highest_bid = Bid.objects.filter(listing=listing).order_by('-highest_bid').first()
            listing.highest_bid = highest_bid.highest_bid  # Update the highest_bid field with the bid amount
            listing.save()
        else:
            # If there are no bids, delete the listing
            listing.delete()


def close_expired_auctions():
    global lock

    if lock.locked():
        print('close_expired_auctions is already running. Skipping...')
        return

    with lock:
        current_time = timezone.now()
        print('Running close_expired_auctions', current_time)

        # Get expired listings that are pending
        expired_listings = Listing.objects.filter(
            status=Status.PENDING,
            end_time__lte=current_time
        )

        for listing in expired_listings:
            print(f'Listing ID {listing.id} - Status updated from "Pending" to "Closed".')
            highest_bid = Bid.objects.filter(listing=listing).order_by('-highest_bid').first()

            if highest_bid is None:
                # If there are no bids, set the status to "Closed" and highest_bid to None
                listing.status = Status.CLOSED
                listing.highest_bid = None
            else:
                # If there are bids, set the status to "Closed" and update the highest_bid field
                listing.status = Status.CLOSED
                listing.highest_bid = highest_bid.highest_bid

            listing.save()

        print(f'Number of expired listings found: {expired_listings.count()}')

        print('Expired listings closed/updated.')

        # Check the count of active listings
        active_listings_count = Listing.objects.filter(status=Status.PENDING).count()
        print(f'Number of active listings: {active_listings_count}')


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(close_expired_auctions, 'interval', minutes=1, id=job_id)
    atexit.register(lambda: scheduler.shutdown(wait=False))  # Register atexit to shut down the scheduler
    scheduler.start()
    print('Scheduler started successfully.')
