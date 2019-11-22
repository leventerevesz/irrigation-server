from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.utils import timezone

from schedules.models import ScheduledRun,  Action

class ScheduledRunListView(ListView):
    template_name = "schedules/list.html"
    now = timezone.datetime(2019,10,1)
    timespan = timezone.timedelta(hours=24)
    queryset = ScheduledRun.objects.filter(start__gte=now, start__lt=now + timespan)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pagetitle"] = "Schedules"
        return context

class UpcomingActionsListView(ListView):
    now = timezone.datetime(2019,10,1)
    timespan = timezone.timedelta(hours=24)
    queryset = Action.objects.filter(datetime__gte=now, datetime__lt=now + timespan)