import os
import time

import openpyxl
import requests
from bs4 import BeautifulSoup

data = input("[+] Введите название таблицы входных данных (пример data.xlsx):  ")
table = openpyxl.open(data, read_only=True)
new_book = openpyxl.Workbook()
if os.path.exists('toysfest-media'):
    pass
else:
    os.mkdir('toysfest-media')
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
        url = f'https://www.toysfest.ru/search/?q={code}'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        item_link = 'https://www.toysfest.ru' + soup.find(class_='prod-card--title').find('a').get('href')
        if item_link != 'https://www.toysfest.ru#':
            nothing = True
            req = requests.get(item_link, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            description = soup.find(itemprop='description').text.strip()
            photos_link = soup.find_all(class_='slide')
            i = 0
            for photo in photos_link:
                photo_link = photo.find('a')
                if photo_link is not None:
                    photo_url = photo_link.get('data-image')
                    if photo_url != '.jpg':
                        req_photo = requests.get(url=photo_url, headers=headers)
                        response = req_photo.content
                        if i == 0:
                            with open(f'toysfest-media/{code}.jpg', 'wb') as file:
                                file.write(response)
                        elif i == 10:
                            print(f'{code} Фото больше 10')
                        elif i > 10:
                            pass
                        else:
                            with open(f'toysfest-media/{code}-{i}.jpg', 'wb') as file:
                                file.write(response)
                        i = i + 1
                    else:
                        print('no photo')
        else:
            nothing = False
        if nothing:
            print(code, 'saved')
            new_sheet[row][0].value = code
            new_sheet[row][1].value = description
        else:
            new_sheet[row][0].value = code
            new_sheet[row][1].value = 'Артикул не найден'
            print(code, 'none')
        time.sleep(2)
new_book.save('toysfest-output.xlsx')
new_book.close()
print('Done.')