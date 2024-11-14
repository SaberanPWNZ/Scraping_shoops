import os
import django
from typing import List
import requests
from bs4 import BeautifulSoup
from django.conf import settings

from utillities import get_article_from_title, clean_price

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraper.settings")

if not settings.configured:
    django.setup()

from items.models import Item


class BaseStore:
    def __init__(self, shop_url, headers=None, cookies=None):
        self.soup = Scraper()
        self.url = shop_url
        self.headers = headers
        self.cookies = cookies
        self.all_items = None

    def load_items(self, container_locator=None, item_locator=None):

        self.soup.get(self.url)
        soup = self.soup.get_text()

        self.all_items = self.extract_items_by_locator(soup, container_locator, item_locator)

    def extract_items_by_locator(self, soup, container_locator, item_locator):
        container = soup.find(class_=container_locator)
        if container:
            return container.find_all(class_=item_locator)
        else:
            return []

    def generate_info(self, title_locator, price_locator=None, status_locator=None):
        if self.all_items is None:
            raise ValueError("Данные не загружены. Вызовите `load_items` перед генерацией информации.")

        item_list = []
        for elem in self.all_items:

            name = elem.find(class_=title_locator).get_text()
            article = get_article_from_title(name)
            price = None

            if price_locator:
                price_element = elem.find(class_=price_locator)
                if price_element:
                    price = clean_price(price_element.get('data-price', '').strip().replace('.00', ''))
            status = ''
            if status_locator:
                status_element = elem.find(class_=status_locator)
                if status_element:
                    status = status_element.get_text()

            if 'Немає в наявності' not in status:
                card_item = {
                    'name': name,
                    'price': price,
                    'article': article,
                    'status': status,
                }
                item_list.append(card_item)

        return item_list

    def compare_data(self, partner_items_list: List[dict]):
        missing_items = []
        for elem in partner_items_list:
            try:
                article = elem.get('article', '').upper()
                if not article:
                    raise ValueError(f'Article is missing or empty in element: {elem}')
                price_partner = int(elem['price'])

                item = Item.objects.filter(article=article).first()

                if item:
                    item_price = int(item.rrp_price)
                    if price_partner == item_price:
                        missing_items.append(f'✅ {article} - Ціна партнера: {price_partner} грн, РРЦ: {item_price} грн')
                    elif price_partner < item_price:
                        missing_items.append(
                            f'🛑 {article} - Ціна нижча за РРЦ: {price_partner} грн, РРЦ: {item_price} грн')
                    else:
                        missing_items.append(
                            f'⚠️ {article} - Ціна вища за РРЦ: {price_partner} грн, РРЦ: {item_price} грн')
                else:
                    missing_items.append(f'🔍 {article} не знайдено в базі данних')

            except KeyError as e:
                missing_items.append(f'❌ Помилка: Невірний формат данних {elem}, {e}')

            except ValueError as e:
                missing_items.append(f'❌ Помилка: {e}')

            except Exception as e:
                missing_items.append(f'❌ Помилка: розпізнавання данних {article}')

        sorted_items = sorted(missing_items, key=lambda x: (not x.startswith('🛑'), x))
        return sorted_items

    def compare_data_xp_pen(self, partner_items_list, article_dict, model, price_field='rrp_price'):

        missing_items = []

        for elem in partner_items_list:
            name = elem['name']
            price_partner = int(elem['price']) if elem['price'] is not None else None
            article = article_dict.get(name)

            item = model.objects.filter(article=article).first()

            if item:
                item_price = int(getattr(item, price_field))
                if price_partner == item_price:
                    missing_items.append(f'✅ {article} - Ціна партнера: {price_partner} грн, РРЦ: {item_price} грн')
                elif price_partner < item_price:
                    missing_items.append(
                        f'🛑 {article} - Ціна нижча за РРЦ: {price_partner} грн, РРЦ: {item_price} грн')
                elif price_partner > item_price:
                    missing_items.append(
                        f'⚠️ {article} - Ціна вища за РРЦ: {price_partner} грн, РРЦ: {item_price} грн')
            else:
                missing_items.append(f'🔍 {name} не знайдено в базі данних')

        sorted_items = sorted(missing_items, key=lambda x: (not x.startswith('✅'), x))
        return sorted_items


class Scraper:
    def __init__(self):
        self.response = None
        self.soup = None

    def get(self, url, headers=None, cookies=None):

        self.response = requests.get(url, headers=headers, cookies=cookies)
        if not self.is_successful():
            raise ValueError(f"Ошибка запроса: {self.response.status_code}")
        return self.response

    def get_text(self):
        self._check_response()
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        return self.soup

    def find_element(self, **kwargs):

        self._check_soup()
        return self.soup.find(**kwargs)

    def find_all_elements(self, **kwargs):
        self._check_soup()
        return self.soup.find_all(**kwargs)

    def find_next_element(self, **kwargs):
        self._check_soup()
        return self.soup.find_next(**kwargs)

    def _get_status_code(self):
        self._check_response()
        return self.response.status_code

    def is_successful(self):
        return self._get_status_code() == 200

    def _check_response(self):
        if not self.response:
            raise ValueError("Не был выполнен запрос. Вызовите `get` сначала.")

    def _check_soup(self):
        if not self.soup:
            raise ValueError("HTML-контент не загружен. Вызовите `get_text` сначала.")