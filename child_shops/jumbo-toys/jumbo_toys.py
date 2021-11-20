import openpyxl
import requests
import os
from bs4 import BeautifulSoup

data = input("[+] Write filename (data.xlsx): ")

table = openpyxl.open(data, read_only=True)
new_book = openpyxl.Workbook()
if os.path.exists('jumbo-toys-media'):
    pass
else:
    os.mkdir('jumbo-toys-media')
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
        url = f'https://jumbo-toys.ru/catalog/?SEARCH_SECTION=0&q={code}'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        try:
            item_link = 'https://jumbo-toys.ru' + soup.find(class_='product__name').get('href')
            nothing = True
        except:
            nothing = False
        if nothing:
            req = requests.get(item_link, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            description = soup.find(class_="product__text").text.strip()
            if 'Торговая марка' in description:
                description = 'НЕТ ОПИСАНИЯ'
            photos_link = soup.find_all(class_='slider-pimagebig__slide')
            i = 0
            for photo in photos_link:
                photo_link = 'https://jumbo-toys.ru' + photo.get('href')
                req_photo = requests.get(url=photo_link, headers=headers)
                response = req_photo.content
                if i == 0:
                    with open(f'jumbo-toys-media/{code}.jpg', 'wb') as file:
                        file.write(response)
                elif i >= 10:
                    print(f'Фото больше 10 {code}')
                else:
                    with open(f'jumbo-toys-media/{code}-{i}.jpg', 'wb') as file:
                        file.write(response)
                i = i + 1
        if code is not None:
            if nothing:
                print(code, 'saved')
                new_sheet[row + 1][0].value = code
                new_sheet[row + 1][1].value = description
            else:
                print(code, 'none')
new_book.save('jumbo-toys-output.xlsx')
new_book.close()
print('Done.')