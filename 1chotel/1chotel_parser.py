import openpyxl
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
new_book = openpyxl.Workbook()
new_sheet = new_book.active
new_sheet['A1'].value = 'Категория'
new_sheet['B1'].value = 'Название'
new_sheet['C1'].value = 'Город'
new_sheet['D1'].value = 'Кол-во номеров'
new_sheet['E1'].value = 'Сылка'
url_list = ['http://1chotel.ru/clients/business-hotel/', 'http://1chotel.ru/clients/resort/',
            'http://1chotel.ru/clients/chains/', 'http://1chotel.ru/clients/mini-hotel/',
            'http://1chotel.ru/clients/hostel/']

for url in url_list:
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        pages = int(soup.find_all('a', class_='page')[-1].text)
    except:
        pages = 1
    for i in range(1, pages+1):
        url_ = url + f'?page={i}'
        print(url_)
        req = requests.get(url_, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        hotel_list = soup.find('div', class_='client-list').find_all('div', class_='info')
        for hotel in hotel_list:
            name = hotel.find('div', class_='name').text
            features = hotel.find_all('div', class_='feature')
            # for feature in features:
            for feature in features:
                if feature.find('div', class_='feature-name').text == 'Город:':
                    country = feature.find('div', class_='feature-value').text
                elif feature.find('div', class_='feature-name').text == 'Количество номеров:':
                    count_rooms = feature.find('div', class_='feature-value').text
            try:
                link = hotel.find('a', class_='link').text
            except:
                link = ''
            print(url.split('/')[-2])
            data = {
                'business-hotel': 'Бизнес-отель',
                'resort': 'Курорт',
                'chains': 'Сеть отелей',
                'mini-hotel': 'Мини-отель',
                'hostel': 'hostel'
            }
            new_sheet.append((data.get(url.split('/')[-2]), name, country, count_rooms, link))
            print((data.get(url.split('/')[-2]), name, country, count_rooms, link))
new_book.save('text.xlsx')
