from django.apps import AppConfig
from .apscheduler import initialize_scheduler, scheduler

class AuctionsConfig(AppConfig):
    name = 'auctions'

    def ready(self):
        # Start the scheduler when the app is ready, but only if it's not already running
        if not scheduler.running:
            initialize_scheduler(scheduler)
