import openpyxl
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

new_book = openpyxl.Workbook()
new_sheet = new_book.active

new_sheet['A1'].value = 'ФИО'
new_sheet['B1'].value = 'номер телефона'
new_sheet['C1'].value = 'пол'
new_sheet['D1'].value = 'возраст'
new_sheet['E1'].value = 'ссылка на анкету'


def main():

    for PAGIN in range(1, 678):
        url = f'https://www.vsekastingi.ru/people/?user_city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&user_age=4&user_age2=&user_length=&user_length2=&user_weight=&user_weight2=&user_gr=&user_gr2=&user_ta=&user_ta2=&user_be=&user_be2=&user_boobs=&user_boobs2=&user_hair_color=&user_eye_color=&p={PAGIN}'
        req = requests.get(url, headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        cards = soup.find(class_='col-md-8').find('center').find_all('a')
        card_urls = []
        for card in cards:
            if 'https://' in card['href']:

                card_urls.append(card['href'])

        print(card_urls)
        print(PAGIN)
        for card in card_urls:
            parse_card(card)
        new_book.save('Все каситинги 2.xlsx')



def parse_card(url):
    with requests.Session() as s:
        s.auth = ('login', 'password')
        s.headers.update(headers)
        req = s.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        name = soup.find(class_='col-md-12').text.strip()
        phone = soup.find(class_='col-md-8').find_all('tr')[-2].find_all('td')[-1].text.strip()
        if phone == 'Контакты':
            phone = ''
        t = soup.find_all(class_='col-md-4')[4]
        table_body = t.find('table')
        rows = table_body.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        try:
            sex = data[2][1]
        except:
            sex = ''
        try:
            age = data[3][1]
        except:
            age = ''
        line = [name, phone, sex, age, url]
        new_sheet.append(line)
        print(line)
if __name__ == '__main__':
    main()
