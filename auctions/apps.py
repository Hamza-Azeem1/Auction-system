from django.apps import AppConfig

class AuctionsConfig(AppConfig):
    name = 'auctions'

    def ready(self):
        # Start the scheduler when the app is ready, but only if it's not already running
        from apscheduler.schedulers.background import BackgroundScheduler
        from .apscheduler import start_scheduler

        if not BackgroundScheduler().running:
            start_scheduler()
