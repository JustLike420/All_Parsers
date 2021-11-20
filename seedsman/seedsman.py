import csv
import math
import os
import time
import re
from random import choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool
import requests
from seleniumwire import webdriver
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select


useragent = UserAgent()
options = webdriver.ChromeOptions()

# options.add_argument("--headless") - скрыть окно браузера

# файлы
table = 'table.csv'  # таблица с результатами, создавать не надо, просто указать путь
media = 'media'  # папка с фото
site_urls = 'urls.txt'  # путь до файла с сылками
proxies = open('proxy_list.txt').read().split('\n')  # прокси

options.add_argument("--start-maximized")


check_file = os.path.exists(f'{table}')
if not check_file:
    with open(table, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(('ссылка', 'название категории', 'описание категории', 'Название товара', 'Описание товара',
                         'Название фото', 'Ссылка на товар', 'Рейтинг', 'Кол-во отзывов', 'Нумерация',
                         'Подпись под рейтингом', 'Characteristic', 'Description', 'BREEDER/BRAND',
                         'PRODUCT TYPE', 'GENETICS', 'PACK SIZE', 'VARIETY', 'FLOWERING TYPE', 'SEX',
                         'THC CONTENT', 'CBD Content', 'YIELD', 'GROWS', 'FLOWERING TIME',
                         'MEDICAL CONDITIONS', 'MEDICINAL PROPERTIES', 'TASTE / FLAVOUR', 'EFFECT',
                         'HARVEST MONTH', 'PLANT HEIGHT', 'AWARDS', 'Other'))
else:
    pass

with open(site_urls, 'r', encoding="utf-8") as file:
    urls = file.read()
urls = urls.split('\n')

num = {
    'id': 1
}


def data():
    for site_id in range(0, len(urls)):
        options.add_argument(f"user-agent={useragent.random}")
        proxy = choice(proxies).split(':')
        ip = proxy[0]
        port = proxy[1]
        login = proxy[2]
        password = proxy[3]
        print(f"{ip}:{port}")
        proxy_options = {
            "proxy": {
                "https": f"http://{login}:{password}@{ip}:{port}"
            }

        }

        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            seleniumwire_options=proxy_options,
            options=options,
        )
        url = urls[site_id]
        driver.get(url=url)
        auth(driver)
        pages = driver.find_element_by_xpath(
            '//*[@id="main-page-wrapper"]/div/div[3]/div[2]/div[2]/div[3]/div[1]/div[2]/div/p').text
        pages = pages.split(' ')
        pages = int(pages[0])
        pages_count = math.ceil(pages / 12) + 1

        soup = BeautifulSoup(driver.page_source, "lxml")
        cat_name = soup.find('div', class_='page-title').find('h1').text
        cat_description_end = ''
        try:
            cat_description = soup.find('div', class_='category-description').find_all('p')
            for par in cat_description:
                cat_description_end += ' ' + par.text
        except:
            pass
        with open(table, 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow((url, cat_name, cat_description_end, '', '', '', '', '', '', '', '', ''))
            driver.quit()
        for i in range(1, pages_count):
            if pages_count == 2:
                new_url = url
            else:
                new_url = f'{url}?&p={i}'
            options.add_argument(f"user-agent={useragent.random}")
            proxy = choice(proxies).split(':')
            ip = proxy[0]
            port = proxy[1]
            login = proxy[2]
            password = proxy[3]
            print(f"{ip}:{port}")
            proxy_options = {
                "proxy": {
                    "https": f"http://{login}:{password}@{ip}:{port}"
                }

            }
            driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                seleniumwire_options=proxy_options,
                options=options,
            )

            driver.get(url=new_url)
            soup = BeautifulSoup(driver.page_source, "lxml")
            cards = soup.find_all('li', class_='item')

            item_urls = []
            for card in cards:
                item_url = card.find('a').get('href')
                item_urls.append(item_url)
                get_parce(item_url, driver)


def auth(driver):
    try:
        selector = driver.find_element_by_name("country_id")
        drp = Select(selector)
        drp.select_by_index(2)
        time.sleep(3)
        driver.find_element_by_class_name("ageButton").click()
        time.sleep(3)
    except:
        print('Authicated')


def get_parce(item_url, driver):
    driver.get(url=item_url)
    item_name = item_url.split('/')[-1]
    if item_name == '':
        item_name = item_url.split('/')[-2]
    print(item_url, item_name, '|', num['id'])
    time.sleep(3)
    try:
        auth(driver)
    except:
        print("уже авторизирован")
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    name = soup.find('div', class_='product-shop').find('div', class_='product-name').find('h1').text
    mini_description = soup.find('div', class_='mini-description').find('div', class_='std').text.split('\n')
    mini_description = mini_description[1]
    t = True
    while t:
        try:
            reviews = WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="product_addtocart_form"]/div[3]/div[1]/div[2]/div/div[1]/div[1]'))).text
            t = False
            time.sleep(10)
            reviews = reviews.split('\n')
            stars = reviews[0].split()
            stars = stars[0].replace('.', ',')
            reviews = reviews[1]
            if reviews == 'Write a review':
                reviews = 'none'
            elif stars == '':
                reviews = 'None'
                stars = 0
            else:
                reviews = reviews.split()
                reviews = reviews[0]
        except:
            driver.refresh()
            continue

    image_link = soup.find("img", {"id": "image-main"}).get("src")
    image_name = item_name + '.jpg'
    proxi = open('proxy_list.txt').read().split('\n')
    proxy = choice(proxi).split(':')
    ip = proxy[0]
    port = proxy[1]
    login = proxy[2]
    password = proxy[3]

    proxies = {
        "https": f"http://{login}:{password}@{ip}:{port}",
    }

    headers = {
        "user-agent": f"{useragent.random}",
    }

    req = requests.get(url=image_link, headers=headers, proxies=proxies)
    response = req.content
    with open(f"{media}/{image_name}", "wb") as file:
        file.write(response)
    big_description = soup.find('div', class_='product-description').find('div', class_="std").find_all('p')
    big_description_text = soup.find('div', class_='product-description').find('div', class_="std")
    big_description_text = str(big_description_text)
    big_description_text = re.sub('<(a).*?>', '', big_description_text)
    big_description_text = re.sub('<(.a).*?>', '', big_description_text)
    big_description_end = ''

    for par in big_description:
        big_description_end += par.text

    characteristics = soup.find('table', id='product-attribute-specs-table').find('tbody').find_all('tr')
    characteristic_table = soup.find('table', id='product-attribute-specs-table')
    characteristic = ''
    char_breeder_brand = char_product_type = char_genetics = char_pack_size = char_variety = char_flowering_type = ''
    char_sex = char_thc_content = char_cbd_content = char_yield = char_plant_height = char_grows = char_flowering_time = ''
    char_harvest_month = char_medical_conditions = char_medicinal_properties = char_taste_flavour = char_effect = ''
    char_other = char_awards = ''

    for row in characteristics:
        characteristic_name = char_desc = ''
        try:
            characteristic_name = f"{row.find('th', class_='label').text}"
            char_desc = f"{row.find('td', class_='data').text}"
            characteristic = characteristic + f"{row.find('th', class_='label').text}: {row.find('td', class_='data').text} | "
        except:
            driver.refresh()
            time.sleep(7)
        if characteristic_name == 'Breeder/Brand':
            char_breeder_brand = char_desc
        elif characteristic_name == 'Product Type':
            char_product_type = char_desc
        elif characteristic_name == 'Genetics':
            char_genetics = char_desc
        elif characteristic_name == 'Pack Size':
            char_pack_size = char_desc
        elif characteristic_name == 'Variety':
            char_variety = char_desc
        elif characteristic_name == 'Flowering Type':
            char_flowering_type = char_desc
        elif characteristic_name == 'Sex':
            char_sex = char_desc
        elif characteristic_name == 'THC Content':
            char_thc_content = char_desc
            char_thc_content = char_thc_content.replace('.', ',')
        elif characteristic_name == 'CBD Content':
            char_cbd_content = char_desc
        elif characteristic_name == 'Yield':
            char_yield = char_desc
        elif characteristic_name == 'Plant Height':
            char_plant_height = char_desc
        elif characteristic_name == 'Grows':
            char_grows = char_desc
        elif characteristic_name == 'Flowering Time':
            char_flowering_time = char_desc
        elif characteristic_name == 'Harvest Month':
            char_harvest_month = char_desc
        elif characteristic_name == 'Medical Conditions':
            char_medical_conditions = char_desc
        elif characteristic_name == 'Medicinal Properties':
            char_medicinal_properties = char_desc
        elif characteristic_name == 'Taste / Flavour':
            char_taste_flavour = char_desc
        elif characteristic_name == 'Effect':
            char_effect = char_desc
        elif characteristic_name == 'AWARDS':
            char_awards = char_desc
        else:
            char_other = ''

    description = f"<h4>{mini_description}</h4> <h3>Characteristics</h3> {characteristic_table} <h3>Description</h3> {big_description_text}"


    with open(table, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(('', '', '', name, description,
                         image_name, item_url, stars, reviews, num['id'],
                         mini_description, characteristic, big_description_end, char_breeder_brand,
                         char_product_type, char_genetics, char_pack_size, char_variety, char_flowering_type, char_sex,
                         char_thc_content, char_cbd_content, char_yield, char_grows, char_flowering_time,
                         char_medical_conditions, char_medicinal_properties, char_taste_flavour, char_effect,
                         char_harvest_month, char_plant_height, char_awards, char_other))
    num['id'] = num['id'] + 1



if __name__ == '__main__':
    data()
