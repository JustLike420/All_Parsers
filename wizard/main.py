import pandas as pd
import asyncio
import tqdm
import aiohttp
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.domain = 'https://b2b.wizard.ua'
        self.users_links = []
        self.all_ids = []
        self.df = pd.DataFrame()

    def __del__(self):
        self.df.to_excel('products_test.xlsx', index=False)

    async def async_request(self, url, session) -> str | None:
        for attempt in range(3):
            try:
                async with session.get(url) as response:
                    html = await response.json()
                    return html
            except Exception as e:
                print(f"Error fetching {url}: {e}. Retrying ({attempt + 1}/3)...")
                await asyncio.sleep(10)
        return None

    async def parse_page(self, url, session):
        data = await self.async_request(url, session)
        ids = [item['id'] for item in data['results']]
        self.all_ids.extend(ids)

    async def parse_item(self, url, session):
        card = await self.async_request(url, session)
        if card is not None:
            c = {
                "vendor_code": card['vendor_code'],
                "code": card['wizard_code_1c'],
                "name": card['name'],
                "price": card['price']['6']['number'],
                "company_price": card['company_price']['6']['number'],
                "recommended_price": card['recommended_price']['6']['number'],
                "brand": card['brand']['name'],
                "stock": sum(place['quantity'] for place in card['stock']),
                "description": '',
                "images": []
            }
            if len(card['images']) != 0:
                for image in card['images']:
                    original = image.get('original', '')
                    if original != '':
                        c['images'].append('https://b2b.wizard.ua' + image['original'])
            c['images'] = ', '.join(c['images'])
            c['description'] = BeautifulSoup(card['description'], 'html.parser').text.strip()
            for attr in card['attributes']:
                c[attr['attr_name']] = attr['attr_value']

            self.df = self.df._append(c, ignore_index=True)

    async def starter(self):

        cookies = {}

        headers = {}
        async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
            pages = 376

            tasks = []
            for i in range(1, int(pages) + 1):
                task = asyncio.create_task(
                    self.parse_page(self.domain + '/api/v1/catalog/products' + f'?format=json&page={i}', session)
                )
                tasks.append(task)
            pbar = tqdm.tqdm(total=len(tasks))
            for f in asyncio.as_completed(tasks):
                value = await f
                pbar.set_description(value)
                pbar.update()
            tasks = []
            for id_ in self.all_ids:
                task = asyncio.create_task(
                    self.parse_item(self.domain + '/api/v1/catalog/products/' + str(id_) + '?format=json', session)
                )
                tasks.append(task)
            pbar = tqdm.tqdm(total=len(tasks))
            try:
                for f in asyncio.as_completed(tasks):
                    value = await f
                    pbar.set_description(value)
                    pbar.update()
            except:
                self.df.to_excel('products_test.xlsx', index=False)


async def main():
    parser = Parser()
    await parser.starter()


if __name__ == '__main__':
    asyncio.run(main())
