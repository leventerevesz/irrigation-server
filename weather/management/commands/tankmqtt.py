from weather.models import TankRecord
from django.utils import timezone

def save_tanklevel(message):
    datetime = timezone.now()
    level = float(message)
    record = TankRecord.objects.create(datetime=datetime, level=level)
    record.save()