"""Script experimeting with requred schedule creation"""

from datetime import date, datetime, time, timedelta

from django.db.models import F, ExpressionWrapper, BigIntegerField
from django.db.models.functions import Now, TruncDate

from programs.models import Program
from schedules.models import RequestedRun

def get_req_run_once_programs():
    return Program.objects.filter(
        enabled=True,
        program_type="run-once",
        date_start=date.today()
    )

def get_req_periodic_programs():
    return Program.objects.filter(
        enabled=True,
        program_type="periodic",
        date_start__lte=date.today(),
    ).exclude(
        date_end__lt=date.today()
    ).annotate(
        days_since_start=ExpressionWrapper(
            TruncDate(Now()) - F('date_start'), # calculate timedelta
            output_field=BigIntegerField()
            ) / 86400000000,                    # microseconds in a day
    )

def get_req_weekly_programs():
    return Program.objects.filter(
        enabled=True,
        program_type="weekly",
        date_start__lte=date.today(),
    ).exclude(
        date_end__lt=date.today()
    ).filter(
        days_of_week__contains=date.today().isoweekday()
    )

def request_run(program, _date=date.today()):
    "Insert run requests in the 'requestedrun' table"
    for channel in program.channels.all():
        RequestedRun.objects.create(
            program=program,
            zone=channel,
            start=datetime.combine(_date, program.time_start),
            duration=program.duration
        ).save()

def request_all():
    querysets = [
        get_req_run_once_programs(),
        get_req_periodic_programs(),
        get_req_weekly_programs()
    ]

    for queryset in querysets:
        for program in queryset:
            request_run(program)
            