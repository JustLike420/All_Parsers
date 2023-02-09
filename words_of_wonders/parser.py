import asyncio
import csv
import json
import time

import requests
import tqdm
import aiohttp
from bs4 import BeautifulSoup, NavigableString

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
all_data = {}


# async def get_html(url, session):
#
#     try:
#         async with session.get(url, headers=headers, allow_redirects=False, ) as resp:
#             response_text = await resp.text()
#
#             soup = BeautifulSoup(response_text, 'lxml')
#             cards = soup.find_all(class_='letterblock')
#
#             for card in cards:
#                 if 'nohover' not in card.attrs['class']:
#                     word = ''.join([letter.text for letter in card.find_all('span')])
#                     lvl = url.split('/')[-2].replace('Reberu-', '')
#                     if lvl not in all_data.keys():
#                         all_data[lvl] = [word]
#                     else:
#                         all_data[lvl].append(word)
#     except Exception as e:
#         print('error', e)
#         await get_html(url, session)

async def get_html(url, session):
    try:
        async with session.get(url, headers=headers, allow_redirects=False, ) as resp:
            response_text = await resp.text()

            soup = BeautifulSoup(response_text, 'lxml')
            cards = soup.find(class_='words')
            list_words = cards.contents
            all_words = []
            word = ''
            for el in list_words:
                if type(el) != NavigableString:
                    if el.text != "":
                        word += el.text
                    elif el.text == "":
                        all_words.append(word)
                        word = ''
            lvl = url.split('/')[-1].replace('level-', '').replace('.html', '')
            all_data[lvl] = all_words
    except Exception as e:
        print('error', e)
        await get_html(url, session)


# def parse_one_card():
#     url = 'https://wordsofwonders.net/ja/%E3%83%96%E3%83%AA%E3%83%83%E3%82%B2%E3%83%B3/level-529.html'
#     response = requests.get(
#         'https://wordsofwonders.net/ja/%E3%83%96%E3%83%AA%E3%83%83%E3%82%B2%E3%83%B3/level-529.html').text
#     soup = BeautifulSoup(response, 'lxml')
#     cards = soup.find(class_='words')
#     list_words = cards.contents
#     all_words = []
#     word = ''
#     for el in list_words:
#         if type(el) != NavigableString:
#             if el.text != "":
#                 word += el.text
#             elif el.text == "":
#                 all_words.append(word)
#                 word = ''
#     lvl = url.split('/')[-1].replace('level-', '').replace('.html', '')
#     all_data[lvl] = all_words


async def main():
    all_links = []
    with open(f'data/result_ja1.csv', 'r', encoding="utf-8") as f:
        for lvl_link in csv.reader(f):
            all_links.append(lvl_link[0])
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in all_links[:3521]:
            task = asyncio.create_task(get_html(link, session))
            tasks.append(task)

        # await asyncio.gather(*tasks)
        pbar = tqdm.tqdm(total=len(tasks))
        for f in asyncio.as_completed(tasks):
            value = await f
            pbar.set_description(value)
            pbar.update()
    with open('json_data_ja1.json', 'w', encoding="utf-8") as outfile:
        json.dump(all_data, outfile)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # parse_one_card()
