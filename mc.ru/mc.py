import time
import openpyxl
import requests
from bs4 import BeautifulSoup
import datetime
new_book = openpyxl.Workbook()
new_sheet = new_book.active

new_sheet['A1'].value = ''
new_sheet['B1'].value = ''

table_links = openpyxl.open('ms.xlsx', read_only=True)
sheet = table_links.active
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': '*/*'
}

today = datetime.datetime.now()
today = today.strftime('%d.%m.%Y-%H.%M.%S')

i = 0
for row_links in range(1, sheet.max_row):
    url = sheet[row_links][0].value + '/PageAll/1'
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    table = soup.find(id='grid_tab').find_all('tr')

    for row in table:
        line = row.find_all('td')
        if i == 10:
            first_column = line[0].text.strip().replace('→', ' ') + line[2].text.strip() + line[3].text.strip()
            second_column = row.find_all('td', attrs={'data-price-val': '3'})[0].text.strip()
        else:
            first_column = line[0].text.strip().replace('→', ' ') + line[2].text.strip()
            second_column = row.find_all('td', attrs={'data-price-val': '2'})[0].text.strip()
        new_sheet[i + 1][0].value = first_column
        new_sheet[i + 1][1].value = second_column
        i = i + 1
    print(sheet[row_links][0].value, 'saved!')
    time.sleep(5)
new_book.save(f'ms_{today}.xlsx')
new_book.close()
print('Done.')

