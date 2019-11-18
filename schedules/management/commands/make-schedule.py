from datetime import datetime, date, time, timedelta

from django.core.management.base import BaseCommand, CommandError
from programs.models import Program
from home.models import Settings
from schedules.models import RequestedRun, ScheduledRun
from weather.models import WeatherRecord, TankRecord

class Command(BaseCommand):
    help = "Creates a scheduled run from requests"

    def add_arguments(self, parser):
        parser.add_argument("--date", help="the day to make the schedule for. YYYY-MM-DD")
    
    def get_date(self, datestr):
        if datestr is None:
            thedate = date.today()
        else:
            thedate = date.fromisoformat(datestr)
        return thedate

    def handle(self, *args, **options):
        thedate = self.get_date(options.get("date"))
        firstdt = datetime.combine(thedate, time(0,0,0))
        lastdt = firstdt + timedelta(hours=24)

        requests = RequestedRun.objects.filter(start__gt=firstdt, start__lt=lastdt).order_by('start')
        weather_records = WeatherRecord.objects.filter(datetime__gte=firstdt, datetime__lt=lastdt)

        if (not requests.exists()):
            self.stderr.write("No requests.")
            return

        # Adapt to weather
        cumulative_reference_ET = sum([record.reference_ET for record in weather_records])
        cumulative_precipitation = sum([record.precipitation for record in weather_records])

        requests_adapted_to_weather = []
        for request in requests:
            adapted_request = self.adapt_to_weather(request, cumulative_reference_ET, cumulative_precipitation)
            if adapted_request is not None:
                requests_adapted_to_weather.append(adapted_request)


        # Adapt to water quota
        # stored_water = self.get_stored_water(thedate)
        requested_water = self.requested_water(requests)
        
        #TODO calculate daily water quota
        water_quota = 2

        requests_adapted_to_quota = []
        if (requested_water < water_quota):
            for request in requests_adapted_to_weather:
                requests_adapted_to_quota.append(request)
        else:
            minimum_water = self.minimum_water_need(requests_adapted_to_weather)
            neccessary_requested_water = self.neccessary_requested_water_need(requests_adapted_to_weather)

            if (neccessary_requested_water < water_quota):
                shortening_factor = 0
            elif (minimum_water < water_quota):
                shortening_factor = (neccessary_requested_water - water_quota) / (neccessary_requested_water - minimum_water)
            else:
                self.stderr.write(
                    f"Exceeding water quota. Quota: {water_quota}, "
                    f"Minimum irrigation: {minimum_water}."
                )
                shortening_factor = 1

            for request in requests_adapted_to_weather:
                adapted = self.shorten_based_on_priority(request, shortening_factor)
                requests_adapted_to_quota.append(adapted)

        # Scheduling
        breakpoint()
        if (len(requests_adapted_to_quota) == 0):
            self.stderr.write(f"Only low priority requests, skipping all.")
            return

        firstrequestdt = requests[0].start
        earlierschedules = ScheduledRun.objects.filter(start__lt=firstrequestdt)
        if (earlierschedules.exists()):
            record = earlierschedules.latest("start")
            lastscheduleddt = record.start + record.duration
        else:
            lastscheduleddt = firstrequestdt
        possible_begin = max(firstrequestdt, lastscheduleddt)

        for request in requests_adapted_to_quota:
            start = max(request.start, possible_begin)
            obj = ScheduledRun.objects.create(
                request=request,
                start=start,
                duration=request.duration
            )
            obj.save()
            possible_begin = start + request.duration

    def shorten_based_on_priority(self, request, shortening_factor):
        if (request.program.priority <= 3):
            request.duration = request.duration
        elif (request.program.priority <= 5):
            request.duration = request.duration * (1 - 0.3 * shortening_factor)
        elif (request.program.priority <= 8):
            request.duration = request.duration * (1 - 0.5 * shortening_factor)
        else:
            request = None

        # round to seconds
        request.duration = self.round_timedelta(request.duration)

        return request

    def round_timedelta(self, td):
        return timedelta(seconds=td.seconds)

    def adapt_to_weather(self, request, cumulative_reference_ET, cumulative_precipitation):
        cumulatice_ET = cumulative_reference_ET * request.zone.plant_coefficient

        # This is a very basic model
        water_need = cumulatice_ET - cumulative_precipitation

        if (request.program.adaptivity == "bypass"):
            treshold = 0.5 # mm
            if (water_need > treshold):
                return request
            else:
                return None

        elif (request.program.adaptivity == "ET"):
            intensity = request.zone.intensity
            programmed_duration = request.duration
            programmed_irrigation = programmed_duration.seconds / 3600 * intensity
            
            adapted_duration = timedelta(hours=(water_need / intensity))
            requested_duration = self.limit_duration(programmed_duration, adapted_duration)
            request.duration = self.round_timedelta(requested_duration)

            return request
        
        else: # adaptivity="none"
            return request

    def limit_duration(self, programmed_duration, adapted_duration):
        lower_bound = 0.5 * programmed_duration
        upper_bound = 1.5 * programmed_duration

        if (adapted_duration < lower_bound):
            duration = lower_bound
        elif (adapted_duration > upper_bound):
            duration = upper_bound
        else:
            duration = adapted_duration

        return duration

    def get_stored_water(self, thedate):
        tank_record_query = TankRecord.objects.filter(datetime__date=thedate)
        settings = Settings.objects.get(pk=1)

        if (tank_record_query.exists()):
            tank_record = tank_record_query.earliest("datetime")
            stored_water = tank_record.level * settings.tank_capacity
        else: 
            self.stderr.write(f"Cannot find tank record for the given day: {thedate}")
            stored_water = 0.5 * settings.tank_capacity
        
        return stored_water

    def requested_water(self, requests):
        total_usage = 0
        for request in requests:
            usage = request.zone.flow_rate * (request.duration.seconds / 3600)
            total_usage += usage
        return total_usage

    def neccessary_requested_water_need(self, requests):
        "Total water need of non-skippable requests"
        water_need = 0
        for request in requests:
            requested_irrigation = request.zone.flow_rate * (request.duration.seconds / 3600)
            if (request.program.priority <= 8):
                water_need += requested_irrigation

        return water_need

    def minimum_water_need(self, requests):
        "Minimum total water need with skipping and shortening"
        water_need = 0
        for request in requests:
            requested_irrigation = request.zone.flow_rate * (request.duration.seconds / 3600)
            if (request.program.priority <= 3):
                water_need += requested_irrigation
            elif (request.program.priority <= 5):
                water_need += requested_irrigation * (1 - 0.3)
            elif (request.program.priority <= 8):
                water_need += requested_irrigation * (1 - 0.5)

        return water_need