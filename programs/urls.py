"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from programs.views import (
    ProgramCreateView,
    ProgramDeleteView,
    ProgramDetailView,
    ProgramListView,
    ProgramsHomeView,
    ProgramUpdateView,
    RunOnceProgramCreateView,
    PeriodicProgramCreateView,
    WeeklyProgramCreateView,
)

app_name = "programs"
urlpatterns = [
    path("", ProgramsHomeView.as_view(), name="home"),
    path("list/", ProgramListView.as_view(), name="list"),
    path("create/", ProgramCreateView.as_view(), name="create"),
    path("create/run-once/", RunOnceProgramCreateView.as_view(), name="create-run-once"),
    path("create/periodic/", PeriodicProgramCreateView.as_view(), name="create-periodic"),
    path("create/weekly/", WeeklyProgramCreateView.as_view(), name="create-weekly"),
    path("<int:id>/", ProgramDetailView.as_view(), name="detail"),
    path("<int:id>/update/", ProgramUpdateView.as_view(), name="update"),
    path("<int:id>/delete/", ProgramDeleteView.as_view(), name="delete"),
]
