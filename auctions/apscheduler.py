from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.db.models import Q, F
import atexit
from threading import Lock

scheduler = BackgroundScheduler()
job_id = 'close_expired_auctions'  # Unique ID for the job
lock = Lock()

def close_expired_auctions():
    global lock

    if lock.locked():
        print('close_expired_auctions is already running. Skipping...')
        return

    with lock:
        print('Running close_expired_auctions')
        current_time = timezone.now()

        from .models import Listing, Status

        # Get expired listings that are either pending or have bids and end_time is expired
        expired_listings = Listing.objects.filter(
            Q(status=Status.PENDING, end_time__lte=current_time) |
            Q(bid__isnull=False, end_time__lte=current_time)
        )

        print(f'Number of expired listings found: {expired_listings.count()}')

        for listing in expired_listings:
            if listing.bid is None:
                print(f'Listing ID {listing.id} - Status updated from "Pending" to "Closed". Listing will be deleted.')
                listing.status = Status.CLOSED
                listing.delete()  # Delete the listing with no bids
            else:
                print(f'Listing ID {listing.id} - Status updated from "Pending" to "Closed".')
                listing.status = Status.CLOSED
                listing.highest_bid = listing.bid  # Update the highest_bid field
                listing.save()

        # Update the status of remaining listings that have bids and end_time is expired
        remaining_listings = Listing.objects.filter(bid__isnull=False, end_time__lte=current_time)
        remaining_listings.update(status=Status.CLOSED, highest_bid=F('bid'))

        print('Expired listings closed/deleted.')

        # Check the count of active listings
        active_listings_count = Listing.objects.filter(status=Status.PENDING).count()
        print(f'Number of active listings: {active_listings_count}')

def initialize_scheduler():
    try:
        # Check if the job with the given ID already exists
        if not scheduler.get_job(job_id):
            # Add the scheduler job to run the function every 10 seconds
            scheduler.add_job(close_expired_auctions, 'interval', seconds=10, id=job_id)
            atexit.register(lambda: scheduler.shutdown(wait=False))  # Register atexit to shut down the scheduler
            scheduler.start()
            print('Scheduler started successfully.')
        else:
            print('Scheduler is already running.')
    except Exception as e:
        print(f'Error starting scheduler: {e}')

# Start the scheduler when the module is imported
initialize_scheduler()