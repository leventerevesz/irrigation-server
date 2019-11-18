from io import StringIO
from datetime import datetime, date, time

from django.core.management import call_command
from django.test import TestCase

from programs.models import Program
from schedules.models import RequestedRun

thedate = date(2019, 10, 1) # fixtures use this date

class RequestScheduleTestCase(TestCase):
    fixtures = ["programs", "zones"]

    def setUp(self):
        out = StringIO()
        call_command("request-schedule", f"--date={thedate.isoformat()}", stdout=out)
        self.assertIn("SUCCESS.", out.getvalue())

    def test_runonce_gets_scheduled(self):
        entry = RequestedRun.objects.get(program_id=1)
        self.assertEquals(entry.program.name, "Simple run-once program")
    
    def test_periodic_gets_scheduled(self):
        entry = RequestedRun.objects.get(program_id=2)
        self.assertEquals(entry.program.name, "Simple periodic program")

    def test_weekly_gets_scheduled(self):
        entry = RequestedRun.objects.get(program_id=11)
        self.assertEquals(entry.program.name, "Everyday weekly program")
    
    def test_duration(self):
        program = Program.objects.get(pk=1)
        entry = RequestedRun.objects.get(program_id=1)
        self.assertEqual(program.duration, entry.duration)
    
    def test_start_date(self):
        entry = RequestedRun.objects.get(program_id=1)
        self.assertEqual(entry.start.date(), thedate)

#class MakeScheduleTestCase(TestCase):

# no requests for today