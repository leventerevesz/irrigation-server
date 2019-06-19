"""Main views for the site"""

from django.shortcuts import render
from django.views import View


class DashboardView(View):
    "Dashboard"
    template_name = "home/home.html"

    def get(self, request, *args, **kwargs):
        "GET request handler"
        context = {
            "pagetitle": "Dashboard"
        }
        return render(request, self.template_name, context)


class AboutView(View):
    "About page"
    template_name = "home/about.html"

    def get(self, request, *args, **kwargs):
        "GET request handler"
        context = {
            "pagetitle": "About"
        }
        return render(request, self.template_name, context)
