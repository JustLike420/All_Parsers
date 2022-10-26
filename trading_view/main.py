import time
import random
import numpy as np
import openpyxl
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# useragent = UserAgent()
class TradingViewChecker:
    def __init__(self):
        self.url = 'https://www.tradingview.com/chart/F3GeUZAf/?symbol=NYSE%3AF'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=C:\Users\Vladimir\PycharmProjects\All_Parsers\User Data")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )

    def run(self):
        self.driver.get(f"{self.url}")

    def select_bac(self):
        b_xpath = '//*[@id="header-toolbar-symbol-search"]'
        button = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, b_xpath)))
        button.click()

        input_xpath = '//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[2]/div[1]/input'
        input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, input_xpath)))
        input.send_keys(Keys.CONTROL + "a")
        input.send_keys(Keys.DELETE)
        input.send_keys("BAC")

        b_xpath = '//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div'
        button = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, b_xpath)))
        button.click()

    def open_settings(self):
        button = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="bottom-area"]/div[4]/div/div[1]/div[1]/div[1]/div[2]/button[1]')))
        button.click()

    def get_net_stats(self, numbers=None):

        while True:
            output_div = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'reports-content')))
            classes = output_div.get_attribute("class")
            if 'opacity-transition' not in classes:
                break
        net_profit = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="bottom-area"]/div[4]/div/div[2]/div/div/div[1]/div/div[1]/div[2]/div[1]'))).text
        total_closed = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="bottom-area"]/div[4]/div/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]'))).text
        print(net_profit, total_closed, '|', numbers)
        return net_profit, total_closed
    def inputs(self, number):
        n = 0
        for i in range(2, 22, 2):
            input_xpath = f'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[{i}]/div/span/span[1]/input'
            input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, input_xpath)))
            input.send_keys(Keys.CONTROL + "a")
            input.send_keys(Keys.DELETE)
            input.send_keys(str(number[n]))
            n += 1

        for i in range(25, 29, 2):
            input_xpath = f'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[{i}]/div/span/span[1]/input'
            input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, input_xpath)))
            input.send_keys(Keys.CONTROL + "a")
            input.send_keys(Keys.DELETE)
            input.send_keys(str(number[n]))
            n += 1

        input_xpath = f'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[20]/div/span/span[1]/input'
        input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, input_xpath)))
        input.send_keys(Keys.ENTER)

    def ok_button_click(self):
        button_xpath = '//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[4]/div/span/button'
        button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, button_xpath)))
        button.click()

    def setup_checkbox(self):
        button_1_xpath = '//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[21]/div/label'
        button = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, button_1_xpath)))
        button.click()
        button_2_xpath = '//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[22]/div/label'
        button = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, button_2_xpath)))
        button.click()

    def setting_properties(self):
        button_xpath = '//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div[2]'
        button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, button_xpath)))
        button.click()
        input_xpath = f'//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[3]/div/div[6]/div/div/span[1]/span[1]/input'
        input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, input_xpath)))
        input.send_keys(Keys.CONTROL + "a")
        input.send_keys(Keys.DELETE)
        input.send_keys("2000")
        button_xpath = '//*[@id="overlap-manager-root"]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div/div[1]'
        button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, button_xpath)))
        button.click()


if __name__ == '__main__':
    new_book = openpyxl.Workbook()
    new_sheet = new_book.active
    new_sheet['A1'].value = 'Число баров в стрике'
    new_sheet['B1'].value = 'Общий прирост цены в стрике %'
    new_sheet['C1'].value = '% отношения амплитуды цен стрика и пола'
    new_sheet['D1'].value = '% на сколько минимум объемы стрика больше объемов пола'
    new_sheet['E1'].value = 'Минимальное число баров в поле'
    new_sheet['F1'].value = 'Максимальное число баров в поле'
    new_sheet['G1'].value = 'Допуск к полу %'
    new_sheet['H1'].value = 'Период скользяшей EMA'
    new_sheet['I1'].value = 'X для фильтров SPX'
    new_sheet['J1'].value = 'Минимальная дельта для фильтра SPX'
    new_sheet['K1'].value = 'Тейк профит %'
    new_sheet['L1'].value = 'Стоп лосс %'
    new_sheet['M1'].value = 'Net Profit'
    new_sheet['N1'].value = 'Total Closed Trades'

    input_1 = [i for i in range(1, 11)]
    input_2 = [round(i, 2) for i in np.arange(0, 2.05, 0.05)]
    input_3 = [i for i in range(0, 51)]
    input_4 = [i for i in range(0, 51)]
    input_5 = [i for i in range(3, 11)]
    input_6 = [i for i in range(0, 60, 10)]
    input_7 = [round(i, 2) for i in np.arange(0, 0.55, 0.05)]
    input_8 = 21
    input_9 = [i for i in range(0, 8)]
    input_10 = [round(i, 2) for i in np.arange(0, 1.05, 0.05)]
    input_11 = [round(i, 2) for i in np.arange(0.1, 1.1, 0.1)]
    input_12 = [round(i, 2) for i in np.arange(0, 1.1, 0.1)]

    sel = TradingViewChecker()
    sel.run()
    sel.select_bac()
    sel.open_settings()
    sel.setting_properties()
    sel.setup_checkbox()
    # while True:
    #     numbers = [random.choice(input_1),
    #                random.choice(input_2),
    #                random.choice(input_3),
    #                random.choice(input_4),
    #                random.choice(input_5),
    #                random.choice(input_6),
    #                random.choice(input_7),
    #                input_8,
    #                random.choice(input_9),
    #                random.choice(input_10),
    #                random.choice(input_11),
    #                random.choice(input_12)]
    #     sel.inputs(numbers)
    #     # sel.ok_button_click()
    #     time.sleep(1)
    #     try:
    #         net_profit, total_closed = sel.get_net_stats(numbers)
    #     except:
    #         net_profit, total_closed = 'nodata', 'nodata'
    #     new_sheet.append((numbers[0],
    #                       numbers[1],
    #                       numbers[2],
    #                       numbers[3],
    #                       numbers[4],
    #                       numbers[5],
    #                       numbers[6],
    #                       numbers[7],
    #                       numbers[8],
    #                       numbers[9],
    #                       numbers[10],
    #                       numbers[11],
    #                       net_profit,
    #                       total_closed
    #                       ))
    #     new_book.save('result.xlsx')