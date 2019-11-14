from django.db import models


class RequestedRun(models.Model):
    program = models.ForeignKey("programs.Program", on_delete=models.CASCADE)
    zone = models.ForeignKey("zones.Zone", on_delete=models.CASCADE) # must register a req for each zone in the program
    start = models.DateTimeField()
    duration = models.DurationField()
    priority = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"({self.id}) [{self.program.id}] {self.program.name} - [{self.zone.id}] {self.zone.name} @ {self.start}"


class ScheduledRun(models.Model):
    request = models.ForeignKey("schedules.RequestedRun", on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = models.DurationField()
    progress = models.FloatField(default=0)

    def __str__(self):
        return f"({self.id}) request:[{self.request.id}] - [{self.request.zone.id}] {self.request.zone.name} @ {self.start}"

class Action(models.Model):
    schedule = models.ForeignKey("schedules.ScheduledRun", on_delete=models.CASCADE)
    channel = models.ForeignKey("controllers.Channel", on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    command = models.CharField(max_length=25)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.id}) channel:[{self.channel.id}] command: {self.command} @ {self.datetime}"