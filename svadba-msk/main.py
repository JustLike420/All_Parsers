import asyncio

import aiohttp
from bs4 import BeautifulSoup


class ParserSvadbaMsk:
    def __init__(self, category_name):
        self.category_name = category_name
        self.phones = set()

    async def async_request(self, url) -> str:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        for attempt in range(3):
            try:
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get(url, allow_redirects=False) as response:
                        html = await response.text()
                        return html
            except Exception as e:
                print(f"Error fetching {url}: {e}. Retrying ({attempt + 1}/3)...")
                await asyncio.sleep(10)

    async def parse_page(self, url):
        html = await self.async_request(url)

        soup = BeautifulSoup(html, "html.parser")
        try:
            phone = soup.find('p', 'phone').text
            self.phones.update(phone)
        except:
            pass


    def save_numbers(self):
        with open('numbers_' + self.category_name + '.txt', "w") as f:
            for phone in self.phones:
                f.write(phone + "\n")
        print('Saved: ', len(self.phones))

    async def runner(self):
        with open(self.category_name + '.html', 'r', encoding='utf-8') as html_file:

            soup = BeautifulSoup(html_file, "html.parser")
            users_links = [user.get('href') for user in soup.find_all('a', class_='catalogPro_toprofile')]
        tasks = []
        for link in users_links:
            task = asyncio.create_task(self.parse_page(link))
            tasks.append(task)
        await asyncio.gather(*tasks)
        self.save_numbers()


if __name__ == '__main__':
    for category in ['photo', 'decor', 'show', 'tamada', 'video']:
        asyncio.run(ParserSvadbaMsk(category).runner())

