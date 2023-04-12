import csv
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# from seleniumwire import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from fake_useragent import UserAgent


class Avito:
    def __init__(self):
        self.url = 'https://www.avito.ru/user/5b78bcea90680289e2d26b009372a9d0/profile?src=search_seller_info'
        self.stream = open("result.csv", "w", newline='', encoding='utf-8')
        self.writer = csv.writer(self.stream)
        self.options = webdriver.ChromeOptions()
        useragent = UserAgent(verify_ssl=False)
        USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36"
        self.options.add_argument(USER_AGENT)
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        # self.options.add_argument(r"user-data-dir=C:\Users\Vladimir\PycharmProjects\All_Parsers\User Data")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                          '''
        })
        self.stream = open("result.csv", "w", newline='')
        self.domain = 'https://www.avito.ru'
        self.urls = self.urls = ['/orehovo-zuevo/kvartiry/2-k._kvartira_46m_25et._1883651285',
                     '/balashiha/kvartiry/1-k._kvartira_42m_89et._2619560132',
                     '/elektrostal/kvartiry/kvartira-studiya_37m_610et._2331069753',
                     '/noginsk/kvartiry/kvartira-studiya_33m_1117et._1914987690',
                     '/noginsk/kvartiry/2-k._kvartira_60m_217et._2139272337',
                     '/elektrostal/kvartiry/kvartira-studiya_30m_610et._2363329071',
                     '/noginsk/kvartiry/kvartira-studiya_38m_1617et._1883451455',
                     '/pavlovskiy_posad/kvartiry/1-k._kvartira_44m_217et._1947753081',
                     '/staraya_kupavna/kvartiry/kvartira-studiya_33m_417et._2331221595',
                     '/noginsk/kvartiry/2-k._kvartira_60m_1717et._2107041111',
                     '/noginsk/kvartiry/kvartira-studiya_39m_1017et._1883632353',
                     '/staraya_kupavna/kvartiry/kvartira-studiya_33m_917et._2171019412',
                     '/orehovo-zuevo/kvartiry/2-k._kvartira_46m_25et._1883651285',
                     '/balashiha/kvartiry/1-k._kvartira_42m_89et._2619560132',
                     '/elektrostal/kvartiry/kvartira-studiya_37m_610et._2331069753',
                     '/noginsk/kvartiry/kvartira-studiya_33m_1117et._1914987690',
                     '/noginsk/kvartiry/2-k._kvartira_60m_217et._2139272337',
                     '/elektrostal/kvartiry/kvartira-studiya_30m_610et._2363329071',
                     '/noginsk/kvartiry/kvartira-studiya_38m_1617et._1883451455',
                     '/pavlovskiy_posad/kvartiry/1-k._kvartira_44m_217et._1947753081',
                     '/staraya_kupavna/kvartiry/kvartira-studiya_33m_417et._2331221595',
                     '/noginsk/kvartiry/2-k._kvartira_60m_1717et._2107041111',
                     '/noginsk/kvartiry/kvartira-studiya_39m_1017et._1883632353',
                     '/staraya_kupavna/kvartiry/kvartira-studiya_33m_917et._2171019412',
                     '/staraya_kupavna/kvartiry/kvartira-studiya_28m_217et._2395404385',
                     '/pavlovskiy_posad/kvartiry/1-k._kvartira_46m_710et._1883313626',
                     '/noginsk/kvartiry/kvartira-studiya_36m_1112et._2011556269',
                     '/noginsk/kvartiry/1-k._kvartira_44m_1017et._1883783408',
                     '/staraya_kupavna/kvartiry/1-k._kvartira_40m_817et._1947122791',
                     '/elektrostal/kvartiry/1-k._kvartira_39m_810et._1851921622',
                     '/staraya_kupavna/kvartiry/1-k._kvartira_36m_217et._2330981744',
                     '/elektrostal/kvartiry/2-k._kvartira_68m_917et._1915687690',
                     '/noginsk/kvartiry/2-k._kvartira_59m_1117et._2139061802',
                     '/elektrostal/kvartiry/2-k._kvartira_60m_99et._2267042600',
                     '/elektrostal/kvartiry/kvartira-studiya_25m_810et._2619003640',
                     '/orehovo-zuevo/kvartiry/1-k._kvartira_38m_39et._1883630738',
                     '/balashiha/kvartiry/1-k._kvartira_47m_1417et._2843572887',
                     '/balashiha/kvartiry/2-k._kvartira_54m_59et._2874944198',
                     '/obuhovo/kvartiry/2-k._kvartira_59m_710et._2330888344',
                     '/noginsk/kvartiry/2-k._kvartira_58m_1017et._1008842413',
                     '/elektrogorsk/kvartiry/2-k._kvartira_60m_39et._1883060386',
                     '/chernogolovka/kvartiry/2-k._kvartira_60m_59et._2138994363',
                     '/orehovo-zuevo/kvartiry/1-k._kvartira_40m_510et._2298988703',
                     '/orehovo-zuevo/kvartiry/1-k._kvartira_31m_35et._1851104293',
                     '/elektrostal/kvartiry/kvartira-studiya_30m_810et._2395270216',
                     '/elektrostal/kvartiry/1-k._kvartira_43m_117et._2043718517',
                     '/elektrostal/kvartiry/2-k._kvartira_70m_1317et._2075717902',
                     '/noginsk/kvartiry/2-k._kvartira_59m_1017et._2107251058',
                     '/elektrostal/kvartiry/1-k._kvartira_46m_612et._2619191091',
                     '/orehovo-zuevo/kvartiry/snimu_2-k._kvartiru_2043135684',
                     '/schelkovo/kvartiry/snimu_1-k._kvartiru_2043073303',
                     '/korolev/kvartiry/snimu_1-k._kvartiru_2043003410',
                     '/pavlovskiy_posad/kvartiry/snimu_1-k._kvartiru_2363672413',
                     '/balashiha/kvartiry/snimu_1-k._kvartiru_1915588445',
                     '/mytischi/kvartiry/snimu_1-k._kvartiru_2043457812',
                     '/pavlovskiy_posad/kvartiry/1-k._kvartira_42m_1017et._2331036824',
                     '/noginsk/kvartiry/2-k._kvartira_46m_15et._1705657672',
                     '/pavlovskiy_posad/kvartiry/2-k._kvartira_65m_317et._2843360704',
                     '/elektrostal/kvartiry/1-k._kvartira_47m_617et._1883431260',
                     '/noginsk/kvartiry/1-k_kvartira_50_m_417_et._1883325957',
                     '/orehovo-zuevo/kvartiry/2-k_kvartira_62_m_210_et._1882952852',
                     '/elektrostal/kvartiry/2-k._kvartira_70m_417et._1883922933',
                     '/elektrostal/kvartiry/kvartira-studiya_30m_910et._2394926805',
                     '/pavlovskiy_posad/kvartiry/1-k._kvartira_45m_710et._1883008786',
                     '/noginsk/kvartiry/1-k._kvartira_41m_1517et._2714983443',
                     '/noginsk/kvartiry/2-k._kvartira_59m_1617et._2107643449',
                     '/elektrostal/kvartiry/2-k._kvartira_60m_710et._2362905903',
                     '/elektrostal/kvartiry/3-k._kvartira_70m_69et._2043503918',
                     '/pavlovskiy_posad/kvartiry/2-k._kvartira_60m_610et._2331368976',
                     '/balashiha/kvartiry/1-k._kvartira_41m_1217et._2619214941',
                     '/elektrostal/kvartiry/1-k._kvartira_37m_810et._1606863691',
                     '/staraya_kupavna/kvartiry/2-k._kvartira_67m_417et._2330977463',
                     '/staraya_kupavna/kvartiry/2-k._kvartira_65_m517_et._1883876908',
                     '/noginsk/kvartiry/2-k._kvartira_62m_39et._1883663432',
                     '/balashiha/kvartiry/1-k._kvartira_45m_45et._2619401812',
                     '/orehovo-zuevo/kvartiry/2-k._kvartira_48m_29et._1883611251',
                     '/elektrostal/kvartiry/1-k._kvartira_44m_717et._1787726090',
                     '/noginsk/kvartiry/1-k_kvartira_50_m_1117_et._1882966039',
                     '/elektrostal/kvartiry/2-k._kvartira_58_m710_et._1504972748',
                     '/noginsk/kvartiry/3-k_kvartira_82_m_317_et._1883164047',
                     '/orehovo-zuevo/kvartiry/1-k._kvartira_36m_25et._1883921822',
                     '/staraya_kupavna/kvartiry/1-k._kvartira_41m_35et._2331608611',
                     '/noginsk/kvartiry/1-k_kvartira_48_m_617_et._1618567619',
                     '/noginsk/kvartiry/2-k._kvartira_70m_1217et._1883715758']

    def run(self):
        self.driver.get(self.url)

    def page_product_links(self):
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        product_block = soup.find('div', class_='ProfileItemsGrid-root-eqOYi')
        product_links = product_block.find_all('a', class_='styles-link-cQMwi')
        links = [link.get('href') for link in product_links]
        return links

    def parse_product(self, url):
        data = {
            'Количество гостей:': None,
            'Можно с детьми:': None,
            'Можно с животными:': None,
            'Можно курить:': None,
            'Разрешены вечеринки:': None,
            'Есть отчётные документы:': None,
            'Количество комнат:': None,
            'Общая площадь:': None,
            'Этаж:': None,
            'Техника:': None,
            'Интернет и ТВ:': None,
            'Комфорт:': None,
            'Залог:': None,
            'Описание:': None,
            'Изображения': None,
            'Главное изображение': None,
            'Цена': None,
            'Адрес': None
        }
        self.driver.get(url)
        src = self.driver.page_source
        # data = []
        # with open('index.html', 'r', encoding='utf-8') as file:
        #     src = file.read()

        soup = BeautifulSoup(src, 'html.parser')
        about_table = soup.find('ul', class_='params-paramsList-zLpAu')
        rules = soup.find('ul', class_='style-item-params-list-_L3rx')
        about_li = about_table.find_all('li')
        rules_li = rules.find_all('li')
        for rule in rules_li:
            for d in data.keys():
                if d in rule.text:
                    data[d] = rule.text.replace(d, '')
        # data.extend([li.text for li in rules_li])
        for rule in about_li:
            for d in data.keys():
                if d in rule.text:
                    data[d] = rule.text.replace(d, '')

        try:
            description = soup.find('div', class_='style-item-description-html-qCwUL')
            data['Описание'] = description.text
        except:
            description = soup.find('div', class_='style-item-description-text-mc3G6')
            data['Описание'] = description.text

        images = soup.find('ul', class_='images-preview-previewWrapper-R_a4U')
        images_li = images.find_all('li')
        data['Изображения'] = [li.find('img').get('src') for li in images_li]
        # print([li.find('img').get('src') for li in images_li])

        main_pic = soup.find('div', class_='image-frame-wrapper-_NvbY').find('img').get('src')
        data['Главное изображение'] = main_pic

        price = soup.find('span', class_='style-price-value-main-TIg6u').text
        data['Цена'] = price

        address = soup.find('div', class_='style-item-address-KooqC').text
        data['Адрес'] = address
        print(data)
        self.writer.writerow([
            data['Количество гостей:'],
            data['Можно с детьми:'],
            data['Можно с животными:'],
            data['Можно курить:'],
            data['Разрешены вечеринки:'],
            data['Есть отчётные документы:'],
            data['Количество комнат:'],
            data['Общая площадь:'],
            data['Этаж:'],
            data['Техника:'],
            data['Интернет и ТВ:'],
            data['Комфорт:'],
            data['Залог:'],
            data['Описание'],
            data['Изображения'],
            data['Главное изображение'],
            data['Цена'],
            data['Адрес']
        ]
        )

    def runner(self):

        # all_links = []
        # self.run()
        # time.sleep(2)
        # for i in range(10):
        #     all_links.extend(self.page_product_links())
        #
        #     time.sleep(1)
        #     button = WebDriverWait(self.driver, 10).until(
        #         EC.element_to_be_clickable((By.XPATH, '//*[@id="item_list_with_filters"]/div[3]/div/div[2]/button[2]')))
        #     try:
        #         button.click()
        #     except:
        #         break
        # print(all_links)
        self.writer.writerow([
            'Количество гостей:',
            'Можно с детьми:',
            'Можно с животными:',
            'Можно курить:',
            'Разрешены вечеринки:',
            'Есть отчётные документы:',
            'Количество комнат:',
            'Общая площадь:',
            'Этаж:',
            'Техника:',
            'Интернет и ТВ:',
            'Комфорт:',
            'Залог:',
            'Описание:',
            'Изображения',
            'Главное изображение',
            'Цена',
            'Адрес',
        ]
        )
        for url in self.urls:
            url = self.domain + url
            try:
                self.parse_product(url)
                time.sleep(10)
            except:
                time.sleep(25)

        # self.parse_product('url')


def convertor():
    from openpyxl import Workbook
    import csv
    wb = Workbook()
    ws = wb.active
    with open(f'result.csv', 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            print(row)
            ws.append(row)
    wb.save(f'result.xlsx')


if __name__ == '__main__':
    avito = Avito()
    avito.runner()
    convertor()
