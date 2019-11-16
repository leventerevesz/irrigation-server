from datetime import datetime, date, time, timedelta

from django.core.management.base import BaseCommand, CommandError

from weather.models import WeatherRecord
from weather.Weather import Weather

#TODO:
#    - Read location settings from database

class Command(BaseCommand):
    help = "update weather forecast"

    def handle(self, *args, **options):
        APIKEY = "8b16caa53b6dac44cd9654f4fbb55b57"
        weather = Weather(APIKEY, 46.1616, 18.3514, 15, 200)

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
