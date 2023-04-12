import asyncio
import json
import urllib
import tqdm
import aiohttp
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from multiprocessing import Pool


class WordSurf:
    def __init__(self, language, link):
        self.lvl_url = link
        self.language = language
        # with open('ko_data.json', 'r', encoding='utf-8') as file:
        #     self.data = json.load(file)
        self.data = {}
        self.errors = 0

    async def async_request(self, url, session) -> str:

        for attempt in range(3):
            try:
                async with session.get(url, allow_redirects=False) as response:
                    html = await response.text()
                    return html
            except Exception as e:
                print(f"Error fetching {url}: {e}. Retrying ({attempt + 1}/3)...")
                await asyncio.sleep(10)

    async def parse_page(self, url, session):
        html = await self.async_request(url, session)
        try:
            soup = BeautifulSoup(html, "html.parser")
            words = [word.text for word in soup.find('div', class_='wordsb').find_all('span')]
            title = soup.find('div', class_='tipsb').find('h3').text

            lvl = url.split('-')[-1]
            self.data[lvl] = {'words': words, 'title': title}
        except:
            self.errors += 1

    async def runner(self):
        links = [self.lvl_url + str(lvl) for lvl in range(1, 9666) if str(lvl) not in self.data.keys()]
        # links = [self.lvl_url + str(lvl) for lvl in range(1, 9666)]
        tasks = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Proxy-Authorization': 'Basic ZTIyNDdhZTFhYzU5N2VlNjI0MWNiZWQzMWQ5YTY5MjM6V2NLUDJFRmtUQnM4dEhuYQ==',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            for link in links:
                task = asyncio.create_task(self.parse_page(link, session))
                tasks.append(task)
            # await asyncio.gather(*tasks)
            pbar = tqdm.tqdm(total=len(tasks))
            for f in asyncio.as_completed(tasks):
                value = await f
                pbar.set_description(value)
                pbar.update()
        print(self.errors)
        with open(f'{self.language}_data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.data))


class WordsAnswer(WordSurf):
    async def parse_page(self, url, session):
        url = urllib.parse.unquote(url)
        html = await self.async_request(url, session)
        try:
            soup = BeautifulSoup(html, "html.parser")
            words = [word.text for word in soup.find('div', class_='words-block').find_all('span')]
            title = soup.find('div', class_='tips-block').find('h3').text

            lvl = url.split('-')[-1]
            self.data[lvl] = {'words': words, 'title': title}
        except:
            print('error', url)
            self.errors += 1


def parser_selenium(lvl):
    url = 'https://word-surf.net/word-surf-ja-%e7%ad%94%e3%81%88/word-surf-ja-%e3%83%ac' \
          '%e3%83%99%e3%83%ab-' + lvl
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options,
        desired_capabilities=caps
    )
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                          '''
    })
    with open('ja_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    driver.get(url)
    try:
        driver.find_element(By.CLASS_NAME, 'wordsb')
        src = driver.page_source

        soup = BeautifulSoup(src, "html.parser")
        words = [word.text for word in soup.find('div', class_='wordsb').find_all('span')]
        title = soup.find('div', class_='tipsb').find('h3').text
        data[lvl] = {'words': words, 'title': title}
        print(lvl, words, title)

        with open(f'ja_data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))
    except Exception as e:
        print('error', lvl, e)


if __name__ == '__main__':
    languages = {
        'en': 'https://word-surf.net/word-surf-answers/word-surf-level-',
        'de': 'https://word-surf.net/word-surf-de-losungen/word-surf-de-level-',
        'fr': 'https://word-surf.net/word-surf-fr-reponse/word-surf-fr-niveau-',
        'es': 'https://word-surf.net/word-surf-es-respuestas/word-surf-es-nivel-',
        'tr': 'https://word-surf.net/word-surf-tr-cevaplari/word-surf-tr-seviye-',
        'br': 'https://word-surf.net/word-surf-br-respostas/word-surf-br-nivel-',
        'ja': 'https://word-surf.net/word-surf-ja-%e7%ad%94%e3%81%88/word-surf-ja-%e3%83%ac%e3%83%99%e3%83%ab-',
        'ko': 'https://word-surf.net/word-surf-ko-%eb%8b%b5%eb%b3%80/word-surf-ko-%eb%a0%88%eb%b2%a8-'
    }
    for language, link in languages.items():
        asyncio.run(WordSurf(language, link).runner())


    with open('link.txt', 'r', encoding='utf-8') as file:
        link = file.readlines()
    asyncio.run(WordsAnswer('ja',
                            link[0][:-1]).runner())
    with open(f'ja_data.json') as json_file:
        data = json.load(json_file)
    links = [str(lvl) for lvl in range(1, 9666) if str(lvl) not in data.keys()]
    print(links)

