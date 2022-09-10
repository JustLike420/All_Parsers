import openpyxl
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
def parse_card(url):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    name = soup.find('h1', itemprop='name').text.strip()
    containers = soup.find_all('div', class_='dailyprice-container')
    line = [name]
    for container in containers:
        price = container.find('div', class_='price-container').text.strip()
        date = container.find('div', class_='delivery-container').text.strip()
        count = container.find('div', class_='quantity-container').text.strip()
        line.extend([price, date, count])
        print(name, price, date, count)
    return line
def get_link(atr, creator):
    url = f'https://aeromotors.ee/ru/kataloog/search?search_query={atr}'
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        lis = soup.find('label', string=re.compile(creator)).attrs['for'].replace('layered_2_', '')
        url = f'https://aeromotors.ee/ru/kataloog/search?layered_id_feature_2%5B0%5D={lis}&search_query={atr}'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        blocks = soup.find_all('div', class_='tdlist-row')
        for block in blocks:
            block_atr = block.find('div', class_='article-number').text.replace(' ', '')
            if block_atr == str(atr):
                link = block.find('a', class_='article-name').get('href')
        print(link, atr, creator)
        line = parse_card(link)
        return line
    except:
        print(atr, creator, 'no info')
        return None

if __name__ == '__main__':
    while True:
        table = openpyxl.open(f'data.xlsx')
        sheet = table.active
        for row in range(2, sheet.max_row + 1):
            creator = sheet[row][0].value
            atr = sheet[row][1].value
            if creator is not None:
                line = get_link(atr, creator)
                if line is not None:
                    for i, el in enumerate(line):
                        sheet.cell(row=row, column=i+3).value = el
            table.save('data1.xlsx')