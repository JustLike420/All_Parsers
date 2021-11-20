import os
import time
from slugify import slugify
import openpyxl
import requests
from bs4 import BeautifulSoup

REGION = 'nsk'  # пустое поле - Москва

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': '*/*'
}
new_book = openpyxl.Workbook()
new_sheet = new_book.active
new_sheet['A1'].value = 'Название'
new_sheet['B1'].value = 'Организатор'
new_sheet['C1'].value = 'Место'
new_sheet['D1'].value = 'Продолжительность'
new_sheet['E1'].value = 'Описание'
new_sheet['F1'].value = 'Название фото'
new_sheet['G1'].value = 'ShowID'
if os.path.exists('media'):
    pass
else:
    os.mkdir('media')


def get_search(text):
    search_url = f'https://{REGION}.ticketland.ru/search/performance/?text={text}'
    req = requests.get(search_url, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        last_page = soup.find_all('li', class_='search-pagination__item')[-1].get('data-page-count')
        for i in range(1, int(last_page) + 1):
            search_url = f'https://nsk.ticketland.ru/search/performance/?text={text}&page={i}'
            req = requests.get(search_url, headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            cards = soup.find_all(class_='card-search')
            for card in cards:
                card_url = 'https://nsk.ticketland.ru' + card.find('a').get('href')
                get_data(card_url)
                time.sleep(1)
            time.sleep(2)
    except:
        search_url = f'https://nsk.ticketland.ru/search/performance/?text={text}'
        req = requests.get(search_url, headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        cards = soup.find_all(class_='card-search')
        if len(cards) == 0:
            new_sheet.append([text])
            print(f'{text} не найдено.')
            new_book.save(f'События-{REGION}.xlsx')
        for card in cards:
            card_url = 'https://nsk.ticketland.ru' + card.find('a').get('href')
            get_data(card_url)
            time.sleep(1)
        time.sleep(2)


def get_data(url):
    req = requests.get(url, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    name = soup.find('h1', itemprop="name").text
    try:
        time = soup.find(class_='description').find_all(class_='mb-2')[1].find('span').text.strip()
    except:
        time = ''
    photo_name = slugify(name)
    description = soup.find('div', itemprop="description").text.strip()
    organizer = soup.find('span', itemprop="organizer").text.strip()
    place = soup.find('span', class_='show-card__building').text.strip()
    showid = soup.find(class_='social').get('id').replace('share_', '')

    try:
        photo_url = soup.find('ul', class_='slides').find('li').find('img').get('data-src')
        req_photo = requests.get(url='https://' + photo_url[2:], headers=headers)
        response = req_photo.content
        with open(f'media/{photo_name}.jpg', 'wb') as file:
            file.write(response)
    except:
        photo_name = 'Нету'
    new_sheet.append([name, organizer, place, time, description, photo_name + '.jpg', showid])
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
