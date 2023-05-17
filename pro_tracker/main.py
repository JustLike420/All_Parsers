import re

import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://www.dota2protracker.com/hero/Void%20Spirit#'
    src = requests.get(url)
    soup = BeautifulSoup(src.text, 'lxml')
    table = soup.find('table', class_='alx_table sort-fd')
    with open('result.txt', 'w', encoding='utf-8') as file:
        for i, tr in enumerate(table.find_all('tr')[1:]):
            pwh = tr.get('pwh')
            pah = tr.get('pah')
            items = '\n'.join(tr.get('items').split(','))
            skills = []
            for image in tr.find('div', class_='table-column-skillbuild').find_all('img'):
                match = re.search(r"/([^/]+)\.png$", image.get('src'))
                if match:
                    skill = match.group(1)
                    skills.append(skill.replace('void_spirit_', ''))
            skills = '\n'.join(skills)
            duration = tr.find('td', class_='td-dur').text
            mmr = tr.find('td', class_='td-imp').text

            match = f"{i + 1})\ndraft\nсоюзный пик\n{pwh}\nвражеский пик\n{pah}\n\n" \
                    f"item build\n{items}\n\nAbilities until lvl10\n\n{skills}\n\nduration\n{duration}\n\nIPM {mmr}\n\n"
            file.write(match)


if __name__ == "__main__":
    main()
