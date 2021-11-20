import openpyxl
import requests
import os
from bs4 import BeautifulSoup

data = input("[+] Введите название таблицы входных данных (пример data.xlsx):  ")
table = openpyxl.open(data, read_only=True)
new_book = openpyxl.Workbook()
if os.path.exists('gulliver-media'):
    pass
else:
    os.mkdir('gulliver-media')

sheet = table.active
new_sheet = new_book.active

new_sheet['A1'].value = 'code'
new_sheet['B1'].value = 'description'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}
description = ''
for row in range(1, sheet.max_row):
    code = sheet[row][0].value
    if code is not None:
        url = f'https://www.gulliver.ru/search?q={code}'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        nothing = soup.find(class_='title__text').text
        if 'ничего не нашлось' in nothing:
            print(nothing.strip())
        else:
            item_link = soup.find(class_="catalog-block__card").find("a").get("href")
            req = requests.get(item_link, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            description = soup.find(class_="product__description-text").text.strip()

            photos_link = soup.find(class_='swiper-wrapper').find_all(class_='swiper-slide')
            i = 0
            for photo in photos_link:
                photo_link = photo.find('img').get('data-src')
                req_photo = requests.get(url=photo_link, headers=headers)
                response = req_photo.content
                if i == 0:
                    with open(f'gulliver/gulliver-media/{code}.jpg', 'wb') as file:
                        file.write(response)
                elif i >= 10:
                    print('Фото больше 10')
                else:
                    with open(f'gulliver/gulliver-media/{code}-{i}.jpg', 'wb') as file:
                        file.write(response)
                i = i + 1
        if code is not None:
            new_sheet[row + 1][0].value = code
            new_sheet[row + 1][1].value = description

new_book.save('gulliver-output.xlsx')
new_book.close()
