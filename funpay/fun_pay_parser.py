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
            href = offer['href']
            quality = offer['data-f-quality']
            description = offer.find('div', class_='tc-desc-text').text
            description = re.sub('[^\x00-\x7Fа-яА-Я]', '', description)  # delete emoji
            price = offer.find('div', class_='tc-price').text
            print(href, quality, description, price)


if __name__ == '__main__':
    funpay = CsGoSkins()
    funpay.run()
    while True:
        funpay.scroll()
        try:
            funpay.show_more()
        except:
            break
    funpay.get_data()
    time.sleep(100)
