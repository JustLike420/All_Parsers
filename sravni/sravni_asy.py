import os
import time
import datetime
import openpyxl
import requests
from bs4 import BeautifulSoup

import asyncio
import aiohttp

new_book = openpyxl.Workbook()
new_sheet = new_book.active

today = datetime.datetime.now()
today = today.strftime('%d.%m.%Y-%H.%M.%S')

new_sheet['A1'].value = 'Номер п/п'
new_sheet['B1'].value = 'Автор'
new_sheet['C1'].value = 'Город'
new_sheet['D1'].value = 'Дата публикации'
new_sheet['E1'].value = 'Страховая'
new_sheet['F1'].value = 'Оценка'
new_sheet['G1'].value = 'Заголовок отзыва'
new_sheet['H1'].value = 'Текст отзыва'
new_sheet['I1'].value = 'Сервис'
new_sheet['J1'].value = 'Ссылка на отзыв'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': '*/*'
}
s = {
    'count': 1,
}

def get_data(url):
    req = requests.get(url, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all(class_='sc-1fxln1u-2')
    for card in cards:

        author = card.find(class_='sc-1fxln1u-17').find_all('span')[0].text.replace(', ', '')
        city = card.find(class_='sc-1fxln1u-17').find_all('span')[1].text.replace(', ', '')
        """ Сделать перевод в 10.12.2021 """
        publication_date = card.find(class_='sc-1fxln1u-17').find_all('span')[2].text.replace(',', '')
        valueCompany = card.find(class_='jBnZGy').find('a').get('href').split('/')[2]
        if card.find('span', class_='sc-1eq8x10-0') is not None:
            review_grade = card.find(class_='sc-1eq8x10-1').text
        else:
            review_grade = ''
        if card.find(class_='sc-1fxln1u-19') is not None:
            review_title = card.find(class_='sc-1fxln1u-19').text
        else:
            review_title = ''
        # if card.find(class_='sc-1fxln1u-20').find('p') is not None:
        #     review_text = card.find(class_='sc-1fxln1u-20').find('p').text.strip()
        # else:
        #     review_text = ''
        review_text = ''
        service = card.find(class_='sc-1fxln1u-23').find('span').text.strip()
        review_link = 'https://www.sravni.ru' + card.find(class_='sc-1fxln1u-27').find('a').get('href')
        req1 = requests.get(review_link, headers)
        src1 = req1.text
        soup1 = BeautifulSoup(src1, 'lxml')
        try:
            review_text = soup1.find(class_='lpzn2g-13').find('p').text.strip()
        except:
            pass
        new_sheet.append(
            ['', author, city, publication_date, valueCompany, review_grade, review_title, review_text, service,
             review_link])
        s['count'] += 1
        print(f'[-] {review_title} | {review_link} | {s["count"]}')
    new_book.save(f'Отзывы - {today}.xlsx')

if __name__ == '__main__':
    for j in range(784, 1728):
        url = f'https://www.sravni.ru/strakhovye-kompanii/otzyvy/?page={j}'
        print(f'[+] PAGE - {j}')
        get_data(url)
        time.sleep(2)
    # get_data('https://www.sravni.ru/strakhovye-kompanii/otzyvy/')