import os
import time
from slugify import slugify
import openpyxl
import requests
from bs4 import BeautifulSoup

REGION = 'sochi'

if os.path.exists('media'):
    pass
else:
    os.mkdir('media')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': '*/*'
}

new_book = openpyxl.Workbook()
new_sheet = new_book.active
new_sheet['A1'].value = 'Название'
new_sheet['B1'].value = 'Организатор'
new_sheet['C1'].value = 'Место'
new_sheet['D1'].value = 'Описание'
new_sheet['E1'].value = 'Название фото'


def get_search(text):
    search_url = f'https://{REGION}.kassy.ru/search/?text={text}'
    req = requests.get(search_url, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        search_result = soup.find('div', id='page').find('div', class_='content').text.strip()
    except:
        search_result = 's'
    nothing = 'Не найдено ни одного мероприятия, содержащего искомую фразу'
    if search_result != nothing:
        cards = soup.find('div', id='page').find('ul', class_='events').find_all('li')
        for card in cards:
            card_url = f'https://{REGION}.kassy.ru' + card.find('h2').find('a').get('href')
            get_data(card_url)
    else:
        new_sheet.append([text])
        print(f'{text} не найдено.')
        new_book.save(f'События-{REGION}.xlsx')

def get_data(url):
    req = requests.get(url, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    name = soup.find('div', id='page').find('h1').find('a').text.strip()
    organizer = soup.find('div', id='organizer_info').text.strip().split('\n')[0].replace('Организатор: ', '')
    if len(soup.find('div', id='page').find(class_='venue').find_all('a')) == 1:
        place = soup.find('div', id='page').find(class_='venue').find_all('a')[0].text
    else:
        place = soup.find('div', id='page').find(class_='venue').find_all('a')[1].text
    if len(soup.find('div', id='page').find(class_='content').find_all('p')) != 2:
        description = soup.find('div', id='page').find(class_='content').find_all('p')[2].text.strip()
    else:
        description = ''

    photo_name = slugify(name) + '.jpg'
    try:
        img_url = f'https://{REGION}.kassy.ru' + soup.find('div', class_='img').find('a').get('href')
        req_photo = requests.get(url=img_url, headers=headers)
        response = req_photo.content
        with open(f'media/{photo_name}', 'wb') as file:
            file.write(response)

    except:
        photo_name = 'Нету'
    new_sheet.append([name, organizer, place, description, photo_name])
    print(f'{name} добавлен.')
    new_book.save(f'События-{REGION}.xlsx')


if __name__ == '__main__':
    data = input("[+] Введите название таблицы входных данных (пример data.xlsx):  ")
    table = openpyxl.open(f'{data}', read_only=True)
    sheet = table.active
    for row in range(2, sheet.max_row + 1):
        text = sheet[row][0].value
        if text is not None:
            get_search(text)

    new_book.close()
