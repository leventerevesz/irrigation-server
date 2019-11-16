from io import StringIO
from datetime import datetime, date, time

from django.core.management import call_command
from django.test import TestCase

from weather.models import WeatherRecord, TankRecord
from weather.WeatherAPI import Weather


class DummyForecast():
    def __init__(self, time, temperature, windSpeed, humidity, pressure, 
            cloudCover, precipIntensity, precipProbability):
        self.time = time
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.windSpeed = windSpeed
        self.cloudCover = cloudCover
        self.precipIntensity = precipIntensity
        self.precipProbability = precipProbability


class Location():
    def __init__(self, latitude, longitude, longitude_tzcenter, elevation):
        self.latitude = latitude
        self.longitude = longitude
        self.longitude_tzcenter = longitude_tzcenter
        self.elevation = elevation 


class ReferenceETCalculationTestCase(TestCase):
    """ Test if the ET calculation formula gives correct results for the example
        cases defined in FAO56.
    """
        
    def get_FAO_location(self):
        loc = Location(
            latitude = 16.2166,
            longitude = -16.2500,
            longitude_tzcenter = -15,
            elevation = 8
        )
        return loc

    def test_FAO_example_1(self):
        loc = self.get_FAO_location()

        test_forecast = DummyForecast(
            time=int(datetime(2019, 10, 1, 14, 30).timestamp()),
            temperature=38,
            humidity=0.52,
            pressure=1010, # hPa because Dar Sky uses this as well
            windSpeed=3.3,
            # Solar radiation (R_s) = 2.450 -- this is set with cloudCover instead.
            cloudCover=0.08, # Depends on Angstrom constants!!!
            precipIntensity=0,
            precipProbability=0
        )
        ET_goal = 0.63

        weather = Weather("", loc.latitude, loc.longitude, loc.longitude_tzcenter, loc.elevation, test_forecast)
        ET = weather.current_hourly_reference_ET

        error = ET_goal - ET
        self.assertLess(error, 0.01)
    
    def test_FAO_example_2(self):
        loc = self.get_FAO_location()

        test_forecast = DummyForecast(
            time=int(datetime(2019, 10, 1, 2, 30).timestamp()),
            temperature=28,
            humidity=0.90,
            pressure=1010, # hPa because Dar Sky uses this as well
            windSpeed=1.9,
            cloudCover=0.3, # Depends on Angstrom constants!!!
            precipIntensity=0,
            precipProbability=0
        )
        ET_goal = 0.0

        weather = Weather("", loc.latitude, loc.longitude, loc.longitude_tzcenter, loc.elevation, test_forecast)
        ET = weather.current_hourly_reference_ET

        error = ET_goal - ET
        self.assertLess(error, 0.01)
