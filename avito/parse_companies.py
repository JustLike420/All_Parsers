import csv
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger

logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')


class Avito:
    def __init__(self):
        self.url = 'https://www.avito.ru/all/predlozheniya_uslug/delovye_uslugi-ASgBAgICAUSYC7KfAQ?cd=1&q=%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F+%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%BE%D0%B2+%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%BF%D0%BB%D0%B5%D0%B9%D1%81%D0%BE%D0%B2&user=2'
        self.stream = open("result.csv", "w", newline='')
        self.writer = csv.writer(self.stream)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=C:\Users\Vladimir\PycharmProjects\All_Parsers\User Data")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )

        self.iter = 1

    def write_data(self, **kwargs) -> None:
        """Запись информации в файл"""
        self.writer.writerow(
            [kwargs['name']])
        logger.info(f'Write = {kwargs["name"]} {self.iter} PAGE: {kwargs["page"]}')
        self.iter += 1

    def run(self):
        self.driver.get(f"{self.url}")

    def parse_html(self, page: int):
        # url = f'https://www.avito.ru/all/predlozheniya_uslug?p={page}&q=%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F+%D0%B4%D0%BB%D1%8F+%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%BF%D0%BB%D0%B5%D0%B9%D1%81%D0%BE%D0%B2&user=2'
        url = f'https://www.avito.ru/all/predlozheniya_uslug/delovye_uslugi-ASgBAgICAUSYC7KfAQ?cd=1&p={page}&q=%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F+%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D0%BE%D0%B2+%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%BF%D0%BB%D0%B5%D0%B9%D1%81%D0%BE%D0%B2'
        try:
            self.driver.get(url)

            html = self.driver.page_source
        except:
            logger.exception('Connection error')

            logger.error(f'Wait 10 sec and retry. Retry count: 1')
            time.sleep(10)
            html = self.parse_html(page)
        return html

    def get_company(self, page: int) -> None:
        """Парсинг страницы"""
        html = self.parse_html(page)

        soup = BeautifulSoup(html, 'lxml')
        all_names = soup.find_all('div', class_='style-title-_wK5H')
        for name in all_names:
            self.write_data(name=name.text, page=page)

    def starter(self) -> None:
        pages = [i for i in range(1, 6)]
        try:
            for page in pages:
                self.get_company(page)
        except Exception as e:
            logger.exception(e)
        else:
            logger.info('Job DONE')
        finally:
            logger.info('=====================Close scraping=====================')
            logger.info(f'Scraped {self.iter - 1} items')


if __name__ == "__main__":
    a = Avito()
    a.starter()
    a.driver.close()
