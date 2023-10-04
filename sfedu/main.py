import asyncio
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import aiohttp


class Parser:
    def __init__(self):
        self.domain = 'https://sfedu.ru/'
        self.wb = Workbook()
        self.sheet = self.wb.active
        self.links = []
        self.connector = aiohttp.TCPConnector(limit=50)

    @staticmethod
    async def async_request(url: str, session: aiohttp.ClientSession) -> str:
        for attempt in range(3):
            try:
                async with session.get(url) as response:
                    html = await response.text()
                    return html
            except Exception as e:
                print(f"Error fetching {url}: {e}. Retrying ({attempt + 1}/3)...")
                await asyncio.sleep(10)

    def make_request(self, url):
        response = requests.get(url)
        return response.text

    async def get_page_links(self, url: str, session: aiohttp.ClientSession) -> None:
        html = await self.async_request(url, session)
        soup = BeautifulSoup(html, "html.parser")
        links = [link.get('href') for link in soup.find('section', class_='company-results__list').find_all('a')]
        self.links.extend(links)

    def parse_page(self, url: str) -> None:
        html = self.make_request(url)
        soup = BeautifulSoup(html, "html.parser")

        company = soup.find(class_='company__title').text

        for item in soup.find_all('div', class_='company__overview-item'):
            if 'Investor type' in item.text:
                investor_type = item.text.replace('Investor type', '')
                break
        company_links = soup.find('div', class_='company__links').find_all('a')
        website = company_links[0].get('href')
        email = ''
        for link in company_links:
            href = link.get('href')
            if 'linkedin' in link.get('href'):
                website += f"\n{href}"
            elif 'mailto:' in href:
                email = href.replace('mailto: ', '')

        investment_preferences_block = soup.find_all('div', class_='company__content-inner')[1]

        region_focus = investment_preferences_block.find('div', class_='company__stats-focus').text

        ticket, horizon, stage, exit_strategy = '', '', '', ''
        for invest in investment_preferences_block.find_all('div', class_='company__preferences-item'):
            match invest.find('h6').text:
                case 'Investment Ticket':
                    ticket = invest.text.replace('Investment Ticket', '').strip()
                case 'Investment Horizon':
                    horizon = invest.text.replace('Investment Horizon', '').strip()
                case 'Investment Stage':
                    stage = invest.text.replace('Investment Stage', '').strip()
                case 'Exit Strategy':
                    exit_strategy = invest.text.replace('Exit Strategy', '').strip()

        contacts_table = soup.find('div', class_='company__contacts-table')
        table_rows = contacts_table.find_all('div', class_='row')[1:]

        contacts = []
        for row in table_rows:
            row_items = [col for col in row.find_all('div', class_='col-6')]
            for col in row_items:
                match col.find('p', class_='company__contacts-item-title').text:
                    case 'Name':
                        name = col.find('p', class_='mb-0').text
                    case 'Title':
                        title = col.find('p', class_='mb-0').text
                    case 'E-mail':
                        email = col.find('p', class_='mb-0').text
                    case 'Social':
                        try:
                            social = col.find('a').get('href')
                        except:
                            social = '-'
            contacts.append([name, title, email, social])

        for contact in contacts:
            content_cells = [
                company, investor_type, website, email, region_focus, ticket, horizon, stage, exit_strategy
            ]
            content_cells.extend(contact)
            self.sheet.append(content_cells)
        self.wb.save('Sports-SportsTech.xlsx')

    def get_company_links(self):
        all_hrefs = []
        main_page = self.make_request('https://sfedu.ru/www/stat_pages22.show?p=UNI/N11900/D')
        soup = BeautifulSoup(main_page, "html.parser")
        uls = soup.find('div', class_='list').find_all('ul')[1:9]
        for ul in uls:
            hrefs = ul.find_all('a')
            for href in hrefs:
                all_hrefs.append(self.domain + href.get('href').replace('ELS/inf', 'ELs/sotr'))
        return all_hrefs

    def get_people_links(self, url):
        urls = []
        response = self.make_request(url)
        soup = BeautifulSoup(response, 'html.parser')
        trs = soup.find('table', class_='tbl1').find_all('tr')
        for tr in trs:
            href = 'https:' + tr.find('a').get('href').replace('¶ms', '&params')
            urls.append(href)
        return urls

    async def starter(self):
        urls = self.get_company_links()
        people_urls = []
        for url in urls:
            people_urls.extend(self.get_people_links(url))


async def main():
    parser = Parser()
    await parser.starter()


if __name__ == '__main__':
    asyncio.run(main())
