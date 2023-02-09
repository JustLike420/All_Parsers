import csv
import os
import time
from openpyxl import Workbook, load_workbook
import csv
from loguru import logger

import requests
from bs4 import BeautifulSoup

logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')
de = 'https://wordsofwonders.app/games/words-of-wonders-de-losungen'
br = 'https://wordsofwonders.app/games/words-of-wonders-br-respostas'
es = 'https://wordsofwonders.app/games/words-of-wonders-es-respuestas'
fr = 'https://wordsofwonders.app/games/words-of-wonders-fr-solution'
tr = 'https://wordsofwonders.app/games/words-of-wonders-tr-cevaplari'
ja = 'https://wordsofwonders.app/games/words-of-wonders-ja-%e7%ad%94%e3%81%88'


class WoW:
    def __init__(self, lang):
        self.link_by_lang = {
            "de": "de-losungen",
            "br": "br-respostas",
            "es": "es-respuestas",
            "fr": "fr-solution",
            "tr": "tr-cevaplari",
            "ja": "ja-%e7%ad%94%e3%81%88",
            "ru": "ru-otvety"
        }
        self.url = f"https://wordsofwonders.app/games/words-of-wonders-{self.link_by_lang[lang]}"
        self.domain = 'https://wordsofwonders.app'
        if not os.path.exists('data'):
            os.mkdir('data')
        self.stream = open(f"data/result_{lang}1.csv", "w", newline='', encoding='utf-8')
        self.writer = csv.writer(self.stream)
        self.all_lvl = []
        self.lvl_counter = 0

    def write_data(self, **kwargs) -> None:
        """Запись информации в файл"""
        self.writer.writerow([kwargs['lvl_link']])

    def site_request(self, url: str) -> str:
        """Запрос на страницу"""
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        try:
            html = requests.get(url, headers=headers, allow_redirects=False).text
        except:
            logger.exception('Connection error')

            logger.error(f'Wait 10 sec and retry. Retry count: 1')
            time.sleep(10)
            html = self.site_request(url)
        return html

    def parse_all_locations(self) -> list:
        """Получение всех ссылок на локации"""
        locations_links = []
        response = self.site_request(self.url)
        soup = BeautifulSoup(response, 'lxml')
        locations = soup.find_all(class_='category-title')
        for location in locations:
            locations_links.append(location.find('a').get('href'))
        return locations_links

    def parse_location(self, url: str) -> None:
        response = self.site_request(url)
        soup = BeautifulSoup(response, 'lxml')
        lvls = soup.find_all(class_='level-title')
        self.lvl_counter += len(lvls)
        logger.success(f"Parsed +{len(lvls)} | All {self.lvl_counter}")
        for lvl in lvls:
            lvl_link = lvl.find('a').get('href')
            self.write_data(lvl_link=lvl_link)
            self.all_lvl.append(lvl_link)

    def starter(self) -> None:
        try:

            loc_links = self.parse_all_locations()
            logger.success(f"Find {len(loc_links)} locations")
            for loc_link in loc_links:
                url = self.domain + loc_link
                self.parse_location(url)
            # for lvl_link in self.all_lvl:
            #     response = self.site_request(lvl_link)
            #     words = self.get_words(response)
            #     logger.success(f"Parsed {self.lvl_counter}")
            #     self.lvl_counter += 1

        except Exception as e:
            logger.exception(e)
        else:
            logger.info('Job DONE')
        finally:

            logger.info('=====================Close scraping=====================')


class TheWoW(WoW):
    def __init__(self, lang):
        super().__init__(lang)
        self.link_by_lang = {
            'ru': '/ru',
            'ja': '/ja'
        }
        self.url = f'https://thewordsofwonders.com{self.link_by_lang[lang]}'
        self.domain = 'https://thewordsofwonders.com'

    def parse_all_locations(self) -> list:
        """Получение всех ссылок на локации"""
        locations_links = []
        response = self.site_request(self.url)
        soup = BeautifulSoup(response, 'lxml')
        locations = soup.find_all(class_='portfolio-link')
        for location in locations:
            locations_links.append(location.get('href'))
            print(location.get('href'))
        return locations_links

    def parse_location(self, url: str) -> None:
        response = self.site_request(url)
        soup = BeautifulSoup(response, 'lxml')
        lvls = soup.find_all(class_='portfolio-link')
        self.lvl_counter += len(lvls)
        logger.success(f"Parsed +{len(lvls)} | All {self.lvl_counter}")
        for lvl in lvls:
            lvl_link = self.domain + lvl.get('href')
            self.write_data(lvl_link=lvl_link)
            self.all_lvl.append(lvl_link)

class WoWNet(WoW):
    def __init__(self, lang):
        super().__init__(lang)
        self.link_by_lang = {
            'ru': '/ru',
            'ja': '/ja'
        }
        self.url = f'https://wordsofwonders.net/{self.link_by_lang[lang]}'
        self.domain = 'https://wordsofwonders.net/'

    def parse_all_locations(self) -> list:
        """Получение всех ссылок на локации"""
        locations_links = []
        response = self.site_request(self.url)
        soup = BeautifulSoup(response, 'lxml')
        locations = soup.find(class_='levels').find_all(class_='na')
        for location in locations:
            locations_links.append(location.get('href'))
        return locations_links

    def parse_location(self, url: str) -> None:
        response = self.site_request(url)
        soup = BeautifulSoup(response, 'lxml')
        lvls = soup.find(class_='levels').find_all(class_='na')
        self.lvl_counter += len(lvls)
        logger.success(f"Parsed +{len(lvls)} | All {self.lvl_counter}")
        for lvl in lvls:
            lvl_link = self.domain + lvl.get('href')
            self.write_data(lvl_link=lvl_link)
            self.all_lvl.append(lvl_link)

if __name__ == "__main__":
    # langs = ('ja',)
    # for lang in langs:
    #     WoW(lang).starter()
    # Writer().writer()
    # WoW('ja').starter()
    # TheWoW('ja').starter()
    WoWNet('ja').starter()
