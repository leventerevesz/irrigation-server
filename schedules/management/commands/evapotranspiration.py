import math
from datetime import date

class Weather:
    def __init__(self):
        self.cloud_cover = None # percentage/100
        self.humidity = None # percentage/100
        self.pericip_intensity = None # mm/hour
        self.pressure = None # kPa !!!
        self.solar_radiation = None # MJ/m2/hour
        self.temperature = None # °C
        self.temperature_min = None
        self.temperature_max = None
        self.wind_speed = None # m/s
        self.longitude = None # decimal
        self.latitude = None # decimal
        self.elevation = None # m

    def mean_temperature(self):
        return self.temperature

    def wind_speed_2m(self):
        return self.wind_speed

    @property
    def reference_ET(self):
        "Penman-Monteith ET estimation, based on UF/IFAS AE45900"

        # 2.
        # Mean daily solar radiation
        R_s = self.solar_radiation # MJ/m2/hour

        # 4.
        Tmean = self.mean_temperature()
        delta = 4096 * (0.6108 * math.exp( 17.27 * Tmean / (Tmean + 273.3)) / (Tmean + 273.3)**2)

        # 6.
        C_p = 1.013e-3 # MJ/kgK
        epsilon = 0.622
        _lambda = 2.45 # MJ/kg
        gamma = C_p * self.pressure / (epsilon * _lambda)

        # 7.
        u_2 = self.wind_speed_2m()
        DT = delta / (delta + gamma * (1 + 0.34 * u_2))

        # 8.
        PT = gamma / (delta + gamma * (1 + 0.34 * u_2))

        # 9.
        # modified
        TT = (900 / 24 / (Tmean + 273.3)) * u_2

        # 10.
        # modified
        T_min, T_max = Tmean, Tmean
        e_Tmin = 0.6108 * math.exp(17.27 * T_min / (T_min + 273.3))
        e_Tmax = 0.6108 * math.exp(17.27 * T_max / (T_max + 273.3))
        e_s = (e_Tmin + e_Tmax) / 2

        # 11.
        RH = self.humidity
        e_a = RH / 100 * ((e_Tmin + e_Tmax) / 2)

        # 12.
        J = date.today().timetuple().tm_yday
        d_r = 1 + 0.033 * math.cos(2 * math.pi * J / 365)
        _delta = 0.409 * math.sin(2 * math.pi * J / 365 - 1.39)

        # 13.
        phi = math.pi / 180 * self.latitude

        # 14.
        omega_s = math.acos(-math.tan(phi) * math.tan(_delta))

        # 15.
        # modified
        G_sc = 0.0820 # MJ/m2/min
        R_a = 60 / math.pi * G_sc * d_r * \
            (omega_s * math.sin(phi) * math.sin(_delta) + math.cos(phi) * math.cos(_delta) * math.sin(omega_s))
        
        # 16.
        R_so = (0.75 + 2e-5 * self.elevation) * R_a

        # 17.
        a = 0.23 # albedo coefficient, a_grass = 0.23
        R_ns = (1 - a) * R_s

        # 18.
        # modified
        sigma = 4.903e-9 / 24
        R_nl = sigma * ((T_max + 273.16)**4 + (T_min + 273.16)**4) / 2 * \
            (0.34 - 0.14 * math.sqrt(e_a)) * (1.35 * R_s / R_so - 0.35)
        
        # 19.
        R_n = R_ns - R_nl
        R_ng = 0.408 * R_n

        # FS1.
        ET_rad = DT * R_ng

        # FS2. 
        ET_wind = PT * TT * (e_s - e_a)

        # Final
        ET_0 = ET_wind + ET_rad
        breakpoint()
        return ET_0

        

def main():
    weather = Weather()
    weather.cloud_cover = 0.7
    weather.humidity = 0.78
    weather.pericip_intensity = 0.2
    weather.pressure = 101
    weather.temperature = 19
    weather.wind_speed = 0.8
    weather.cloud_cover = 0.2 # percentage/100
    weather.humidity = 0.78 # percentage/100
    weather.pericip_intensity = 0.01 # mm/hour
    weather.pressure = 101 # kPa !!!
    weather.solar_radiation = 380 * 3.6e-3 # MJ/m2/hour
    weather.temperature = 24 # °C
    weather.temperature_min = 9
    weather.temperature_max = 25
    weather.wind_speed = 2 # m/s
    weather.longitude = 18.350610 # decimal
    weather.latitude = 46.161686 # decimal
    weather.elevation = 200 # m

    ET_0 = weather.reference_ET
    print(f"ET_0 = {ET_0}")

if __name__ == "__main__":
    main()