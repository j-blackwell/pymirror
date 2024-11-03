from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from widgets.bins.bins import update_bins
from widgets.football.football import update_football_matches
from widgets.tfl.tfl_departures import update_tfl_departures
from widgets.tfl.tfl_status import update_tfl_status
from widgets.weather.weather import update_weather


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=update_bins,
        trigger=CronTrigger(month="*", day="*", hour=0, minute=0),
        id="bins",
        replace_existing=True,
    )
    scheduler.add_job(
        func=update_football_matches,
        trigger=CronTrigger(month="*", day="*", hour=0, minute=0),
        id="football",
        replace_existing=True,
    )
    scheduler.add_job(
        func=update_tfl_departures,
        trigger=CronTrigger(month="*", day="*", hour="*", minute="*", second=50),
        id="tfl_departures",
        replace_existing=True,
    )
    scheduler.add_job(
        func=update_tfl_status,
        trigger=CronTrigger(month="*", day="*", hour="*", minute="*", second=50),
        id="tfl_status",
        replace_existing=True,
    )
    scheduler.add_job(
        func=update_weather,
        trigger=CronTrigger(month="*", day="*", hour="*", minute=0, second=0),
        id="weather",
        replace_existing=True,
    )

    scheduler.start()


# Keep the script running
def update_all():
    start_scheduler()

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    update_all()
