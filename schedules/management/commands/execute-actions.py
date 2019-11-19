from datetime import datetime, date, time, timedelta
from threading import Timer

from django.core.management.base import BaseCommand, CommandError

from home.models import Settings
from schedules.models import Action

from irrigation import mqtt

class Command(BaseCommand):
    help = "Execute actions scheduled for the next 1 minute"

    def add_arguments(self, parser):
        parser.add_argument("--datetime", help="Date and time in ISO format. YYYY-MM-DDTHH:MM:SS")
    
    def get_datetime(self, datetimestr):
        if datetimestr is None:
            thedatetime = datetime.now()
        else:
            thedatetime = datetime.fromisoformat(datetimestr)
        return thedatetime

    def handle(self, *args, **options):
        time_begin = self.get_datetime(options.get("datetime"))
        time_end = time_begin + timedelta(minutes=1)

        actions = Action.objects.filter(datetime__gte=time_begin, datetime__lt=time_end)
        #breakpoint()
        
        for action in actions:
            delay = (action.datetime - time_begin).seconds
            t = Timer(delay, self.execute_action, [action])
            t.start()
    
    def execute_action(self, action):
        topic = "/commands/" + action.channel.topic
        data = action.command
        self.stdout.write(f"Executing action {action.id}: topic: {topic} data: {data}")
        mqtt.client.publish(topic, data, qos=1)