import asyncio
import time
from pprint import pp
import xml.etree.ElementTree as ET
from typing import TypedDict
import bs4.element
import requests
from bs4 import BeautifulSoup
import aiohttp
from bs4 import BeautifulSoup
import tqdm
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}


def get_card_urls() -> list:
    urls = []
    tree = ET.parse('VendorYML.xml')
    root = tree.getroot()
    for child in root.findall('vendor'):
        models = child.find('models')
        for model in models:
            urls.append(model.find('promoUrl').text)
    return urls


async def parse_card(card_url: str, session: aiohttp.client.ClientSession) -> None:
    async with session.get(card_url, headers=headers, timeout=5) as req:
        src = await req.read()
        soup = BeautifulSoup(src, 'lxml')
        try:
            code = soup.find('span', class_='product_code_by_font').text
        except:
            code = ''
        try:
            description = soup.find('div', class_='clear_styles')

        except:
            description = ''
        try:
            images = description.find_all('img')
            for image in images:
                try:
                    image_src = image['src'].replace('../', 'https://www.fortu.ru/')
                    image['src'] = image_src
                except:
                    pass
        except:
            pass
        card_xml = ET.SubElement(r, 'card')

        code_xml = ET.SubElement(card_xml, 'code')
        code_xml.text = str(code)

        description_xml = ET.SubElement(card_xml, 'description')
        description_xml.text = str(description)
        my_data = ET.tostring(r, encoding='utf-8')
        file = open('out55.xml', 'wb')
        file.write(my_data)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in get_card_urls():
            task = asyncio.create_task(parse_card(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)
        # pbar = tqdm.tqdm(total=len(tasks))
        # for f in asyncio.as_completed(tasks):
        #     value = await f
        #     pbar.set_description(value)
        #     pbar.update()


if __name__ == '__main__':
    r = ET.Element('cards')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
