import requests
import json
from datetime import datetime, timedelta

APPID = "d9a5161cce486ab8a4a866e48edf9b9f"
POLYID = "5d97212fae8d9e0013fc164d"   # Hetenytuja
#POLYID = "5d971a14eb408b0007146877"  #example

def set_polygon():
    API_ENDPOINT = "http://api.agromonitoring.com/agro/1.0/polygons?appid={APPID}".format(
        APPID=APPID)
    poly_json = {
        "name": "Hetenytuja",
        "geo_json": {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [18.350199, 46.161538],
                        [18.351974, 46.161947],
                        [18.352296, 46.161285],
                        [18.350456, 46.160906],
                        [18.350199, 46.161538]
                    ]
                ]
            }
        }
    }
    response = requests.post(url=API_ENDPOINT, json=poly_json)
    print("======== RESPONSE ==========")
    print(response.text)


def get_current_weather():
    API_ENDPOINT = "http://api.agromonitoring.com/agro/1.0/weather?appid={APPID}&polyid={POLYID}".format(
        APPID=APPID, POLYID=POLYID)

    response = requests.get(url=API_ENDPOINT)
    current_weather = json.loads(response.text)
    return current_weather

def get_soil_data():
    API_ENDPOINT = "http://api.agromonitoring.com/agro/1.0/soil?appid={APPID}&polyid={POLYID}".format(
        APPID=APPID, POLYID=POLYID)
    response = requests.get(url=API_ENDPOINT)
    soil_data = json.loads(response.text)
    return soil_data

def get_prec_last_24_h():
    start = int(datetime.now().timestamp())
    end = int((datetime.now() - timedelta(hours=24)).timestamp())
    API_ENDPOINT = "http://api.agromonitoring.com/agro/1.0/weather/history/accumulated_precipitation?polyid={POLYID}&start={START}&end={END}&threshold=284&appid={APPID}".format(
        APPID=APPID, POLYID=POLYID, START=start, END=end
    )
    response = requests.get(url=API_ENDPOINT)
    prec = json.loads(response.text)
    return prec

if (__name__ == "__main__"):
    r = get_soil_data()
    print(r)
    r = get_current_weather()
    print(r)
    r = get_prec_last_24_h()
    print(r)
