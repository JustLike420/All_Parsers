import os
import openpyxl
import requests
from bs4 import BeautifulSoup

data = input("[+] Введите название таблицы входных данных (пример data.xlsx):  ")
table = openpyxl.open(data, read_only=True)
new_book = openpyxl.Workbook()
if os.path.exists('toyway-media'):
    pass
else:
    os.mkdir('toyway-media')
sheet = table.active
new_sheet = new_book.active

new_sheet['A1'].value = 'code'
new_sheet['B1'].value = 'description'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': '*/*'
}
description = ''
# code = 'e0783'
for row in range(2, sheet.max_row + 1):
    code = sheet[row][0].value
    if code is not None:
        url = f'https://www.toyway.ru/search/?q={code}&search='
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        search = soup.find_all(class_='catalog-item-desc')
        if len(search) != 0:
            for item in search:

                for span in item.find_all('span'):
                    if f'Артикул: {code}' in span.text:
                        item_link = 'https://www.toyway.ru' + item.find(class_='catalog-item-title').find('a').get('href')
            nothing = True
        else:
            nothing = False
        if nothing:
            req = requests.get(item_link, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            descriptions = soup.find(itemprop='description').find_all('p')
            description = ''
            for d in descriptions:
                description = description + d.text.strip()
            photos_link = soup.find_all(class_='catalog_detail')
            i = 0
            for photo in photos_link[0].find_all('a'):
                one_image = photo.get('data-src')
                if one_image is not None:
                    photo_link = 'https://www.toyway.ru' + one_image
                    req_photo = requests.get(url=photo_link, headers=headers)
                    response = req_photo.content
                    if i == 0:
                        with open(f'toyway-media/{code}.jpg', 'wb') as file:
                            file.write(response)
                    elif i == 10:
                        print(f'{code} Фото больше 10')
                    elif i > 10:
                        pass
                    else:
                        with open(f'toyway-media/{code}-{i}.jpg', 'wb') as file:
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
new_book.save('toyway-output.xlsx')
new_book.close()
print('Done.')
