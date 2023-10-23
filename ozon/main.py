import time

from openpyxl import load_workbook

from ozon.selenium_parser import SeleniumParser
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class OzonParser(SeleniumParser):

    def save_page(self, url: str):
        self._driver.get(url)
        # time.sleep(6)
        WebDriverWait(self._driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="section-characteristics"]/div[1]/h2/a')))
        html_code = self._driver.page_source
        with open('data/' + url.split('/')[4] + ".html", "w", encoding="utf-8") as file:
            file.write(html_code)


workbook = load_workbook('data.xlsx')
worksheet = workbook.active

with OzonParser() as parser:
    for cell in worksheet['A']:
        link = cell.value
        if 'https' in link:
            try:
                parser.save_page(link)
            except:
                print(cell)


