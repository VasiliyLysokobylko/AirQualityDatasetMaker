import os
import json
from cityair_api import CityAirRequest, Period


class User:
    def __init__(self, login, password):
        self.login = login
        self.password = password


class DataScraper:
    def __init__(self, user: User, output_path: str):
        self.output_path = output_path
        self.user: User = user
        self.city_air_api = CityAirRequest(self.user.login, self.user.password)
        if not os.path.exists(output_path):
            os.mkdir(output_path)

    def scrap_all_cities(self):
        for location in self.city_air_api.get_locations():
            self.scrap_city(location)

    def scrap_city(self, city):
        city_output_path = os.path.join(self.output_path, city['name'])
        if 'stations' not in city or city['stations'] is None:
            print("Empty city: " + json.dumps(city, indent=4))
            return
        with open(city_output_path + '.json', 'w') as cf:
            cf.write(json.dumps(city, indent=4))
        for station in city['stations']:
            output_file = city_output_path + '_station_' + str(station['id']) + '.csv'
            output_json_file = city_output_path + '_station_' + str(station['id']) + '.json'
            with open(output_json_file, 'w') as f:
                f.write(json.dumps(station, indent=4))
            df = self.city_air_api.get_station_data(station_id=station['id'], period=Period.HOUR)
            df.to_csv(output_file, sep='\t', encoding='utf-8')
