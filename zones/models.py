from django.db import models


class Zone(models.Model):
    "Irrigation zone"
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=80, blank=True, default="")
    description = models.TextField(blank=True, default="")
    channels = models.ManyToManyField("controllers.Channel", blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.id}) {self.name}"