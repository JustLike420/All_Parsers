import time

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
    sel = TradingViewChecker()
    sel.run()
    sel.select_bac()
    sel.open_settings()
    sel.setting_properties()
    sel.setup_checkbox()
    numbers = [1, 0.5, 0, 50, 3, 50, 0.12, 21, 5, 0.1, 0.27, 1]
    for i in range(1, 11):
        numbers[0] = i
        sel.inputs(numbers)
        # sel.ok_button_click()
        # time.sleep(1100)
        try:
            sel.get_net_stats(numbers)
        except:
            pass
