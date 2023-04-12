import asyncio
import json
import requests
import tqdm
import aiohttp
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, category):
        self.category = category
        self.domain = 'https://iq-banket.ru/'
        self.users_links = []
        self.phones = []

    def get_page_count(self):
        url = self.domain + self.category
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        last_page = soup.find_all('a', class_='before_tablet')[-1].text
        print(last_page)
        return last_page

    async def async_request(self, url, session) -> str:
        for attempt in range(3):
            try:
                async with session.get(url) as response:
                    html = await response.text()
                    return html
            except Exception as e:
                print(f"Error fetching {url}: {e}. Retrying ({attempt + 1}/3)...")
                await asyncio.sleep(10)

    async def parse_page(self, url, session):
        html = await self.async_request(url, session)
        soup = BeautifulSoup(html, "html.parser")
        usernames = [username.get('href') for username in soup.find_all('a', class_='user_name')]
        self.users_links.extend(usernames)

    async def parse_phone(self, url, session):
        html = await self.async_request(url, session)
        soup = BeautifulSoup(html, "html.parser")
        js = soup.find_all('script')[1].text.replace('window.__INITIAL_STATE__ = ', '')
        data = json.loads(js)
        try:
            phone = data['profile']['phones'][0]
            self.phones.append(phone)
        except:
            pass

    async def starter(self):
        page_count = self.get_page_count()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            for i in range(1, int(page_count) + 1):
                task = asyncio.create_task(
                    self.parse_page(self.domain + self.category + f'?page={i}', session)
                )
                tasks.append(task)
            pbar = tqdm.tqdm(total=len(tasks))
            for f in asyncio.as_completed(tasks):
                value = await f
                pbar.set_description(value)
                pbar.update()
            tasks = []
            for user in self.users_links:
                user = user.split('/')
                task = asyncio.create_task(
                    self.parse_phone(self.domain + f'{user[1]}/{user[2]}', session)
                )
                tasks.append(task)
            pbar = tqdm.tqdm(total=len(tasks))
            for f in asyncio.as_completed(tasks):
                value = await f
                pbar.set_description(value)
                pbar.update()
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        for phone in self.phones:
            ws.append([phone])
        wb.save(f'{self.category}.xlsx')


async def main():
    categories = ['photographers', 'videographers', 'musicians', 'decorators']
    for category in categories:
        parser = Parser(category)
        await parser.starter()


if __name__ == '__main__':
    asyncio.run(main())

    # for language, link in languages.items():
    #     asyncio.run(WordSurf(language, link).runner())
