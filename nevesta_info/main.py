import csv
import json
import time
from typing import Tuple
from loguru import logger
import requests
from bs4 import BeautifulSoup

logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')


class MaximumRetriesReached(Exception):
    pass


class Nevesta:
    def __init__(self, category):
        self.category = category
        self.url = f'https://www.nevesta.info/catalog/{self.category}/Russia-2017370/'
        self.stream = open(f"result_{self.category}.csv", "w", newline='')
        self.writer = csv.writer(self.stream)
        self.iter = 1

    def __del__(self):
        """Закрытие файла и конвертация в xlsx"""
        from convert import convert_workbook
        self.stream.close()
        convert_workbook(f'result_{self.category}')

    def write_data(self, **kwargs) -> None:
        """Запись информации в файл"""
        self.writer.writerow(
            [kwargs['url'], kwargs['phone']])
        logger.info(f'Write = {kwargs["url"]} {kwargs["phone"]} Page: {kwargs["page"]} All: {self.iter}')
        self.iter += 1

    def parse_html(self, url: str) -> str:
        """Запрос на страницу"""
        headers = {
            'authority': 'www.nevesta.info',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        try:
            html = requests.get(url, headers=headers).text
        except:
            logger.exception('Connection error')

            logger.error(f'Wait 10 sec and retry. Retry count: 1')
            time.sleep(10)
            html = self.parse_html(url)
        return html

    def get_contacts(self, item_id: str) -> Tuple[str, str]:
        """Получение номера"""
        url = f'https://nevesta.info/catalog/{item_id}/contacts/'
        html = self.parse_html(url)
        return html, url

    def get_page(self, page: int) -> None:
        """Парсинг страницы"""
        url = self.url + f'page{page}/'
        html = self.parse_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        all_items = soup.find('div', class_='firms-list-long')
        import re
        pattern = re.compile(r'nevesta\.info/catalog/\d+')
        match = pattern.findall(str(all_items))
        all_items_links = list(set(match))
        for item in all_items_links:
            item_url = item.split('/')[-1]
            api_return, url = self.get_contacts(item_url)
            json_return = json.loads(api_return)
            phone = json_return.get('phone')

            self.write_data(url=url, phone=phone, page=page)

    def get_page_count(self) -> int:
        html = self.parse_html(self.url)
        soup = BeautifulSoup(html, 'html.parser')
        page_count = soup.find_all('a', class_='pagination__pages__list__item__link')[5]
        page_count = page_count.get('href').split('/')[-2].replace('page', '')
        return int(page_count)

    def starter(self) -> None:

        page_count = self.get_page_count()
        logger.info(f'Find {page_count} PAGES')
        try:
            for page in range(1, page_count + 1):
                self.get_page(page)
        except Exception as e:
            logger.exception(e)
        else:
            logger.info('Job DONE')
        finally:

            logger.info('=====================Close scraping=====================')
            logger.info(f'Scraped {self.iter - 1} items')


if __name__ == '__main__':
    f = Nevesta('artisty-i-show')
    f.starter()
    del f
