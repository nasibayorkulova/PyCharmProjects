import requests
from bs4 import BeautifulSoup
import json
from config import CATEGORIES
from database import Database


# response = requests.get('https://www.afisha.uz/exhibitions/')
# print(response) #вывод кода HTTP состояния
# print(response.text) #вывод html страницы
# html = response.text

# soup = BeautifulSoup(html, 'html.parser') # упрощает сбор информации с веб-страниц
# whenlist = soup.find('table', class_ = 'when-list')
# whenblock = whenlist.find('td', class_ = 'whenblock')
# print(whenblock)

class Parser:
    def __init__(self):
        self.URL = 'https://www.afisha.uz/exhibitions/'
        self.HOST = 'https://www.afisha.uz'
        self.database = Database()

    def get_html(self):
        try:
            response = requests.get(self.URL)
            response.raise_for_status()
            html = response.text
            return html
        except requests.HTTPError:
            print(f'Произошла ошибка {response.status_code}')

    def get_content(self, category_name, html):
        soup = BeautifulSoup(html, 'html.parser')
        whenlist = soup.find_all('table', class_='when-list')
        content = {category_name: []}
        for whenl in whenlist:
            whenblock = whenl.find('td', class_='whenblock')
            num = whenblock.find('p', class_='w-num').get_text()
            month = whenblock.find('p', class_='w-month').get_text()
            day = whenblock.find('p', class_='w-day').get_text(strip=True)

            data = f'{num}-{month}-{day}'

            what = whenl.find('td', class_='what').find_all('div', style='height: 1%; overflow:hidden;')
            # title = what.find('div', class_='item2').find('a').get_text()
            # url = self.HOST + what.find('div', class_='item2').find('a')['href']
            # desc = what.find('div', class_='item2').find_all('p', class_='desc').get_text().replace(' ',' ')
            # place = what.find('div', class_='item2').find('p', class_='place').get_text()

            content[category_name].append({
                'Дата': data,
                'Мероприятия': [{
                    'Название': block.find('div', class_='item2').find('a').get_text().replace(' ', ' '),
                    'Ссылка': self.HOST + block.find('div', class_='item2').find('a')['href'],
                    'Описание': block.find('div', class_='item2').find('p', class_='desc').get_text().replace(' ', ' '),
                    'Место проведения': block.find('div', class_='item2').find('p', class_='place').get_text()
                } for block in what]
            })

            for photo in what:
                photo_url = self.HOST + photo.find('div', class_='fl').find('a')['href']
                self.database.insert_data('afisha_photos', photo_url)
            self.database.export_json()
        return content

    def run(self, category_name, category_url):
        self.URL = category_url
        html = self.get_html()
        if html:
            content = self.get_content(category_name, html)

            with open('afisha_exhibitions.json', mode='w', encoding='utf-8') as file:
                json.dump(content, file, indent=4, ensure_ascii=False)


parser = Parser()
for category_name, category_url in CATEGORIES.items():
    parser.run(category_name, category_url)
