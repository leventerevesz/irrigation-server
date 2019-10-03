"""controller models"""

from django.db import models


class Controller(models.Model):
    "Microcontroller unit"
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=80, blank=True, default="")
    description = models.TextField(blank=True, default="")
    channel_count = models.PositiveSmallIntegerField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.id}) {self.name}"


class Channel(models.Model):
    "Channel on a microcontroller"
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=80, blank=True, default="")
    description = models.TextField(blank=True, default="")
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE)
    channel_no = models.PositiveSmallIntegerField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.id}) {self.name}"
