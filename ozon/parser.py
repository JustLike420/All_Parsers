import json
import os
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd

char_div = 'state-webCharacteristics-545710-default-1'


def get_element_text(element) -> str:
    e = element.text.replace('\n', '')
    cleaned_text = re.sub(r'\s+', ' ', e)
    return cleaned_text


with open('data/test.html', 'r', encoding='utf-8') as file:
    data = file.read()


def parse_data(data):
    soup = BeautifulSoup(data, 'html.parser')

    # характеристики

    elements = soup.find('div', id='section-characteristics').find_all('dl', class_='s6j')
    for element in elements:
        key = get_element_text(element.find('dt'))
        value = get_element_text(element.find('dd'))
        print(key, value)

    compound = soup.find_all('div', id='section-description')
    compound_text = ''
    for c in compound:
        if 'Состав' in c.text:
            compound_text = get_element_text(c).replace('Состав', '')
            print(compound_text)
    main_info = soup.find('script', type='application/ld+json').text
    data_dict = json.loads(main_info)
    price = data_dict['offers']['price']
    description = data_dict['description']
    image = data_dict['image']

    content = soup.find('div', class_='client-state')
    char_div = content.find('div', id='state-webCharacteristics-545710-default-1').get('data-state')
    print(char_div)


def test():
    df = pd.DataFrame()
    folder_path = 'data'
    i = 1
    file_names = os.listdir(folder_path)
    for file_name in file_names:

        table_item = {
            "Ссылка": "",
            "Наименование": "",
            "Цена": "",
            "Описание": "",
            "Предпочтения (Особенности состава)": "",
            "Подкатегория (Область использования)": "",
            "Средство (Тип)": "",
            "Эффект (Эффект от использования уходовой косметики)": "",
            "Текстура": "",
            "Тип кожи": "",
            "Формат упаковки (Упаковка)": "",
            "Активные ингредиенты (Бьюти-ингредиент)": "",
            "Тип волос": "",
            "Вес": "",
            "Объём": "",
            "Цвет": "",
            "Тип кожи головы": "",
            "Возраст (Возрастной диапазон)": "",
            "Способ применения": "",
            "Состав": "",
            "Фотографии товара": "",
        }
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
        soup = BeautifulSoup(file_contents, 'html.parser')
        main_info = soup.find('script', type='application/ld+json').text
        data_dict = json.loads(main_info)
        name = data_dict['name']
        url = data_dict['offers']['url']
        price = data_dict['offers']['price']
        description = data_dict['description']
        image = data_dict['image']
        table_item['Ссылка'] = url
        table_item['Наименование'] = name
        table_item['Цена'] = price
        table_item['Описание'] = description
        table_item['Фотографии товара'] = image

        compound = soup.find_all('div', id='section-description')
        composition = ''
        application_method = ''
        for c in compound:
            if 'Состав' in c.text:
                compound_text = get_element_text(c)
                result = re.split(r"(?=Способ применения|$)", compound_text)

                if len(result) >= 1:
                    composition = result[0].replace("Состав", "").strip()
                    application_method = result[1].replace("Способ применения", "").strip() if len(result) > 1 else ""

        table_item['Состав'] = composition
        table_item['Способ применения'] = application_method
        content = soup.find('div', class_='client-state')
        char_div = content.find('div', id='state-webCharacteristics-545710-default-1').get('data-state')
        char_dict = json.loads(char_div)
        chars = char_dict['characteristics'][0]

        for char in chars['short']:

            match char['name']:
                case 'Тип':
                    table_item['Средство (Тип)'] = char['values'][0]['text']
                case 'Объем, мл':
                    table_item['Объём'] = char['values'][0]['text']
                case 'Тип кожи':
                    table_item['Тип кожи'] = char['values'][0]['text']
                case 'Область использования':
                    table_item['Подкатегория (Область использования)'] = char['values'][0]['text']
                case 'Эффект от использования уходовой косметики':
                    table_item['Эффект (Эффект от использования уходовой косметики)'] = char['values'][0]['text']
                case 'Упаковка':
                    table_item['Формат упаковки (Упаковка)'] = char['values'][0]['text']
                case 'Вес, г':
                    table_item['Вес'] = char['values'][0]['text']
                case 'Цвет':
                    table_item['Цвет'] = char['values'][0]['text']
                case 'Особенности состава':
                    table_item['Предпочтения (Особенности состава)'] = char['values'][0]['text']
                case 'Тип волос':
                    table_item['Тип волос'] = char['values'][0]['text']
                case 'Эффект':
                    table_item['Эффект (Эффект от использования уходовой косметики)'] = char['values'][0]['text']
                case 'Бьюти-ингредиент':
                    table_item['Активные ингредиенты (Бьюти-ингредиент)'] = char['values'][0]['text']
                case 'Возрастной диапазон':
                    table_item['Возраст (Возрастной диапазон)'] = char['values'][0]['text']
                case 'Текстура':
                    table_item['Текстура'] = char['values'][0]['text']
                case 'Тип волос':
                    table_item['Тип волос'] = char['values'][0]['text']
                case 'Тип кожи головы':
                    table_item['Тип кожи головы'] = char['values'][0]['text']
                case 'Способ применения':
                    table_item['Способ применения'] = char['values'][0]['text']
        # print(table_item)

        df = df._append(table_item, ignore_index=True)
        df.to_excel('products_test.xlsx', index=False)
        print(i, '/', len(file_names))
        i += 1
        # break


# parse_data(data)
test()
