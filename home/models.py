from django.db import models


class Settings(models.Model):
    weather_api_key = models.CharField(max_length=64)
    site_latitude = models.FloatField()
    site_longitude = models.FloatField()
    site_elevation = models.FloatField()
    tzcenter_longitude = models.FloatField()
    
    mqtt_user = models.CharField(max_length=32)
    mqtt_password = models.CharField(max_length=32)

    tank_capacity = models.FloatField()
    