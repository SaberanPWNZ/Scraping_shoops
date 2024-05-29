import requests
import lxml
from bs4 import BeautifulSoup


class BaseStore:
    def __init__(self, url, headers=None, cookies=None):
        self.url = url
        self.headers = headers
        self.cookies = cookies

    def get(self):
        response = requests.get(self.url, self.headers)
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



