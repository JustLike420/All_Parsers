import csv
import json
import os
import re
import time

import openpyxl
from openpyxl import Workbook, load_workbook
import csv
from loguru import logger
import requests
from bs4 import BeautifulSoup

logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')


class OlPartnersParser:
    def __init__(self):
        self.url = "http://ol.partners/Products"

        self.workbook = openpyxl.Workbook()

        self.sheet = self.workbook.active
        self.sheet.append(['Code', 'Name', 'EUR', 'USD', 'UAH many', 'UAH', 'AvailabilityStatus'])

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
        cookies = {
            '.AspNetCore.Antiforgery.w88DwCwRc4w': 'CfDJ8M0WEM0f1wlFhG3xjGgysWKWOrxUDI-6METSGlfnhmdAmeffPy7bX9a0dnekhY_W2yDhHIPWu4LQDPTd9OAvNc6GZG9kSCB3G5NQRbHP66SxYBiHmoAisQsk1wYrg2TYKogF6ZkcvDhKMtt-WVHPmX8',
            '.AspNetCore.Cookies': 'CfDJ8M0WEM0f1wlFhG3xjGgysWJzhOAng9sdVTbL3Rc-96_J-9KLYZzRHkN1T7eHZOvG7EAAJmu9nxpJHwqedoR6HTUl4Smk3dxDBHZESuGcGEbjmWOzg9osFqdtYjZBM9N36BgpMu8dB25-S0UohYxX120jo83kfUxP5PMQcUt0g3LWSgE9rW1_ODOO6N3zTSfJ0j1ZytSnLBJBGdZzSnt0eTICKqTIU_-bfraPsFcfCcq3IwPTJ3u2JS2y0su-BJtePYyypgGiMe9FYdMaHVT9dJDGbEK74WeNUYJT-HjjdS7OevqhY4gJjgsDTl0aDf7l_B_m6u5upC2JQV30vjl3ocgLJePhOCOcDi_HdQbhAro6lwHoJMPpfF1PBVP0fuV-VuHiuQB0TH990yRpmnm6hvO0tfqFB07VJJeKagtKxDkSZUCCnDwv_mrfm1daTe7rKE9mNRAyLmI6PmTBdmfjh7HoCZBTsdwlCZO2A-akM_AWx1B5fCd-WhkvxRx3pG1PMPUEdIT-8BAA9AlgMNmWuHpoFXNTxUwc_RfbXv3HevT6iC5XzP2_f38Lu9xObUFcBvRVwqCn3h74fXC_PwI3wyfcz69EUTlqBVgjzsKHwLyA1B1WVboibfKhh0Y7RPW7SCeco4VgdSO5syjewMcGxW3uxFNdWpEY5ORhBQzpx7z7zZ3_XIwq3tHTBpiygAbgyTwmDW68d1Q5FomejFY5RXM',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'http://ol.partners/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        params = {
            'categoryId': category_id,
        }
        try:
            html = requests.get(self.url, params=params, cookies=cookies, headers=headers).text
        except:
            logger.exception('Connection error')

            logger.error(f'Wait 10 sec and retry. Retry count: 1')
            time.sleep(10)
            html = self.site_request()
        return html

    def starter(self) -> None:
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
            logger.info('Job DONE')
        finally:

            logger.info('=====================Close scraping=====================')


if __name__ == '__main__':
    OlPartnersParser().starter()
