import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
code = 'GRN28'
url = f'https://www.detmir.ru/search/results/?qt={code}&searchType=common&searchMode=common'
req = requests.get(url, headers=headers)
src = req.text
with open('index.html', 'w') as f:
    f.write(src)
