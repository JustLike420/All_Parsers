import os

import openpyxl
import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

if os.path.exists('media') is False:
    os.mkdir('media')

new_book = openpyxl.Workbook()
new_sheet = new_book.active
new_sheet['A1'].value = 'name'
new_sheet['B1'].value = 'makes'
new_sheet['C1'].value = 'models'
new_sheet['D1'].value = 'breadcrumbs'
new_sheet['E1'].value = 'images'
new_sheet['F1'].value = 'url'

def get_links():
    pages = 395
    with open('links.txt', 'w+', encoding='utf-8') as file:
        for page in range(1, pages + 1):
            url = 'https://protuning.com/en/products?page=1&per_page=36&order_by=popular&layout=blocks'

            req = requests.get(url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            blocks = soup.find_all('div', class_='product-block-wrapper')
            for block in blocks:
                block_href = 'https://protuning.com' + block.find('a').get('href')
                file.write(block_href + '\n')
            print(str(page) + '/' + str(pages))


def parse_card(url):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    blocks = soup.find_all('div', class_='col-md-6 col-lg-6')
    # left_block = blocks[0]
    right_block = blocks[1]

    name = right_block.find('h1').text.strip()
    code = url.replace('https://protuning.com/en/', '').split('-')[0]

    try:
        compatibility_block = right_block.find('table')
        makes = compatibility_block.find_all('tr')[0].find('td').text
        models = compatibility_block.find_all('tr')[1].find('td').text
    except:
        makes, models = '', ''
    try:
        breadcrumbs = soup.find('div', class_='breadcrumbs').find('div', class_='hidden-xs hidden-sm').text.strip().replace(
        '\n\n', '->')
    except:
        breadcrumbs = ''

    images = json.loads(soup.find('div', class_='images-container js-images').get('data-images'))
    images_names = ''
    i = 0
    for image in images:
        photo_link = image['src']
        req_photo = requests.get(url=photo_link, headers=headers)
        response = req_photo.content
        with open(f'media/{code}-{i}.jpg', 'wb') as file:
            file.write(response)
            i += 1
            images_names += f'{code}-{i}.jpg, '
    new_sheet.append((name, makes, models, breadcrumbs, images_names, url))
    new_book.save('output_data1.xlsx')

if __name__ == "__main__":
    # get_links() - all links for cards
    with open('links.txt', 'r', encoding='utf-8') as file_links:
        links = file_links.readlines()
        for link in links:
            print(link)
            parse_card(link)
