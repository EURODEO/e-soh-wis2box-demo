import random

from locust import HttpUser, between, task


stations = ['0-20000-0-06201', '0-20000-0-06207', '0-20000-0-06215', '0-20000-0-06225', '0-20000-0-06257', '0-20000-0-06260', '0-20000-0-06269']
parameters = ['air_temperature', 'wind_direction', 'wind_speed', 'pressure_reduced_to_mean_sea_level', 'relative_humidity']


class Wis2Box(HttpUser):
    # wait_time = between(0, 1)


    @task
    def feature(self):
        id = random.choice(stations)
        parameter = random.choice(parameters)
        headers = {"accept-encoding": "br,gzip"}
        url = f"""/oapi/collections/urn:x-wmo:md:nld:knmi_esoh_demo:surface-weather-observations/items?f=json&name={parameter}&wigos_station_identifier={id}&sortby=-resultTime&limit=1000&datetime=2023-02-01T00%3A00%3A00Z%2F2023-03-10T00%3A00%3A00Z"""
        self.client.get(url, headers=headers, name="/collections/obs/items?")
