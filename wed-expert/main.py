import asyncio
import csv
import os.path
import re
import time
import aiohttp
from bs4 import BeautifulSoup
from loguru import logger
import requests

logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')


class MaximumRetriesReached(Exception):
    pass


class WebExpert:
    def __init__(self, category_name):
        self.category = category_name
        self.url = "https://{region}.wed-expert.com/{type}/{name}"
        # msk.wed-expert.com/profiles or categories/

        if not os.path.exists('data'):
            os.mkdir('data')
        self.stream = open(f"data/result_{self.category}.csv", "w", newline='')
        self.writer = csv.writer(self.stream)
        self.numbers_count = 0
        self.all_usernames = []
        self.number_class_name = {
            'presenters': 'catalog-item-title-name',
            'photographers': 'catalog-photo-item-user-name',
            'wedding-decoration': 'catalog-item-title-name',
            'videographers': 'video-item-title',
            'show-programs': 'catalog-item-title-name',
        }

    def write_data(self, **kwargs) -> None:
        """Запись информации в файл"""
        self.writer.writerow([kwargs['phone']])
        self.numbers_count += 1

    def api_request(self, url: str) -> str:
        """Запрос на страницу"""
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        try:
            html = requests.get(url, headers=headers).text
        except:
            logger.exception('Connection error')

            logger.error(f'Wait 10 sec and retry. Retry count: 1')
            time.sleep(10)
            html = self.api_request(url)
        return html

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
        raise Exception(f"Failed to fetch {url} after {3} attempts")

    def get_regions(self):
        regions = []
        with open('regions.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            city_line = line.split(' - ')
            city_name = city_line[0]
            regions.append(city_name)
        return regions


class UsernameParser(WebExpert):
    def __init__(self, category_name):
        super().__init__(category_name)
        self.usernames = set()

    def extract_usernames(self, html, region):
        soup = BeautifulSoup(html, "html.parser")
        usernames = [user.get('href').split('/')[-1] + ':' + region for user in
                     soup.find_all('a', class_=self.number_class_name[self.category])]
        return usernames

    async def parse_page(self, url):
        region = re.search(r'(?<=https:\/\/)[a-z-]+(?=\.wed-expert\.com)', url).group(0)

        html = await self.async_request(url)
        usernames = self.extract_usernames(html, region)
        self.usernames.update(usernames)
        await asyncio.sleep(1)

    async def starter(self):
        print(f"===== starting {self.category} =====")
        tasks = []
        all_regions = self.get_regions()
        for region in all_regions:
            url = self.url.format(region=region, type='categories', name=self.category)
            api_response = self.api_request(url)

            soup = BeautifulSoup(api_response, 'html.parser')
            try:
                last_page = soup.find('ul', class_='pagination').find_all('li')[-2].text
                print('pages: ', last_page, 'region: ', region)
                for page in range(1, int(last_page) + 1):
                    task = asyncio.create_task(self.parse_page(url + f'?page={page}'))
                    tasks.append(task)
            except:
                print('0 pages in: ', region)
        await asyncio.gather(*tasks)

    def save_usernames(self):
        with open(f'data\\{self.category}.txt', "w") as f:
            for username in self.usernames:
                f.write(username + "\n")
        print('Saved: ', len(self.usernames))


class PhoneParser(WebExpert):
    def __init__(self, category_name):
        super().__init__(category_name)
        self.phones = set()

    def extract_number(self, html):
        soup = BeautifulSoup(html, "html.parser")
        try:
            number = soup.find('a', class_='contact-item').text
        except:
            number = ''
        return number

    async def parse_page(self, url):
        try:
            html = await self.async_request(url)
            phone = self.extract_number(html)
            self.phones.update(phone)
        except:
            pass
        await asyncio.sleep(1)

    def get_usernames(self):
        with open(f'data\\{self.category}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        usernames = [line for line in lines]
        return usernames

    async def starter(self):
        print(f"===== starting {self.category} =====")
        tasks = []
        all_usernames = self.get_usernames()
        urls = []
        for username in all_usernames:
            user = username.split(':')[0]
            region = username.split(':')[1]

            urls.append(self.url.format(region=region, type='profiles', name=user))
        for url in urls:
            task = asyncio.create_task(self.parse_page(url))
            tasks.append(task)
        await asyncio.gather(*tasks)

    def save_numbers(self):
        with open('numbers_' + self.category + '.txt', "w") as f:
            for phone in self.phones:
                f.write(phone + "\n")
        print('Saved: ', len(self.phones))


async def main():
    categories = ['presenters', 'photographers', 'wedding-decoration', 'show-programs', 'videographers']
    for category in categories:
        parser = UsernameParser(category)
        await parser.starter()
        parser.save_usernames()
    for category in categories:
        parser = PhoneParser(category)
        await parser.starter()
        parser.save_numbers()


asyncio.run(main())
