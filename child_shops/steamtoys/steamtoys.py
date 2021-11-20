import os

import openpyxl
import requests
from bs4 import BeautifulSoup

data = input("[+] Введите название таблицы входных данных (пример data.xlsx):  ")
table = openpyxl.open(data, read_only=True)
new_book = openpyxl.Workbook()
if os.path.exists('steamtoys-media'):
    pass
else:
    os.mkdir('steamtoys-media')
sheet = table.active
new_sheet = new_book.active

new_sheet['A1'].value = 'code'
new_sheet['B1'].value = 'description'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': '*/*'
}
description = ''
for row in range(2, sheet.max_row + 1):
    code = sheet[row][0].value
    if code is not None:
        url = f'https://steamtoys.ru/catalog/?search={code}'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        try:
            item_link = 'https://steamtoys.ru' + soup.find(class_='product__name').find('a').get('href')
            nothing = True
        except:
            nothing = False
        if nothing:
            req = requests.get(item_link, headers=headers)
            src = req.text

            soup = BeautifulSoup(src, 'lxml')
            descriptions = soup.find(id='prod_detail_text').find_all('p')
            description = ''
            for d in descriptions:
                description = description + d.text.strip()
            photos_link = soup.find_all(class_='thumb__item')
            i = 0
            for photo in photos_link:
                if 'www.youtube.com' not in photo.get('href'):
                    photo_link = photo.get('href')
                    req_photo = requests.get(url=photo_link, headers=headers)
                    response = req_photo.content
                    if i == 0:
                        with open(f'steamtoys-media/{code}.jpg', 'wb') as file:
                            file.write(response)
                    elif i == 10:
                        print(f'{code} Фото больше 10')
                    elif i > 10:
                        pass
                    else:
                        with open(f'steamtoys-media/{code}-{i}.jpg', 'wb') as file:
                            file.write(response)
                    i = i + 1
        if code is not None:
            if nothing:
                print(code, 'saved')
                new_sheet[row][0].value = code
                new_sheet[row][1].value = description
            else:
                new_sheet[row][0].value = code
                new_sheet[row][1].value = 'Артикул не найден'
                print(code, 'none')
new_book.save('steamtoys-output.xlsx')
new_book.close()
print('Done.')
