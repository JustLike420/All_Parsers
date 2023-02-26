import json
import os
import re
import time
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
from loguru import logger
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')


class OlPartnersAuth:
    def __init__(self):
        self.url = 'http://ol.partners/Account/Login'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )

        self.email = os.getenv('email')
        self.password = os.getenv('password')
        logger.info("Запускаю браузер")

    def auth(self) -> None:
        logger.info("Прохожу авторизацию")
        self.driver.get(self.url)

        email_input = self.driver.find_element(By.ID, "Email")
        email_input.send_keys(self.email)
        password_input = self.driver.find_element(By.ID, "Password")
        password_input.send_keys(self.password)

        login_button = self.driver.find_element(By.CLASS_NAME, "submitBlue")
        login_button.click()
        logger.success("Авторизация завершена")

    def get_cookies(self) -> dict:
        logger.info("Получаю куки")
        cookies_dict = {}
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        self.driver.quit()
        return cookies_dict


class OlPartnersParser:
    def __init__(self, cookies: dict):
        self.url = "http://ol.partners/Products"

        self.workbook = openpyxl.Workbook()

        self.sheet = self.workbook.active
        self.sheet.append(['Code', 'Name', 'EUR', 'USD', 'UAH many', 'UAH', 'AvailabilityStatus'])

        self.cookies = cookies

    def __del__(self):
        self.workbook.save('data.xlsx')

    def save_data(self, data):

        self.sheet.append(
            [data['Code'], data['Name'], data['PriceEUR'], data['Price'], data['PriceUAH'], data['PriceX'],
             data['AvailabilityStatusString']])

    def get_page_data(self, category_id):
        html = self.site_request(category_id)
        soup = BeautifulSoup(html, 'html.parser')
        scripts = soup.find_all('script')
        data_script = scripts[28].string
        match = re.search(r'"dataSource"\s*:\s*[^[]*\[([^\]]*)\]', data_script)
        contents = '[' + match.group(1) + ']'

        all_data = json.loads(contents)
        for data in all_data:
            self.save_data(data)
        logger.success(f"Saved {len(all_data)} lines!")

    def site_request(self, category_id) -> str:
        """Запрос на страницу"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'http://ol.partners/Account/Login?ReturnUrl=^%^2F',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        params = {
            'categoryId': category_id,
        }
        try:
            html = requests.get(self.url, params=params, cookies=self.cookies, headers=headers).text
        except:
            logger.exception('Connection error')

            logger.error(f'Wait 10 sec and retry. Retry count: 1')
            time.sleep(10)
            html = self.site_request()
        return html

    def starter(self) -> None:
        logger.info("Запуск парсера")
        try:
            all_categories = ['11f01a80-c6dd-43f1-ae13-1feb3af842e4',
                              '940e48f2-1b99-44e3-95d0-456f77b1cbfe',
                              '75a30afc-297b-4a5a-ae3e-3adedb31da5d',
                              'e640a874-fd20-4d68-a5cf-3b9354bccc5a',
                              '4a363165-8ca2-4875-a8aa-6401eaeb60b7',
                              '4b1ed2a0-7372-49d4-8570-7be730b86a84',
                              'f4087857-f58b-41d1-b1e0-7b407b3e3bfa',
                              '40137948-7c36-4187-a598-0d50eb1df16f',
                              '85089059-b2ea-414c-a0f0-0cb7187f4e74',
                              '98cef2a4-d106-4da2-9b4c-f8e66696fd13',
                              'd191ae68-f2ee-4472-8036-e37d06c8ffc9',
                              'cccd3e1f-6b84-49c8-b342-dee61a5caf10',
                              '271f5959-3c31-47d1-81a4-4ed3ce39cde4',
                              '386e20ca-2ae8-4a2c-a430-4cc5de787f7e',
                              'df91cb4f-7944-41cb-a05c-bca4d372fcec',
                              'd2c0cdcb-796c-48ac-be30-3fa9bad62c91']
            for category in all_categories:
                self.get_page_data(category)

        except Exception as e:
            logger.exception(e)
        else:
            logger.info("Готово!")
        finally:

            logger.success('=====================Парсинг завершен=====================')


if __name__ == '__main__':
    loginer = OlPartnersAuth()
    loginer.auth()
    cookies = loginer.get_cookies()
    OlPartnersParser(cookies).starter()
