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
    def __init__(self, name, price, article):
        self.title = name
        self.price = price
        self.article = article


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
