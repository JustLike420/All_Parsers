import csv
import os.path
import time
from loguru import logger
import requests

logger.add("out.log", backtrace=True, diagnose=True, rotation='50 MB')


class MaximumRetriesReached(Exception):
    pass


class Gorko:
    def __init__(self, category_name, category_id):
        self.category = category_name
        self.category_id = category_id
        self.url = "https://api.gorko.ru/api/v3/vendorcard?entity[cityId]={city_id}&entity[languageId]=1&entity[specKey]=1" \
                   "&list[cityId]={city_id}&list[filters]=service=1&list[page]=1&list[perPage]=1000&list[seed]=543860" \
                   "&list[typeId]={category_id}"

        if not os.path.exists('data'):
            os.mkdir('data')
        self.stream = open(f"data/result_{self.category}.csv", "w", newline='')
        self.writer = csv.writer(self.stream)
        self.numbers_count = 0

    def __del__(self):
        """Закрытие файла и конвертация в xlsx"""
        from convert import convert_workbook
        self.stream.close()
        convert_workbook(f'data/result_{self.category}')

    def write_data(self, **kwargs) -> None:
        """Запись информации в файл"""
        self.writer.writerow([kwargs['phone']])
        self.numbers_count += 1

    def api_request(self, url: str) -> dict:
        """Запрос на страницу"""
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        try:
            html = requests.get(url, headers=headers).json()
        except:
            logger.exception('Connection error')

            logger.error(f'Wait 10 sec and retry. Retry count: 1')
            time.sleep(10)
            html = self.api_request(url)
        return html

    def get_contacts(self, api_response: dict) -> list:
        """Получение номеров"""
        numbers = []
        for value_dict in api_response["entity"].values():
            number = value_dict.get("schema").get("telephone")
            numbers.append(number)
        return numbers

    def starter(self) -> None:
        try:
            with open('regions_with_ids.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
            for line in lines:
                city_line = line.split(' - ')
                city_name = city_line[1]
                city_id = city_line[2]
                api_response = self.api_request(self.url.format(city_id=city_id, category_id=self.category_id))
                numbers = self.get_contacts(api_response)
                for number in numbers:
                    self.write_data(phone=number, city_name=city_name)
                logger.success(f"Write {len(numbers)} numbers in {city_name}")
        except Exception as e:
            logger.exception(e)
        else:
            logger.info('Job DONE')
        finally:

            logger.info('=====================Close scraping=====================')
            logger.info(f'Scraped {self.numbers_count} items')


def get_regions_numbers():
    regions = []
    with open('regions.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for line in lines:
        city_line = line.split(' - ')
        city_name = city_line[1]
        url = f'https://api.gorko.ru/api/v2/cities?name={city_name}&fields=url&per_page=1'
        response = requests.get(url).json()
        region_id = response['cities'][0]['id']
        regions.append(line.replace('\n', '') + f' - {region_id}\n')

    with open('regions_with_ids.txt', 'w', encoding='utf-8') as file:
        file.writelines(regions)


def main():
    categories = [("Ведущие", 7),
                  ("Видеографы", 6),
                  ("Фотографы", 5),
                  ("Оформители", 12),
                  ("Артисты", 15)]
    for category in categories:
        f = Gorko(category[0], category[1])
        f.starter()


if __name__ == '__main__':
    main()
