import xml.etree.ElementTree as ET
from typing import TypedDict

import bs4.element
import openpyxl
import requests
from bs4 import BeautifulSoup


class CardDetails(TypedDict):
    code: int
    description: bs4.element.Tag


def get_card_urls() -> list:
    urls = []
    tree = ET.parse('VendorYML.xml')
    root = tree.getroot()
    for child in root.findall('vendor'):
        models = child.find('models')
        for model in models:
            urls.append(model.find('promoUrl').text)
    return urls


def parse_url(url: str) -> CardDetails:
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        code = soup.find('span', class_='product_code_by_font').text
    except:
        code = ''
    try:
        description = soup.find('div', class_='clear_styles')
    except:
        description = ''
    return CardDetails(**{"code": code, "description": description})


def change_image_urls(card_description: bs4.element.Tag) -> bs4.element.Tag:

    images = card_description.find_all('img')
    for image in images:
        image_src = image['src'].replace('../', 'https://www.fortu.ru/')
        image['src'] = image_src
    return card_description


def main():
    card_urls = get_card_urls()

    for url in card_urls:
        card = parse_url(url)
        card['description'] = change_image_urls(card['description'])
        print(f"[INFO] {card['code']} {url}")
        new_sheet.append((card['code'], str(card['description'])))
        new_book.save(f'output.xlsx')



if __name__ == "__main__":
    new_book = openpyxl.Workbook()
    new_sheet = new_book.active
    new_sheet['A1'].value = 'артикул'
    new_sheet['B1'].value = 'описание'
    main()
