from datetime import datetime, date, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from programs.models import Program
from schedules.models import RequestedRun


class Command(BaseCommand):
    help = "Creates a scheduled run for all irrigation events due today"

    def add_arguments(self, parser):
        parser.add_argument("--date", help="the day to create a schedule for")

    def handle(self, *args, **options):
        thedate = self._get_date(options.get("date"))

        qs1 = self.get_runonce_programs(thedate)
        qs2 = self.get_periodic_programs(thedate)
        qs3 = self.get_weekly_programs(thedate)

        queryset = qs1.union(qs2, qs3)

        program_count = 0
        entry_count = 0

        for program in queryset:
            program_count += 1
            start = datetime.combine(date=thedate, time=program.time_start)
            for zone in program.zones.all():
                entry_count += 1
                entry = RequestedRun(program=program, zone=zone, start=start, duration=program.duration)
                entry.save()

        self.stdout.write(f"Date: {thedate}")
        self.stdout.write(f"Found {program_count} programs.")
        self.stdout.write(f"Created {entry_count} schedule entries.")
        self.stdout.write(self.style.SUCCESS("SUCCESS."))

    def _get_date(self, datestr):
        if datestr is None:
            thedate = date.today()
        else:
            thedate = date.fromisoformat(datestr)
        return thedate

    def get_runonce_programs(self, thedate):
        programs = Program.objects.filter(enabled=True, program_type="run-once", date_start=thedate)
        return programs
    
    def get_periodic_programs(self, thedate):
        programs = Program.objects.filter(enabled=True, program_type="periodic")
        programs = self._filter_start_end_dates(programs, thedate)
        programs = self._filter_period(programs, thedate)
        return programs

    def get_weekly_programs(self, thedate):
        programs = Program.objects.filter(enabled=True, program_type="weekly")
        programs = self._filter_start_end_dates(programs, thedate)
        programs = self._filter_weekday(programs, thedate)
        return programs
    
    def _filter_start_end_dates(self, programs, thedate):
        return programs.exclude(date_start__gt=thedate).exclude(date_end__lt=thedate)

    def _filter_period(self, programs, thedate):
        pk_list = []
        for p in programs:
            if self._periodic_is_due(p.date_start, thedate, p.period):
                pk_list.append(p.pk)
        return programs.filter(pk__in=pk_list)

    def _periodic_is_due(self, base_date, current_date, period):
        diff = (current_date - base_date).days
        mod = diff % period
        is_due = (mod == 0)
        return is_due

    def _filter_weekday(self, programs, thedate):
        day = str(thedate.isoweekday())
        return programs.filter(days_of_week__contains=day)
