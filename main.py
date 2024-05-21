import csv
import json
import lxml
from bs4 import BeautifulSoup
import requests

from config import HEADERS
from utillities import get_article_from_title
from Classes.store import BaseStore




response = requests.get(
    url="https://www.foxtrot.com.ua/uk/shop/graficheskie_plansheti_wacom.html"
)

soup = BeautifulSoup(response.text, 'lxml')
#fields_name = ['name', 'price', 'article']
all_items = soup.find(class_='listing__body-wrap image-switch')

item_list = []

for item in all_items.find_all('article'):
    price = item.find_next('div', class_="card-price")
    name = item.find_next(class_='card__title')
    article = "this will be true article"

    if price is not None:
        price = price.text.strip().replace(" ", "").replace("₴", "")

    if name is not None:
        name = name.get('title')

    card_item = {
        'name': name,
        'price': price,
        'article': get_article_from_title(name)
        }


    item_list.append(card_item)

    # with open("Items.json", "w", encoding='UTF-8') as f:
    #     json.dump(item_list, f, ensure_ascii=False, indent=4)





