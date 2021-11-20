import openpyxl
import requests
import os
from bs4 import BeautifulSoup

data = input("[+] Введите название таблицы входных данных (пример data.xlsx):  ")
table = openpyxl.open(data, read_only=True)
new_book = openpyxl.Workbook()
if os.path.exists('onetoyshop-media'):
    pass
else:
    os.mkdir('onetoyshop-media')

sheet = table.active
new_sheet = new_book.active

new_sheet['A1'].value = 'code'
new_sheet['B1'].value = 'description'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': '*/*'
}
description = ''
for row in range(2, sheet.max_row+1):
    code = sheet[row][0].value
    if code is not None:
        url = f'https://onetoyshop.ru/search/?q={code}'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        try:
            item_link = 'https://onetoyshop.ru' + soup.find(class_='name').find('a').get('href')
            nothing = True
        except:
            nothing = False
        if nothing:
            req = requests.get(item_link, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            description = soup.find(class_='detail_text').text.strip()
            photos_link = soup.find(class_='big_product_slider').find_all('img')
            i = 0
            for photo in photos_link:
                photo_link = 'https://onetoyshop.ru' + photo.get('src')
                req_photo = requests.get(url=photo_link, headers=headers)
                response = req_photo.content
                if i == 0:
                    with open(f'onetoyshop-media/{code}.jpg', 'wb') as file:
                        file.write(response)
                elif i >= 10:
                    print('Фото больше 10')
                else:
                    with open(f'onetoyshop-media/{code}-{i}.jpg', 'wb') as file:
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

new_book.save('onetoyshop-output.xlsx')
new_book.close()
print('Done.')
