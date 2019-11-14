from datetime import datetime, date, time
import math

import darksky

class WeatherConditions():
    "Interface for DarkSky API data"
    def __init__(self, data):
        self.time = data.time
        self.temperature = data.temperature
        self.wind_speed = data.windSpeed
        self.humidity = data.humidity
        self.pressure = data.pressure / 10 # kPa
        self.cloud_cover = data.cloudCover


class Weather():
    def __init__(self, apikey, latitude, longitude, longitude_tzcenter, elevation):
        self.apikey = apikey
        self.latitude = latitude
        self.longitude = longitude
        self.longitude_tzcenter = longitude_tzcenter
        self.elevation = elevation

        self.forecast = darksky.forecast(self.apikey, self.latitude, self.longitude, units="si")

    def _isdaytime(self, omega):
        isdaytime = False
        if (omega > -math.pi/2 and omega < math.pi/2):
            isdaytime = True
        return isdaytime

    def hourly_reference_ET(self, weather_conditions):
        """ 
        Penman-Monteith ET estimation
        based on UF/IFAS AE45900 and http://www.fao.org/3/X0490E/x0490e07.htm
        """

        # Angstrom coefficients
        a_A = 0.28
        b_A = 0.45

        # 1.
        T_hr = weather_conditions.temperature
        
        # 2. (May be implemented later)
        # R_s = None # MJ/m2/day

        # 3.
        u_2 = weather_conditions.wind_speed

        # 4.
        Delta = 4096 * (0.6108 * math.exp( 17.27 * T_hr / (T_hr + 237.3)) / (T_hr + 237.3)**2)

        # 6.
        C_p = 1.013e-3 # MJ/kgK
        epsilon = 0.622
        _lambda = 2.45 # MJ/kg
        P = weather_conditions.pressure # kPa 
        gamma = C_p * P / (epsilon * _lambda)

        # 7.
        DT = Delta / (Delta + gamma * (1 + 0.34 * u_2))

        # 8.
        PT = gamma / (Delta + gamma * (1 + 0.34 * u_2))

        # 9.
        # modified
        TT = (37 / (T_hr + 273)) * u_2

        # 10.
        e_s = 0.6108 * math.exp(17.27 * T_hr / (T_hr + 237.3))

        # 11.
        RH = weather_conditions.humidity
        e_a = RH * e_s

        # 12.
        J = date.fromtimestamp(weather_conditions.time).timetuple().tm_yday
        d_r = 1 + 0.033 * math.cos(2 * math.pi * J / 365)
        delta = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)

        # 13.
        phi = math.pi / 180 * self.latitude

        # 14.
        omega_s = math.acos(-math.tan(phi) * math.tan(delta))

        # FAO hourly calculation
        L_z = self.longitude_tzcenter
        L_m = self.longitude
        dt = datetime.fromtimestamp(weather_conditions.time)
        t = dt.hour + dt.minute / 60
        b = 2 * math.pi * (J - 81) / 364
        S_c = 0.1645 * math.sin(2 * b) - 0.1255 * math.cos(b) - 0.025 * math.sin(b)
        omega = math.pi / 12 * ((t + 0.06667 * (L_m - L_z) + S_c) - 12)
        omega_1 = omega - math.pi * 1 / 24
        omega_2 = omega + math.pi * 1 / 24
        N = 24 / math.pi * omega_s

        if (self._isdaytime(omega)):
            # 15.
            # R_a from FAO
            G_sc = 0.0820 # MJ/m2/min
            R_a = 12 * 60 / math.pi * G_sc * d_r * (
                (omega_2 - omega_1) * math.sin(phi) * math.sin(delta) +
                math.cos(phi) * math.cos(delta) * (math.sin(omega_2) - math.sin(omega_1)))
            
            # 2. if solar radiation is not measured
            # Angstrom equation FAO eq.35
            R_s = (a_A + b_A * (1 - weather_conditions.cloud_cover)) * R_a
            
            # 16.
            R_so = (0.75 + 2e-5 * self.elevation) * R_a
            sky_coefficient = R_s / R_so

            # 17.
            a = 0.23 # albedo coefficient, a_grass = 0.23
            R_ns = (1 - a) * R_s

            # 19.1
            G_coefficient = 0.1
        
        else: # nighttime
            R_ns = 0
            sky_coefficient = 1 - (b_A * weather_conditions.cloud_cover) / (a_A + b_A)
            G_coefficient = 0.5

        # 18.
        sigma = 4.903e-9 / 24
        R_nl = sigma * (T_hr + 273.16)**4 * \
            (0.34 - 0.14 * math.sqrt(e_a)) * (1.35 * sky_coefficient - 0.35)        
        
        # 19.2
        R_n = R_ns - R_nl
        G = G_coefficient * R_n
        R_ng = 0.408 * (R_n - G)

        # FS1.
        ET_rad = DT * R_ng

        # FS2. 
        ET_wind = PT * TT * (e_s - e_a)

        # Final
        ET_0 = ET_wind + ET_rad
        return ET_0
    
    @property
    def current_hourly_reference_ET(self):
        weather_conditions = WeatherConditions(self.forecast)
        return self.hourly_reference_ET(weather_conditions)


if __name__ == "__main__":
    APIKEY = "8b16caa53b6dac44cd9654f4fbb55b57"
    LATITUDE = 46.1616
    LONGITUDE = 18.3514

    weather = Weather(APIKEY, 46.1616, 18.3514, 15, 200)
    ET_0 = weather.current_hourly_reference_ET
    print(ET_0)