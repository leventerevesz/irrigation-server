from django.contrib import admin

from .models import RequestedRun, ScheduledRun

# Register your models here.

admin.site.register(RequestedRun)
admin.site.register(ScheduledRun)
