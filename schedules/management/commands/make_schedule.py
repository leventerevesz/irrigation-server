from datetime import datetime, date, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from programs.models import Program
from schedules.models import RequestedRun, ScheduledRun

class Command(BaseCommand):
    help = "Creates a scheduled run from requests"
