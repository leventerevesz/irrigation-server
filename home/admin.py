from django.contrib import admin

from .models import Settings, Log

class LogAdmin(admin.ModelAdmin):
    list_display = ('message', 'datetime')

admin.site.register(Settings)
admin.site.register(Log, LogAdmin)