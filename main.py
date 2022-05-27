import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.citilink.ru/catalog/kompyutery/'
HEADERS = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
           'accept': '*/*'}
FILE = 'goods.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='PaginationWidget__page')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product_data__gtm-js')

    products = []
    for item in items:
        rows = item.find_all('span', class_='ProductCardHorizontal__properties_value')
        try:
            products.append({
                'title': item.find('a', class_='ProductCardHorizontal__title').get_text(strip=True),
                'par1': rows[0].get_text(strip=True),
                'price': item.find('span', class_='ProductCardHorizontal__price_current-price '
                                                  'js--ProductCardHorizontal__price_current-price').get_text(strip=True)
            })
        except IndexError:
            print('index Error')
        except AttributeError:
            print('attribute Error')
    return products


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'par1', 'price'])
        for item in items:
            writer.writerow([item['title'], item['par1'], item['price']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        goods = []
        pages_count = get_pages_count(html.text)
        for page in range(1, 15):
            print(f'Парсинг страницы {page} из {pages_count}')
            html = get_html(URL, params={'p': page})
            goods.extend(get_content(html.text))
        print(goods)
        save_file(goods, FILE)
        print(f'Получено: {len(goods)} товаров')

    else:
        print('error')


parse()
