"This is just an experimenting / debug file."

import math
from datetime import date, datetime, time

class Weather:
    def __init__(self):
        self.cloud_cover = None # percentage/100
        self.humidity = None # percentage/100
        self.pericip_intensity = None # mm/day
        self.pressure = None # kPa !!!
        self.solar_radiation = None # MJ/m2/day
        self.temperature = None # °C
        self.temperature_min = None
        self.temperature_max = None
        self.wind_speed = None # m/s
        self.longitude = None # decimal, 360-x if East of Greenwich
        self.longitude_tz_center = None # 360-x if East of Greenwich
        self.latitude = None # decimal
        self.elevation = None # m
        self.timestamp = None # UNIX timestamp

    def mean_temperature(self):
        #return (self.temperature_max + self.temperature_min) / 2
        return self.temperature

    def wind_speed_2m(self):
        return self.wind_speed

    def _isdaytime(self, omega):
        isdaytime = False
        if (omega > -math.pi/2 and omega < math.pi/2):
            isdaytime = True
        return isdaytime

    @property
    def reference_ET(self):
        "Penman-Monteith ET estimation, based on UF/IFAS AE45900"

        # Angstrom coefficients
        a_A = 0.28
        b_A = 0.45

        # 1.
        T_hr = self.temperature
        
        # 2.
        R_s = self.solar_radiation # MJ/m2/day

        # 3.
        u_2 = self.wind_speed_2m()

        # 4.
        Delta = 4096 * (0.6108 * math.exp( 17.27 * T_hr / (T_hr + 237.3)) / (T_hr + 237.3)**2)

        # 6.
        C_p = 1.013e-3 # MJ/kgK
        epsilon = 0.622
        _lambda = 2.45 # MJ/kg
        P = self.pressure # kPa 
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
        RH = self.humidity
        e_a = RH * e_s

        # 12.
        J = date.fromtimestamp(self.timestamp).timetuple().tm_yday
        d_r = 1 + 0.033 * math.cos(2 * math.pi * J / 365)
        delta = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)

        # 13.
        phi = math.pi / 180 * self.latitude

        # 14.
        omega_s = math.acos(-math.tan(phi) * math.tan(delta))

        # FAO hourly calculation
        L_z = self.longitude_tz_center
        L_m = self.longitude
        dt = datetime.fromtimestamp(self.timestamp)
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
            if R_s is None:
                # Angstrom equation FAO eq.35
                R_s = (a_A + b_A * (1 - self.cloud_cover)) * R_a
            
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
            sky_coefficient = 1 - (b_A * self.cloud_cover) / (a_A + b_A)
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


def weather_reference_1():
    weather = Weather()
    weather.temperature = 38 # °C
    weather.humidity = 0.52 # relative
    weather.wind_speed = 3.3 # m/s
    weather.solar_radiation = 2.450 # MJ/m2/hour
    weather.pressure = 101 # kPa !!!
    weather.cloud_cover = 0 # relative
    weather.longitude = -16.2500 # decimal
    weather.latitude = 16.2166 # decimal
    weather.elevation = 8 # m
    weather.timestamp = int(datetime(2019, 10, 1, 14, 30).timestamp())
    weather.longitude_tz_center = -15 # west north of Greenwich
    return weather

def weather_reference_2():
    weather = Weather()
    weather.temperature = 28 # °C
    weather.humidity = 0.90 # relative
    weather.wind_speed = 1.9 # m/s
    weather.solar_radiation = 0 # MJ/m2/hour
    weather.pressure = 101 # kPa !!!
    weather.cloud_cover = 0.3 # relative
    weather.longitude = -16.2500 # decimal
    weather.latitude = 16.2166 # decimal
    weather.elevation = 8 # m
    weather.timestamp = int(datetime(2019, 10, 1, 2, 30).timestamp())
    weather.longitude_tz_center = -15
    return weather

def test_reference_ET(weather, goal):
    ET_0 = weather.reference_ET
    error = abs(ET_0 - goal)
    if (error < 0.01):
        return True
    else:
        return False

def test_with_FAO_data():
    weather1 = weather_reference_1()
    goal1 = 0.63
    if (test_reference_ET(weather1, goal1) == True):
        print("FAO Test 1 OK")
    else:
        print("FAO Test 1 FAIL")

    weather2 = weather_reference_2()
    goal2 = 0.0
    if (test_reference_ET(weather2, goal2) == True):
        print("FAO Test 2 OK")
    else:
        print("FAO Test 2 FAIL")

def current_weather():
    weather = Weather()
    weather.temperature = 26 # °C
    weather.humidity = 0.2 # relative
    weather.wind_speed = 3.83 # m/s
    weather.solar_radiation = None # MJ/m2/hour
    weather.pressure = 100.51 # kPa !!!
    weather.cloud_cover = 0.2 # relative
    weather.longitude = 18.539 # decimal
    weather.latitude = 46.1616 # decimal
    weather.elevation = 200 # m
    weather.timestamp = int(datetime(2019, 10, 1, 2, 30).timestamp())
    weather.longitude_tz_center = 15 # decimal
    return weather
    
def main():
    #test_with_FAO_data()
    weather = current_weather()
    ET_0 = weather.reference_ET
    print(f"ET_0 = {ET_0}")

if __name__ == "__main__":
    main()