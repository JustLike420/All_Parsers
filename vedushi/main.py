import threading
import time
import random
import openpyxl
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth


class VedushiParser:
    def __init__(self):
        self.url = 'https://vedushi.ru/artists/photographs/'

        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def run(self):
        self.driver.get(f"{self.url}")

    def scroll(self):
        count = 0
        while True:
            if count != 3:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                count += 1
            else:
                break

    def find_all_links(self):
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        links = soup.find_all('a', class_='ava')
        print(links)
        all_links = [link.get('href') for link in links]
        with open('urls.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(all_links))
        self.driver.close()
    # def select_bac(self):
    #     b_xpath = '//*[@id="header-toolbar-symbol-search"]'
    #     button = WebDriverWait(self.driver, 20).until(
    #         EC.visibility_of_element_located(
    #             (By.XPATH, b_xpath)))
    #     button.click()
    #
    #     input_xpath = '//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[2]/div[1]/input'
    #     input = WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located(
    #             (By.XPATH, input_xpath)))
    #     input.send_keys(Keys.CONTROL + "a")
    #     input.send_keys(Keys.DELETE)
    #     input.send_keys("BAC")
    #
    #     b_xpath = '//*[@id="overlap-manager-root"]/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div'
    #     button = WebDriverWait(self.driver, 20).until(
    #         EC.visibility_of_element_located(
    #             (By.XPATH, b_xpath)))
    #     button.click()


class UserParse:
    def __init__(self):
        self.url = 'https://vedushi.ru'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
            desired_capabilities=caps
        )
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                          '''
        })

    def parse_page(self, url):
        print(url)
        self.driver.get(self.url + url)
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'show_phone')))
            button.click()
            while True:
                src = self.driver.page_source
                soup = BeautifulSoup(src, 'html.parser')
                phone = soup.find('div', class_='phone').text.strip()
                if '*' not in phone:
                    print(phone)
                    with open('phones.txt', 'a', encoding='utf-8') as file:
                        file.write(phone + '\n')
                    break
        except:
            pass

    # def run(self, urls):
    #     threads = []
    #
    #     for url in urls:
    #         thread = threading.Thread(target=self.parse_page, args=(url,))
    #         thread.start()
    #         threads.append(thread)
    #
    #     for thread in threads:
    #         thread.join()
    #
    #     self.driver.quit()


if __name__ == '__main__':
    # vedushi = VedushiParser()
    # vedushi.run()
    # vedushi.scroll()
    # vedushi.find_all_links()
    # /musician/alena-roksis/
    # with open('urls.txt', 'r') as file:
    #     urls = file.readlines()
    # for url in urls:
    #     user = UserParse()
    #     user.parse_page(url)
    phones = []
    with open('phones_vedushi.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line != '\n':
                phones.append(line)
    phones1 = ['+' + phone + '\n' for phone in phones[-1].split('+')]
    phones.pop()
    phones.extend(phones1)
    print(phones)
    with open('phones_ved.txt', 'w') as f:
        for phone in phones:
            f.write(phone)