import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger

logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')


def convert_workbook():
    from openpyxl import Workbook
    import csv
    wb = Workbook()
    ws = wb.active
    with open('result.csv', 'r') as f:
        for row in csv.reader(f):
            ws.append(row)
    wb.save('result.xlsx')


class Gis:
    def __init__(self):
        self.url = 'https://2gis.ru/n_urengoy/search/%D1%81%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8'
        self.stream = open("result.csv", "w", newline='')
        self.writer = csv.writer(self.stream)
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument(r"user-data-dir=C:\Users\Vladimir\PycharmProjects\All_Parsers\User Data")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )

        self.iter = 1

    def write_data(self, **kwargs) -> None:
        """Запись информации в файл"""
        if kwargs['links'] is not None:
            whats_links = ' '.join(kwargs['links'])
            whats_count = len(kwargs['links'])
        else:
            whats_links = ''
            whats_count = 0
        self.writer.writerow(
            [kwargs['title'], kwargs['page_url'], whats_links])
        logger.info(f'Write = {kwargs["title"]} {self.iter} {whats_count}')
        self.iter += 1

    def get_page_number(self):
        page = 1
        self.driver.get(f"{self.url}")
        try:
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/footer/div[2]').click()
        except:
            pass
        while True:
            try:
                right_button = self.driver.find_element(By.XPATH,
                '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div[2]/div[2]')
                ActionChains(self.driver).move_to_element(right_button).click(right_button).perform()
                page += 1
            except Exception as e:
                print(e)
                return page

    def run(self):
        all_cards = []
        pages_count = self.get_page_number()
        pages = [i for i in range(1, pages_count)]
        for page in pages:
            self.driver.get(f"{self.url}/page/{page}")
            src = self.driver.page_source
            bs = BeautifulSoup(src, 'lxml')
            cards = bs.find_all('div', class_='_1h3cgic')
            for card in cards:
                card_href = card.find('a').get('href').split('?stat')[0]
                all_cards.append(card_href)
        logger.info(f'Найдено {len(all_cards)}\n')
        logger.info('Запуск...')
        for card in all_cards:
            card_id = card.split('/')[-1]
            self.single(card_id)

    def single(self, card_id):
        page_url = f'https://2gis.ru/n_urengoy/firm/{card_id}'
        self.driver.get(page_url)
        src = self.driver.page_source
        links = self.get_whatsapp_links(src)
        bs = BeautifulSoup(src, 'lxml')
        title = bs.find('h1', class_='_d9xbeh').text
        self.write_data(title=title, page_url=page_url, links=links)

    @staticmethod
    def get_whatsapp_links(src):
        import re
        bs = BeautifulSoup(src, 'lxml')
        for script in bs.find_all('script'):
            pattern = re.compile(r"https:\/\/wa\.me\/\d+")
            match = pattern.findall(str(script))
            if match:
                return list(set(match))


if __name__ == '__main__':
    a = Gis()
    a.run()
    a.driver.close()
    a.stream.close()
    convert_workbook()
