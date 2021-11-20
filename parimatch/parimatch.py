from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

useragent = UserAgent()

url = 'https://parimatch.ru/ru/e-sports'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument(f"user-agent={useragent.random}")
driver = webdriver.Chrome(
    ChromeDriverManager().install(),
    options=options,
)

driver.get(f"{url}")
hrefs = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'styles_wrapper__BfdYz')))
for href in hrefs:
    print(href.get_attribute('href'))
driver.close()