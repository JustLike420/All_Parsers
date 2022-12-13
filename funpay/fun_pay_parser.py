import re
import time
import random
import numpy as np
import openpyxl
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class FunPay:
    def __init__(self):
        self.url = 'https://funpay.com/'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )

    def run(self):
        self.driver.get(f"{self.url}")

    def scroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def show_more(self):
        self.driver.find_element(By.CLASS_NAME, 'lazyload-more').click()


class CsGoSkins(FunPay):
    def __init__(self):
        super().__init__()
        self.url = 'https://funpay.com/lots/209/'

    def get_data(self):
        data = self.driver.page_source
        soup = BeautifulSoup(data, 'lxml')
        offers = soup.find_all('a', class_='tc-item')

        for offer in offers:
            user_block = offer.find('div', class_='tc-user')
            username = user_block.find('div', class_='media-user-name').text.strip()
            user_href = user_block.find('div', class_='avatar-photo')['data-href']
            try:
                rating = offer.find('span', class_='rating-mini-count').text
            except:
                rating = -1
            # print(username, user_href, rating)
            title = offer.find('div', class_='tc-desc-text').text
            title = re.sub('[^\x00-\x7Fа-яА-Я]', '', title)  # delete emoji
            if 'StatTrak' in title:
                stat_trak = True
                title = title.replace('StatTrak ', '')
                title = title.replace('StatTrak', '')
            else:
                stat_trak = False

            title = title.split(',')[0]  # delete trash
            try:
                filtered_title = title.split('|')
                gun_name = filtered_title[0]
                gun_title = filtered_title[1]
                filtered = True
            except:
                filtered_title = title
                gun_name, gun_title = '', ''
                filtered = False


            type = offer['data-f-type']
            try:
                other = offer['data-f-other']
            except:
                other = ''
            rare = offer['data-f-rare']
            quality = offer['data-f-quality']
            href = offer['href']
            count = offer.find('div', class_='tc-amount').text
            price = offer.find('div', class_='tc-price')['data-s']
            # print(title, type, other, rare, quality, href, count, price, stat_trak)
            if filtered:
                print(title, '------', gun_name, '-------', gun_title)

if __name__ == '__main__':
    funpay = CsGoSkins()
    funpay.run()
    # while True:
    #     funpay.scroll()
    #     try:
    #         funpay.get_data()
    #         funpay.show_more()
    #     except:
    #         break
    funpay.get_data()
    time.sleep(100)
