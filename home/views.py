"""Main views for the site"""

from django.shortcuts import render
from django.views import View
from django.utils import timezone

from schedules.models import ScheduledRun, Action
from home.models import Log


class DashboardView(View):
    template_name = "home/home.html"

    def get(self, request, *args, **kwargs):
        now = timezone.datetime(2019, 10, 1)
        current_weather = "Sunny"
        current_temperature = 28
        tank_level = 65
        timespan = timezone.timedelta(hours=24)
        upcoming_schedules = ScheduledRun.objects.filter(
            start__gte=now, start__lt=now + timespan)
        upcoming_actions = Action.objects.filter(
            datetime__gte=now, datetime__lt=now + timespan)
        last_logs = Log.objects.order_by("-datetime")[:5]

        context = {
            "pagetitle": "Home",
            "current_weather": current_weather,
            "current_temperature": current_temperature,
            "tank_level": tank_level,
            "schedule_list": upcoming_schedules,
            "action_list": upcoming_actions,
            "log_list": last_logs,
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = "home/about.html"

    def get(self, request, *args, **kwargs):
        "GET request handler"
        context = {
            "pagetitle": "About"
        }
        return render(request, self.template_name, context)
