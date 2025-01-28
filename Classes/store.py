import asyncio
import logging
import os
import django
from typing import List
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from datetime import datetime

from django.utils import timezone

from Classes.status import Status
from checker.models import Partner, PartnerItem, PriceHistory
from telegram_bot.bot import send_telegram_message_task
from utillities import get_article_from_title, clean_price, create_message

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraper.settings")

if not settings.configured:
    django.setup()

from items.models import Item, Brand

logger = logging.getLogger()


class BaseStore:
    def __init__(self, shop_url, headers=None, cookies=None):
        self.soup = Scraper()
        self.url = shop_url
        self.headers = headers
        self.cookies = cookies
        self.all_items = None

    def __str__(self):
        return

    def send_allert_notification(self):
        send_telegram_message_task(message=f'Не вдалось завантажити данні - {self.__class__.__name__}')

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

    def save_parsed_data(self, partner_name, items, brand):
        brand_instance = Brand.objects.get_or_create(name=brand)
        if not brand_instance:
            raise ValueError(f"Бренд '{brand}' не знайдено.")

        partner, _ = Partner.objects.get_or_create(name=partner_name)

        for item in items:
            article = item.get('article')
            price = item.get('price')
            raw_status = item.get('status')

            if not article:
                continue

            if price is None or price == "":
                continue
            try:
                price = float(price)
            except ValueError:
                continue

            availability = False
            if raw_status is not None:
                availability = raw_status.lower() in ['в наявності', 'доступно', 'есть']
            partner_item, created = PartnerItem.objects.get_or_create(
                partner=partner,
                article=article,
                defaults={
                    'price': price,
                    'availability': availability,
                    'last_updated': datetime.now()
                }
            )

            PriceHistory.objects.create(
                partner_item=partner_item,
                price=partner_item.price
            )
            new_price = price
            time = datetime.utcnow()
            if partner_item.price < new_price and availability == True:
                old_price = partner_item.price
                prediction = True
                message = create_message(partner_name, new_price, partner_item.article, time, prediction)
                send_telegram_message_task.delay(message)
            if new_price < partner_item.price and availability == True:
                prediction = False
                message = create_message(partner_name, new_price, partner_item.article, time, prediction)
                send_telegram_message_task.delay(message)

            partner_item.price = price
            partner_item.availability = availability
            partner_item.last_updated = timezone.now()
            partner_item.save()


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
