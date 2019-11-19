from django.contrib import admin

from .models import WeatherRecord, TankRecord

class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'formatted_precipitation', 'formatted_reference_ET')

    def formatted_precipitation(self, record):
        return f"{record.precipitation:.4f}"
    formatted_precipitation.short_description = "Hourly Precipitation"

    def formatted_reference_ET(self, record):
        return f"{record.reference_ET:.4f}"
    formatted_reference_ET.short_description = "Hourly Reference ET"

class TankRecordAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'level')

admin.site.register(WeatherRecord, WeatherRecordAdmin)
admin.site.register(TankRecord, TankRecordAdmin)