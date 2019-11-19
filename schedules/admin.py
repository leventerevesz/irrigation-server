from django.contrib import admin

from .models import RequestedRun, ScheduledRun, Action

class RequestedRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'program', 'zone', 'start', 'duration', 'priority')

class ScheduledRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'start', 'duration', 'progress')

class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', 'channel', 'topic', 'command', 'done')

    def topic(self, action):
        return f"{action.channel.topic}"

admin.site.register(RequestedRun, RequestedRunAdmin)
admin.site.register(ScheduledRun, ScheduledRunAdmin)
admin.site.register(Action, ActionAdmin)