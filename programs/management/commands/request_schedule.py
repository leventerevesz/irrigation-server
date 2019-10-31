from datetime import datetime, date, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from programs.models import Program
from schedules.models import RequestedRun



class Command(BaseCommand):
    help = "Creates a scheduled run for all irrigation events due today"

    def handle(self, *args, **options):
        thedate = date(2019, 10, 31)

        qs1 = self.get_runonce_programs(thedate)
        qs2 = self.get_periodic_programs(thedate)
        qs3 = self.get_weekly_programs(thedate)

        queryset = qs1.union(qs2, qs3)

        for program in queryset:
            self.stdout.write("Processing [{}] {} ...".format(program.id, program.name))
            start = datetime.combine(date=thedate, time=program.time_start)
            for zone in program.zones.all():
                self.stdout.write("  -> zone {}".format(zone.name))
                entry = RequestedRun(program=program, zone=zone, start=start, duration=program.duration)
                entry.save()

        self.stdout.write(self.style.SUCCESS("All OK."))


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
