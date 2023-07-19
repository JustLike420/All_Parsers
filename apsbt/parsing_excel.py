import requests
from bs4 import BeautifulSoup as Soup
import urllib3

urllib3.disable_warnings()

DIR_PATH = 'data/'


class Parser:
    def __init__(self, data: str):
        self.path = DIR_PATH
        self.data = {'data': 'results/market/' + data}

    def parse_files(self, html: str):
        soup = Soup(html, "html.parser")
        data_rows = soup.find_all('div', class_='xml-data-row')

        for row in data_rows:
            urls = row.find_all('a')
            for url in urls:
                href = url.get('href')
                file_title = href.split('/')[-1]
                response = requests.get(href, verify=False)
                with open(f'{self.path}{file_title}', 'wb') as f:
                    f.write(response.content)

    def run(self):
        self.get_data()
        response = requests.post('https://www.atsenergo.ru/js-data', data=self.data, verify=False)
        self.parse_files(response.text)

    def get_data(self):
        pass


class CalcfacthourParser(Parser):
    def get_data(self):
        response = requests.get(f'https://www.atsenergo.ru/{self.data["data"]}', data=self.data, verify=False)
        soup = Soup(response.text, "html.parser")
        option = soup.find('select', class_='periods').find('option')
        self.data['id'] = option.get('value')


class SvncParser(Parser):
    def get_data(self):
        response = requests.get(f'https://www.atsenergo.ru/{self.data["data"]}', data=self.data, verify=False)
        soup = Soup(response.text, "html.parser")
        option = soup.find('select', class_='periods').find('option')
        self.data['id'] = f'period={option.get("value")}&ftempl=3&step=1&published={option.get("data-published")}'


def get_nreport():
    url = 'https://www.atsenergo.ru/nreport?rname=FRSTF_ATS_REPORT_PUBLIC_FSK&rdate=20230601'
    response = requests.get(url, verify=False)
    soup = Soup(response.text, "html.parser")
    file_block = soup.find('div', class_='reports_files').find('a')
    file_title = file_block.text
    file_url = 'https://www.atsenergo.ru/nreport' + file_block.get('href')
    response = requests.get(file_url, verify=False)
    with open(f'{DIR_PATH}{file_title}', 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    calcfacthour = CalcfacthourParser(data='calcfacthour')
    calcfacthour.run()
    svnc = SvncParser(data='svnc')
    svnc.run()
    get_nreport()
