from django.contrib import admin

from .models import RequestedRun, ScheduledRun, Action

class RequestedRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'program', 'zone', 'start_iso', 'duration', 'priority')

    def start_iso(self, requestedrun):
        return requestedrun.start.strftime("%Y-%m-%d %H:%M:%S")
    start_iso.short_description = "start"

class ScheduledRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'start_iso', 'duration', 'progress')

    def start_iso(self, scheduledrun):
        return scheduledrun.start.strftime("%Y-%m-%d %H:%M:%S")
    start_iso.short_description = "start"

class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'schedule_id', 'datetime_iso', 'channel', 'topic', 'command', 'done')

    def schedule_id(self, action):
        return f"{action.schedule.id}"

    def datetime_iso(self, action):
        return action.datetime.strftime("%Y-%m-%d %H:%M:%S")

    def topic(self, action):
        return f"{action.channel.topic}"

admin.site.register(RequestedRun, RequestedRunAdmin)
admin.site.register(ScheduledRun, ScheduledRunAdmin)
admin.site.register(Action, ActionAdmin)