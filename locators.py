import csv
import json
import lxml
from bs4 import BeautifulSoup
import requests


from config import HEADERS


response = requests.get(
    url="https://www.foxtrot.com.ua/uk/shop/graficheskie_plansheti_wacom.html"
)


soup = BeautifulSoup(response.text, 'lxml')
fields_name = ['name', 'price', 'article']
all_items = soup.find(class_='listing__body-wrap')

item_list = []
for item in all_items:
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
        'article': article
                }
    item_list.append(card_item)
    with open('foxtrot.csv', "a", encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields_name)
        writer.writeheader()
        writer.writerow(card_item)


print(item_list)







# with open('Response.json', 'w', encoding='UTF-8') as file:
#
#     json_data = json.dumps(response.json(), ensure_ascii=False, indent=4)
#     file.write(json_data)


