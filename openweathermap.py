import requests


class Parser:
    def __init__(self):
        self.URL = 'https://api.openweathermap.org/data/2.5/weather'

    def get_json(self):
        response = requests.get(self.URL, params={
            'q': 'Ташкент',
            'appid': '1843127cf10122cbc5515c43b7ba3c22',
            'units': 'metric',
            'lang': 'ru'
        })
        try:
            response.raise_for_status()
            json = response.json()
            return json
        except requests.HTTPError:
            print(f'Произошла ошибка {response.status_code}')

    def get_content(self, json):
        weather = json['weather']
        city_name = json['name']

        #for weat in weather:
        print(f'Погода в {city_name}е {weather[0]["description"]}')

    def run(self):
        json = self.get_json()
        if json:
            self.get_content(json)


parser = Parser()
parser.run()
