import time
import xml.etree.ElementTree as ET
from typing import TypedDict
import bs4.element
import requests
from bs4 import BeautifulSoup


class CardDetails(TypedDict):
    # code: int
    description: bs4.element.Tag


def get_card_urls() -> list:
    cards = []
    tree = ET.parse('VendorYML.xml')
    root = tree.getroot()
    for child in root.findall('vendor'):
        models = child.find('models')
        for model in models:
            cards.append({"url": model.find('promoUrl').text, "code": model.find('vendorCode')})
    return cards


def parse_url(url: str) -> CardDetails:
    req = requests.get(url)
    if req.status_code != 200:
        time.sleep(10)
        parse_url(url)
    else:
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        # try:
        #     code = soup.find('span', class_='product_code_by_font').text
        # except:
        #     code = ''
        try:
            description = soup.find('div', class_='clear_styles')
        except:
            description = ''
        return CardDetails(**{"description": description})


def change_image_urls(card_description: bs4.element.Tag) -> bs4.element.Tag:
    images = card_description.find_all('img')
    for image in images:
        try:
            image_src = image['src'].replace('../', 'https://www.fortu.ru/')
            image['src'] = image_src
        except:
            pass
    return card_description


def main():
    card_urls = get_card_urls()

    r = ET.Element('cards')
    i = 0
    for url in card_urls:
        if i > 2008:
            card = parse_url(url['url'])
            card['description'] = change_image_urls(card['description'])
            print(url['url'], i)
            card_xml = ET.SubElement(r, 'card')
            code = ET.SubElement(card_xml, 'code')
            code.text = str(url['code'].text)
            description = ET.SubElement(card_xml, 'description')
            description.text = str(card['description'])
            my_data = ET.tostring(r, encoding='utf-8')
            file = open('outs2.xml', 'wb')
            file.write(my_data)
        i += 1




if __name__ == "__main__":
    main()
