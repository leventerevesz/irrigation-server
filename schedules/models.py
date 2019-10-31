from django.db import models

# Create your models here.

## REQURED_SCHEDULE
# Foreign Key Program
#  - Foreign Key Channel
# Start date, time
# Duration

class RequestedRun(models.Model):
    program = models.ForeignKey("programs.Program", on_delete=models.CASCADE)
    zone = models.ForeignKey("zones.Zone", on_delete=models.CASCADE) # must register a req for each zone in the program
    start = models.DateTimeField()
    duration = models.DurationField()

    def __str__(self):
        return f"({self.id}) Z{self.zone.id} {self.start}"


class ScheduledRun(models.Model):
    program = models.ForeignKey("programs.Program", on_delete=models.CASCADE)
    zone = models.ForeignKey("zones.Zone", on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = models.DurationField()
    progress = models.FloatField()

