from datetime import date, datetime, time, timedelta

from django.test import TestCase

from programs.models import Program

import sys


class ProgramTestCase(TestCase):
    "Program tests"
    fixtures = ['zones', 'programs']

    def test_fixture_loading(self):
        p = Program.objects.get(pk=1)
        self.assertTrue(isinstance(p, Program))

    def test_program_name(self):
        p = Program.objects.get(name="Simple run-once program")
        self.assertEqual(p.name, "Simple run-once program")
    
    def test_program_desc_unicode(self):
        p = Program.objects.get(name="Unicode description")
        self.assertEqual(p.description, "Árvíztűrő tükörfúrógép")

    def create_dummy_program(
            self, 
            name="dummy program", 
            program_type="run-once", 
            date_start=date.today(), 
            time_start=datetime.now().time(), 
            **kwargs):
        return Program.objects.create(name=name, program_type=program_type, date_start=date_start, time_start=time_start, **kwargs)

    def test_program_type(self):
        pr = self.create_dummy_program(program_type="run-once")
        pp = self.create_dummy_program(program_type="periodic")
        pw = self.create_dummy_program(program_type="weekly")
        pr = Program.objects.get(pk=pr.pk)
        pp = Program.objects.get(pk=pp.pk)
        pw = Program.objects.get(pk=pw.pk)
        self.assertEqual(pr.program_type, "run-once")
        self.assertEqual(pp.program_type, "periodic")
        self.assertEqual(pw.program_type, "weekly")

    def test_date_start(self):
        p = self.create_dummy_program(self, date_start=date.today())
        p = Program.objects.get(pk=p.pk)
        self.assertEqual(p.date_start, date.today())
    
    def test_program_str(self):
        p = self.create_dummy_program(pk=99, name="__str__ test program")
        disp_str = p.__str__()
        self.assertEqual(disp_str, "(99) __str__ test program")

    def test_get_absolute_url(self):
        p = self.create_dummy_program(pk=919)
        url = p.get_absolute_url()
        self.assertTrue(url.count("919") == 1)
