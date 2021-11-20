import datetime
import time

import openpyxl
import requests
import os
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': '*/*'
}
xlsx_table = openpyxl.open('template.xlsx')
sheet = xlsx_table.active
table_links = ['https://kontinental.ru/catalog/ploskiy_prokat/list_nerzhaveyushchiy_/',
               'https://kontinental.ru/catalog/ploskiy_prokat/rulony_nerzhaveyushchie/',
               'https://kontinental.ru/catalog/sortovoy_prokat/krug_nerzhaveyushchiy/',
               'https://kontinental.ru/catalog/sortovoy_prokat/shestigrannik_nerzhaveyushchiy/',
               'https://kontinental.ru/catalog/sortovoy_prokat/ugolok_nerzhaveyushchiy/',
               'https://kontinental.ru/catalog/sortovoy_prokat/provoloka_nerzhaveyushchaya/',
               'https://kontinental.ru/catalog/trubnyy_prokat/truba_nerzhaveyushchaya_besshovnaya/',
               'https://kontinental.ru/catalog/trubnyy_prokat/truba_nerzhaveyushchaya_svarnaya/kruglaya/',
               'https://kontinental.ru/catalog/trubnyy_prokat/truba_nerzhaveyushchaya_svarnaya/profilnaya/']

today = datetime.datetime.now()
today = today.strftime('%Y-%m-%d')


def get_item_info(item_url):
    req = requests.get(item_url, headers=headers)

    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    name = soup.find(class_='product-box').find(class_='col-lg-5').find('div', class_='h1').text  # Название
    prices = soup.find(class_='product-box').find(class_='col-lg-7').find(class_='row').find_all(class_='col-6')
    price_list = []

    price1 = price2 = price3 = price4 = price5 = price6 = ''
    for price in prices:
        price_list.append(price.find('span').text)

    if len(price_list) == 2:
        price5 = price_list[0]
        price6 = price_list[1]
    elif len(price_list) == 3:
        price1 = price_list[0]
        price2 = price_list[1]
        price3 = price_list[2]
    elif len(price_list) == 4:
        price1 = price_list[0]
        price2 = price_list[1]
        price3 = price_list[2]
        price4 = price_list[3]

    min_price = min(price_list)

    weight = soup.find(class_='product-box').find(class_='col-lg-7').find(class_='buyer-nav').find_all('div')[1].find(
        'input').get('data-product-weight')  # расчетный вес
    chapters = soup.find_all(class_='breadcrumb-item')
    last_chapter = ''
    for chapter in chapters:
        way = chapter.find('span').text
        if way == 'Главная страница':
            pass
        else:
            last_chapter = last_chapter + way + ';'
    chapter_string = last_chapter[:-1]
    sheet.append([item_url, name, price1, price2, price3, price4, weight, price5, price6, min_price, chapter_string])
    print(item_url, name, price1, price2, price3, price4, weight, price5, price6, min_price, chapter_string)


def main(link_table):
    table_link = link_table + '?PGN=100000'
    req = requests.get(table_link, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    table = soup.find('div', class_='catalog-section').find_all(class_='product-item-container')
    for row in table:
        item_url = 'https://kontinental.ru' + row.find('a').get('href')
        get_item_info(item_url)
    xlsx_table.save(f'{today} - металлопрокат.xlsx')
    xlsx_table.close()


if __name__ == '__main__':
    for link in table_links:
        main(link)
        time.sleep(10)
