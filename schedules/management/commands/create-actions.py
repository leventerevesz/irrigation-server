from datetime import datetime, date, time, timedelta

from django.core.management.base import BaseCommand, CommandError

from home.models import Settings
from schedules.models import RequestedRun, ScheduledRun, Action

class Command(BaseCommand):
    help = "Creates a scheduled run from requests"

    def add_arguments(self, parser):
        parser.add_argument("--date", help="the day to make the schedule for. YYYY-MM-DD")
    
    def get_date(self, datestr):
        if datestr is None:
            thedate = date.today()
        else:
            thedate = date.fromisoformat(datestr)
        return thedate
    
    def handle(self, *args, **options):
        thedate = self.get_date(options.get("date"))

        scheduled_runs = ScheduledRun.objects.filter(start__date=thedate)
        for sched in scheduled_runs:
            for channel in sched.request.zone.channels.all():
                open_action = Action.objects.create(
                    schedule=sched,
                    channel=channel,
                    datetime=sched.start,
                    command="o"
                )
                close_action = Action.objects.create(
                    schedule=sched,
                    channel=channel,
                    datetime=sched.start + sched.duration,
                    command="c"
                )
                open_action.save()
                close_action.save()
