import requests
from bs4 import BeautifulSoup
import openpyxl
import aiohttp
import asyncio

headers = {
    # куки с логином/паролем
    'cookie': '_ym_debug=null; PHPSESSID=lttrhNnN5tUNnS3mtOtlDlKINYDY1okp; BITRIX_SM_SOUND_LOGIN_PLAYED=Y; _ym_debug=null',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}

new_book = openpyxl.Workbook()
new_sheet = new_book.active

new_sheet['A1'].value = 'ФИО'
new_sheet['B1'].value = 'номер телефона'
new_sheet['C1'].value = 'пол'
new_sheet['D1'].value = 'возраст'
new_sheet['E1'].value = 'ссылка на анкету'


async def main():
    for PAGIN in range(1, 455):
        req = requests.get(
            f'https://всекастинги.рф/job-seekers/?arrFilter_pf%5BSEX%5D=&arrFilter_pf%5BCITY%5D=1301&arrFilter_pf%5BBIRTH%5D=&arrFilter_pf%5BHEIGHT%5D%5BLEFT%5D=&arrFilter_pf%5BHEIGHT%5D%5BRIGHT%5D=&arrFilter_pf%5BWEIGHT%5D%5BLEFT%5D=&arrFilter_pf%5BWEIGHT%5D%5BRIGHT%5D=&arrFilter_ff%5BSECTION_ID%5D=576&arrFilter_ff%5BNAME%5D=&set_filter=Y&PAGEN_1={PAGIN}',
            headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        cards = soup.find_all(class_='card__name')
        card_urls = []
        for card in cards:
            card_url = 'https://xn--80adegqbk0a5adl.xn--p1ai' + card['href']
            card_urls.append(card_url)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in card_urls:
                task = asyncio.create_task(parse_card(url, session))
                tasks.append(task)
            result = await asyncio.gather(*tasks)



async def parse_card(card_url, session):
    async with session.get(card_url, headers=headers) as req:
        # req = requests.get(card_url, headers=headers)
        src = await req.read()
        # print(src)
        soup = BeautifulSoup(src, 'lxml')
        full_name = soup.find(class_='subject-card__title').text.strip()

        card_details = soup.find_all(class_='subject-card__info-data-value')
        sex = card_details[1].text.strip()
        if sex == 'Жен.':
            sex = 'Женский'
        elif sex == 'Муж.':
            sex = 'Мужской'
        age = card_details[0].text.strip()
        # где-то есть 2 номера
        phone_number = card_details[5].text.strip().split(' ')[0]
        line = [full_name, phone_number, sex, age, card_url]
        new_sheet.append(line)
        new_book.save(f'Всекастинги.xlsx')
        print(full_name, age, sex, phone_number)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
