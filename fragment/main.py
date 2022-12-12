import csv
import time

from loguru import logger
import requests
from bs4 import BeautifulSoup

logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')


class MaximumRetriesReached(Exception):
    pass


class FragmentParser:
    def __init__(self):
        self.url = 'https://fragment.com/username/'
        self.nicks = None
        self.prices = open('prices.txt', 'w')
        self.stream = open("result.csv", "w", newline='')
        self.writer = csv.writer(self.stream)
        self.count = 0
        self.iter = 1

    def get_nicks_from_file(self, file_name: str = 'nicks.txt') -> None:
        """Получение всех ников с файла"""
        with open(file_name, 'r', encoding='utf-8') as file:
            self.nicks = file.read().split('\n')
        logger.info(f'Find {len(self.nicks)} nicks. Starting...')

    def write_data(self, **kwargs) -> None:
        """Запись информации в файл"""
        self.writer.writerow(
            [kwargs['username'], kwargs['status'], kwargs['current_price'], kwargs['min_price'], kwargs['url']])
        logger.info(f'Write = {kwargs["username"]} {kwargs["status"]} {self.iter}')
        self.iter += 1

    def parse_html(self, username):
        headers = {
            'authority': 'fragment.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        url = self.url + username
        try:
            html = requests.get(url, headers=headers).text
        except:
            logger.exception('Connection error')

            logger.error(f'Wait 10 sec and retry. Retry count: 1')
            time.sleep(10)
            html = self.parse_html(username)
        return html

    def get_user(self, username: str) -> None:
        """Парсинг карточки ника"""
        html = self.parse_html(username)
        url = self.url + username
        soup = BeautifulSoup(html, 'html.parser')
        check_unavailable = soup.find('h1', class_='tm-main-intro-header')
        if check_unavailable:
            status = 'unavailable'
            current_price = None
            min_price = None
            url = None
            try:
                self.write_data(username=username, status=status, current_price=current_price, min_price=min_price,
                                url=url)
                self.count += 1
            except:
                logger.debug(username + ' ERROR')
            return
        status = soup.find('span', class_='tm-section-header-status').text

        if status == 'Available':
            try:
                min_price = soup.select_one(
                    '#aj_content > main > section > div.tm-section-box.tm-section-bid-info > div > span:nth-child(2)').text
            except:
                min_price = None
            try:

                current_price = soup.find('div', class_='table-cell-value').text
            except:
                current_price = 0
        elif status == 'Sold' or status == 'On auction':
            try:
                current_price = soup.find('div', class_='table-cell-value').text
            except:
                current_price = None
            min_price = None
        else:
            status = 'error'
            current_price = None
            min_price = None
            url = None
        self.write_data(username=username, status=status, current_price=current_price, min_price=min_price, url=url)

    def starter(self) -> None:
        try:
            self.get_nicks_from_file()
            for nick in self.nicks:
                self.get_user(nick)
        except Exception as e:
            logger.exception(e)
        else:
            logger.info('Job DONE')
        finally:

            logger.info('=====================Close scraping=====================')
            logger.info(f'Errors {len(self.nicks) - self.count - 1} found')
            logger.info(f'Scraped {self.count} items')


if __name__ == '__main__':
    f = FragmentParser()
    f.starter()
