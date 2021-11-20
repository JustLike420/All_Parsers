from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

vk_link = input('[+] INPUT LINK: ')

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(
    ChromeDriverManager().install(),
    options=options,
)

driver.get('https://ru.savefrom.net/7/')
driver.find_element_by_id('sf_url').send_keys(vk_link)
driver.find_element_by_id('sf_submit').click()
element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "link-download")))
print(f"[+] DOWNLOAD: {element.get_attribute('href')}")
driver.quit()