from django.db import models


class WeatherRecord(models.Model):
    datetime = models.DateTimeField()
    precipitation = models.FloatField()
    reference_ET = models.FloatField()

    def __str__(self):
        return f"({self.id}) @ {self.datetime} - ET: {self.reference_ET:.3f} Precip: {self.precipitation:.3f}"


class TankRecord(models.Model):
    datetime = models.DateTimeField()
    level = models.FloatField()

    def __str__(self):
        return f"({self.id}) @ {self.datetime} - {self.level:.3f}"