from django.contrib import admin

from .models import RequestedRun, ScheduledRun, Action

# Register your models here.

admin.site.register(RequestedRun)
admin.site.register(ScheduledRun)
admin.site.register(Action)