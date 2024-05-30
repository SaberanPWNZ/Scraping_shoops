import requests
import lxml
from bs4 import BeautifulSoup

from utillities import get_article_from_title


class BaseStore:
    def __init__(self, shop_url, all_items, headers=None, cookies=None, ):
        self.item_list = []
        self.url = shop_url
        self.headers = headers
        self.cookies = cookies
        self.all_items = all_items

    @staticmethod
    def get(self, shop_url):
        response = requests.get(url=shop_url)
        return response

    def post(self):
        return requests.post(self.url, self.headers)

    def generate_info(self, all_items):
        for item in all_items.find_all('article'):
            price = item.find_next('div', class_="card-price")
            name = item.find_next(class_='card__title')

            if price is not None:
                price = price.text.strip().replace(" ", "").replace("₴", "")

            if name is not None:
                name = name.get('title')

            card_item = {
                'name': name,
                'price': price,
                'article': get_article_from_title(name)
            }
            self.item_list.append(card_item)

        return self.item_list


class Item:
    def __init__(self, primary_key, article, title, price):
        self.id = primary_key
        self.article = article
        self.title = title
        self.price = price

    @classmethod
    def from_tuple(cls, db_tuple):
        return cls(db_tuple[0], db_tuple[1], db_tuple[2], db_tuple[3])

    def strip_price(self, price: str):
        return price.strip().replace(' ', '').replace(',00', '')


class Soup:
    def __init__(self, response):
        self.soup = BeautifulSoup(response.text, 'lxml')

    def find_element(self, **kwargs):
        obj = self.soup.find(**kwargs)
        return obj

    def find_all_elements(self, **kwargs):
        obj = self.soup.find_all(**kwargs)
        return obj

    def find_next_element(self, **kwargs):
        obj = self.soup.find_next(**kwargs)
        return obj
