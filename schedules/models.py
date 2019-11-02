from django.db import models


class RequestedRun(models.Model):
    program = models.ForeignKey("programs.Program", on_delete=models.CASCADE)
    zone = models.ForeignKey("zones.Zone", on_delete=models.CASCADE) # must register a req for each zone in the program
    start = models.DateTimeField()
    duration = models.DurationField()

    def __str__(self):
        return f"({self.id}) [{self.program.id}] {self.program.name} - [{self.zone.id}] {self.zone.name} @ {self.start}"


class ScheduledRun(models.Model):
    program = models.ForeignKey("programs.Program", on_delete=models.CASCADE)
    zone = models.ForeignKey("zones.Zone", on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = models.DurationField()
    progress = models.FloatField()

