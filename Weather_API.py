import requests
import json

class Weather():
    def __init__(self, APPID=None, POLYID=None):
        self.APPID = APPID
        self.POLYID = POLYID
    
    def get_current_weather(self):
        """ Gets current weather data from the Agro Weather API, returns the data in a dict. """
        api_endpoint = "http://api.agromonitoring.com/agro/1.0/weather?appid={APPID}&polyid={POLYID}".format(
            APPID=self.APPID, POLYID=self.POLYID)
        response = requests.get(url=api_endpoint)
        weather_data = json.loads(response.text)
        return weather_data
    
    def get_soil_data(self):
        """ Gets current soil data from the Agro Soil API, returns the data in a dict. """
        api_endpoint = "http://api.agromonitoring.com/agro/1.0/soil?appid={APPID}&polyid={POLYID}".format(
            APPID=self.APPID, POLYID=self.POLYID)
        response = requests.get(url=api_endpoint)
        soil_data = json.loads(response.text)
        return soil_data
    
    def create_polygon(self, polygon_json):
        """ Creates a new polygon from the supported GeoJSON data, and sets it as 
            default for this Weather instance. Returns the response data in a dict.
        
            polygon_json: GeoJSON representation of the polygon
        """
        api_endpoint = "http://api.agromonitoring.com/agro/1.0/polygons?appid={APPID}".format(
            APPID=self.APPID)
        response = requests.post(url=api_endpoint, json=polygon_json)
        response_data = json.loads(response.text)
        _set_created_polygon(response_data)
        return response_data

    def _set_created_polygon(self, response_data):
        poly_id = response_data.get("id")
        if poly_id is not None:
            self.POLYID = poly_id



if __name__ == "__main__":
    APPID = "d9a5161cce486ab8a4a866e48edf9b9f"
    POLYID = "5d97212fae8d9e0013fc164d"   # Hetenytuja

    weather = Weather(APPID=APPID, POLYID=POLYID)

    cw = weather.get_current_weather()
    print(cw)
