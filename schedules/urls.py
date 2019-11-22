from django.urls import path

from schedules.views import ScheduledRunListView

app_name = "schedules"
urlpatterns = [
    path("", ScheduledRunListView.as_view(), name="overview"),
]