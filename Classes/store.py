import requests
import lxml
from bs4 import BeautifulSoup

from utillities import get_article_from_title, HEADERS


class BaseStore:
    def __init__(self, shop_url, headers=HEADERS, cookies=None, ):
        self.item_list = []
        self.url = shop_url
        self.headers = headers
        self.cookies = cookies
        self.all_items = []

    @staticmethod
    def get(self, shop_url):
        response = requests.get(url=shop_url, headers=self.headers)
        return response

    def post(self):
        return requests.post(self.url, self.headers)


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

    @classmethod
    def get_article_from_title(self, title: str):
        article = title.split('(')
        article = article[1].replace(')', "")
        return article


class Soup:
    def __init__(self, response):
        self.soup = BeautifulSoup(response.text, 'lxml')

    def find_element(self, **kwargs):
        obj = self.soup.find(**kwargs)
        return obj

    def find_elements(self, **kwargs):
        obj = self.soup.find(**kwargs)
        return obj

    def find_all_next(self, **kwargs):
        obj = self.soup.find_all_next(**kwargs)
        return obj

    def find_all_elements(self, **kwargs):
        obj = self.soup.find_all(**kwargs)
        return obj

    def find_next_element(self, **kwargs):
        obj = self.soup.find_next(**kwargs)
        return obj
