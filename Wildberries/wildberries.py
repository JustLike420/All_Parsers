import datetime
import openpyxl
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

new_book = openpyxl.Workbook()
new_sheet = new_book.active

new_sheet['A1'].value = 'Текст'
new_sheet['B1'].value = 'Кол-во товара'
today = datetime.datetime.now()
today = today.strftime('%d.%m.%Y-%H.%M.%S')


def main(text):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    useragent = UserAgent()
    options.add_argument(f"user-agent={useragent.random}")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options,
    )

    driver.get(f"https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search={text}")
    try:
        tovar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'goods-count')))
        colichestvo = tovar.text.replace('товаров', '')

    except:
        colichestvo = 0
    new_sheet.append([text, colichestvo])
    new_book.save(f'output - {today}.xlsx')
    print(f'[+] {text} - {colichestvo}')

if __name__ == '__main__':
    f = open('text.txt', 'r', encoding='utf-8')
    for line in f:
        main(line.strip())
