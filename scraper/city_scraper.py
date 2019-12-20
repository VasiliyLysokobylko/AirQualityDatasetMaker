import os
from cityair_api import CityAirRequest, Period


class City:
    def __init__(self, login, password):
        self.login = login
        self.password = password


class DataScraper:
    def __init__(self, output_path: str):
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.mkdir(output_path)

    def scrap_all_cities(self, cities: list):
        for city in cities:
            self.scrap_city(city)

    def scrap_city(self, city: City):
        city_output_path = os.path.join(self.output_path, city.login)
        r = CityAirRequest(city.login, city.password)
        stations = r.get_stations()
        for station_id in stations:
            output_file = city_output_path + '_station_' + str(station_id) + '.csv'
            df = r.get_station_data(station_id=station_id, period=Period.HOUR)
            df.to_csv(output_file, sep='\t', encoding='utf-8')
