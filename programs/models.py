"""programs models"""

from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Program(models.Model):
    "Irrigation program"
    PROGRAM_TYPES = [
        ("run-once", "Run Once"),
        ("periodic", "Periodic"),
        ("weekly", "Weekly"),
    ]
    DAYS_OF_WEEK = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday")
    ]

    name = models.CharField(max_length=80)
    description = models.TextField(blank=True, default="")
    program_type = models.CharField(
        max_length=16,
        choices=PROGRAM_TYPES,
        default="run-once"
    )
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    days_of_week = models.CharField(max_length=25, default="")
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    period = models.DurationField(blank=True, null=True)
    priority = models.PositiveSmallIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"({self.id}) {self.name}"

    def get_absolute_url(self):
        "Return the url of the detail view"
        return reverse("programs:detail", kwargs={"id": self.id})
