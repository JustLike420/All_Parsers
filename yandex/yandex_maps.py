import time
import random
import numpy as np
import openpyxl
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
from selenium import webdriver as wb
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# useragent = UserAgent()
class YandexChecker:
    def __init__(self):
        self.url = 'https://yandex.ru/maps/213/moscow/search/%D1%81%D0%B0%D0%BD%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0'

        self.options = webdriver.ChromeOptions()
        # self.options.add_argument(r"user-data-dir=C:\Users\Vladimir\PycharmProjects\All_Parsers\User Data")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )

    def run(self):
        self.driver.get(self.url)
        time.sleep(100)


class YandexMapParser:
    # def __init__(self, _link,  sleep_time=0.1,
    #              change_header_iter=10,save_after=100,
    #              with_selenium=True, token=None,
    #              _query="Ozon, пункты выдачи москва",
    #              region='москва', _curr_date=datetime.now().strftime('%s'), _browser='firefox'):
    #
    #     self.link = _link
    #     self.sleep_time = sleep_time
    #     self.change_header_iter = change_header_iter
    #     self._header = self._change_user_agent()
    #     self.save_after = save_after
    #     self.with_selenium = with_selenium
    #
    #     self.query = _query
    #     self.region = region
    #     self.curr_date = _curr_date
    #     self.browser = _browser
    #
    #     self._df = None
    #
    #     if self.with_selenium:
    #         if self.browser == 'firefox':
    #             self.driver = webdriver.Firefox(executable_path='drivers/geckodriver_firefox')
    #         elif self.browser == 'chrome':
    #             self.driver = webdriver.Chrome(executable_path='drivers/chromedriver97')
    #     else:
    #         self.driver = None
    #
    #     self.token = token
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument(r"user-data-dir=C:\Users\Vladimir\PycharmProjects\All_Parsers\User Data")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=self.options,
        )
        self.link = 'https://yandex.ru/maps/213/moscow/search/%D1%81%D0%B0%D0%BD%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0'

    @staticmethod
    def _change_user_agent():

        """
        This function switch user anonymity

        :return:
        Dict having useragent fot higher am
        """

        _ua = UserAgent()
        return {'User-Agent': str(_ua.chrome)}

    def parse_data(self):
        self.driver.get(self.link)


        try:
            # get info about scroll
            wait = WebDriverWait(self.driver, 15)
            source = wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "scroll__scrollbar-thumb")))

            source_ele = self.driver.find_element(By.CLASS_NAME, "scroll__scrollbar-thumb")
            target_ele = self.driver.find_element(By.CLASS_NAME, "scroll__scrollbar-thumb")

            target_ele_x_offset = target_ele.location.get("x")
            # target_ele_y_offset = target_ele.location.get("y")

            height = int(self.driver.execute_script(
                "return document.documentElement.scrollHeight"
            ))
            # Performs dragAndDropBy onto the target element offset position
            last_len = -10e6

            while True:
                # drag slider down till the end. Calculate length
                # of slider current position and calculating offset as
                #  height(height of window) - slider height - slider position
                time.sleep(5)

                slider = self.driver.find_elements_by_class_name('scroll__scrollbar-thumb')[0]
                slider_size = slider.size

                slider_w, slider_h = slider_size['width'], slider_size['height']

                wb.ActionChains(self.driver).drag_and_drop_by_offset(source_ele, target_ele_x_offset,
                                                                     height - slider_h - slider.location.get(
                                                                         "y")).perform()

                time.sleep(5)
                wb.ActionChains(self.driver).drag_and_drop_by_offset(source_ele, target_ele_x_offset,
                                                                     1).perform()

                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # calculating stop criteria. If no more new elements stop parsing
                addresses = soup.find_all("div", {"class": "search-business-snippet-view__address"}, text=True)
                addresses = [i.text.strip().replace("\xa0", " ") for i in addresses]
                curr_len = len(addresses)
                print(addresses)
                if last_len == curr_len:
                    break
                else:
                    last_len = curr_len
        except TimeoutException:
            pass

        # extract information
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # extract addresses
        addresses = soup.find_all("div",
                                  {"class": "search-business-snippet-view__address"}, text=True)
        addresses = [i.text.strip().replace("\xa0", " ") for i in addresses]

        # extract rating
        rate = soup.find_all("span",
                             {"class": "business-rating-badge-view__rating"}, text=True)
        rate = [i.text.strip().replace("\xa0", " ").replace(",", ".") for i in rate]

        # extract categories
        # typing = soup.find_all("div",
        #                        {"class": "search-business-snippet-view__categories"}, text=True)
        # typing = [i.text.strip().replace("\xa0", " ").replace(",", ".") for i in typing]

        # extract titles
        title = soup.find_all("div",
                              {"class": "search-business-snippet-view__title"}, text=True)
        title = [i.text.strip().replace("\xa0", " ").replace(",", ".") for i in title]

        lat_list = []
        lon_list = []

        # geocoding via google
        # for j in tqdm(addresses):
        #
        #     sleep(0.3)
        #     lat, lon = self._get_google_results(j, False, True)
        #     lat_list.append(lat)
        #     lon_list.append(lon)

        # create dataframe
        # self._df = pd.DataFrame({
        #     'ADDRESS': addresses,
        #     'TYPE_PP': mode(typing),
        #     'COMPANY_NAME': mode(title),
        #     'LAT': lat_list,
        #     'LON': lon_list,
        #     'REGION': self.region,
        #     'DATE_OF_LOADING': self.curr_date
        # })

        # close drivers
        self.driver.close()
        self.driver.quit()

        return 1


if __name__ == '__main__':
    parser = YandexMapParser()
    df_new = parser.parse_data()
