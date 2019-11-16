from datetime import datetime, date, time, timedelta

from django.core.management.base import BaseCommand, CommandError

from home.models import Settings

from weather.models import WeatherRecord
from weather.WeatherAPI import Weather


#TODO:
#    - Read location settings from database

class Command(BaseCommand):
    help = "update weather forecast"

    def handle(self, *args, **options):
        settings = Settings.objects.get(pk=1)

        weather = Weather(
            settings.weather_api_key,
            settings.site_latitude,
            settings.site_longitude,
            settings.tzcenter_longitude, 
            settings.site_elevation
        )

        weather_forecast = weather.reference_ET_precipitation_forecast
        
        first_dt = weather_forecast[0]["datetime"]
        future_records = WeatherRecord.objects.filter(datetime__gte=first_dt)
        future_records.delete()

        for record in weather_forecast:
            obj = WeatherRecord.objects.create(
                datetime=record["datetime"], 
                reference_ET=record["ET"], 
                precipitation=record["precipitation"]
            )
            obj.save()
