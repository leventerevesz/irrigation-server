from django.db import models


class Zone(models.Model):
    "Irrigation zone"
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=80, blank=True, default="")
    description = models.TextField(blank=True, default="")
    plant_coefficient = models.FloatField(default=1)
    channels = models.ManyToManyField("controllers.Channel", blank=True)
    intensity = models.FloatField(default=5)
    flow_rate = models.FloatField(default=1) # m3/h
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.id}) {self.name}"