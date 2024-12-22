import logging
import os
import django
from typing import List
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from Classes.status import Status
from utillities import get_article_from_title, clean_price

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraper.settings")

if not settings.configured:
    django.setup()

from items.models import Item, Brand
from checker.models import Partner, ScrapedData, ScrapedItem

logger = logging.getLogger()

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
            status = None
            if price_locator:
                price_element = elem.find(class_=price_locator)
                if price_element:
                    price = clean_price(price_element.get('data-price', '').strip().replace('.00', ''))

            if status_locator:
                status_element = elem.find(class_=status_locator)
                if status_element:
                    status = status_element.get_text()

                card_item = {
                    'name': name,
                    'price': price,
                    'article': article,
                    'status': status,
                }
                print(card_item)
                item_list.append(card_item)

        return item_list

    def compare_data(self, partner_items_list: List[dict]):

        missing_items = []
        for elem in partner_items_list:
            try:
                article = elem.get('article', '').upper()
                if not article:
                    raise ValueError(f'Article is missing or empty in element: {elem}')

                price_partner = elem['price']

                item = Item.objects.filter(article=article).first()

                if item:
                    item_price = int(item.rrp_price)
                    if int(price_partner) == item_price:
                        missing_items.append(f'✅ {article} - Ціна партнера: {price_partner} грн, РРЦ: {item_price} грн')
                    elif int(price_partner) < item_price:
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

            # except Exception as e:
            #     missing_items.append(f'❌ Помилка: розпізнавання данних {}')

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

    def generate_info_with_articles(self, title_locator=None, price_locator=None, status_locator=None,
                                    article_extractor=None):
        if self.all_items is None:
            raise ValueError("Данные не загружены. Вызовите `load_items` перед генерацией информации.")

        item_list = []
        for elem in self.all_items:

            name_element = elem.find(class_=title_locator)
            name = name_element.get_text().strip() if name_element else None

            article = article_extractor(name) if article_extractor and name else None

            price = None
            if price_locator:
                price_element = elem.find(class_=price_locator)
                price = clean_price(
                    price_element.get('data-price', '').strip().replace('.00', '')) if price_element else None

            status = None
            if status_locator:
                status_element = elem.find(class_=status_locator)
                status = Status.not_in_stock if status_element else Status.in_stock

            card_item = {
                'name': name,
                'article': article,
                'price': price,
                'status': status,
            }
            item_list.append(card_item)

        return item_list

    def save_parsed_data(self, partner_name: str, items: list, brand: str):
        try:
            partner, _ = Partner.objects.get_or_create(name=partner_name)
            brand_obj = Brand.objects.filter(name=brand).first()
            if not brand_obj:
                raise ValueError(f"Бренд {brand} не найден в базе данных.")

            with transaction.atomic():
                scraped_data = ScrapedData.objects.create(partner=partner)

                existing_articles = {item.article for item in
                                     ScrapedItem.objects.filter(article__in=[i['article'] for i in items])}

                new_items = [
                    ScrapedItem(
                        name=item['name'],
                        price=item['price'],
                        article=item['article'],
                        status=item['status'],
                        brand=brand_obj
                    )
                    for item in items if item['article'] not in existing_articles
                ]

                if new_items:
                    ScrapedItem.objects.bulk_create(new_items, ignore_conflicts=True)

                all_items = ScrapedItem.objects.filter(article__in=[item['article'] for item in items])

                scraped_data.items.add(*all_items)
                scraped_data.last_update = now()
                scraped_data.save()


        except Exception as e:
            print(f"Ошибка: {str(e)}")
            raise


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
