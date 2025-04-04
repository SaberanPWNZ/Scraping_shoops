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
        self.pagination_param = "?page="

    #def load_items(self, pages=1, tag=None, container_locator=None, item_locator=None, headers=None):


    def get_soup(self, link):
        response = requests.get(link, headers=self.headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')

    def send_allert_notification(self):
        send_telegram_message_task(message=f'Не вдалось завантажити данні - {self.__class__.__name__}')

    def load_items(self, container_locator=None, item_locator=None, pages=None, tag=None):

        self.all_items = []
        if isinstance(pages, int):
            urls = [f"{self.url}{self.pagination_param}{i}" for i in range(1, pages + 1)]
        elif isinstance(pages, list):
            urls = pages
        else:
            raise ValueError("`pages`must be int (pages count) or list.")

        for url in urls:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Error with {url}: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            self.all_items.extend(self.extract_items_by_locator(soup, container_locator, item_locator, tag))

        return self.all_items

    def extract_items_by_locator(self, soup, container_locator, item_locator, tag=None, ):
        container = soup.find(tag, class_=container_locator)
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

    def generate_info_with_articles(self, title_locator=None,
                                    price_locator=None, status_locator=None,
                                    article_extractor=None, price_extractor=None, status_extractor=None):
        if not self.all_items:
            raise ValueError("Данные не загружены. Передайте список товаров.")

    def _generate_info_with_articles(self, title_locator=None, price_locator=None, status_locator=None,
                                     article_extractor=None, price_extractor=None, status_extractor=None):
        if self.all_items is None:
            raise ValueError("Данные не загружены. Вызовите `load_items` перед генерацией информации.")


        item_list = []
        for elem in self.all_items:
            name_element = elem.find(class_=title_locator) if title_locator else None
            name = name_element.get_text(strip=True) if name_element else None

            article = article_extractor(name) if article_extractor and name else None

            price = None
            if price_extractor:
                extracted_price = price_extractor(elem)
                price = clean_price(extracted_price) if extracted_price else None
            elif price_locator:
                price_element = elem.select_one(price_locator)
                price = clean_price(price_element.get_text(strip=True)) if price_element else None

            status = None
            if status_extractor:
                status = status_extractor(elem)
            elif status_locator:
                status_element = elem.select_one(status_locator)
                status = Status.not_in_stock if status_element else Status.in_stock

            item_list.append({
                'name': name,
                'article': article,
                'price': price,
                'status': status,
            })

        return item_list

    def generate_info_with_many_links(self, links: list, products_link_locator: str, name_elem_locator: str,
                                      price_elem_locator: str, article_elem_locator: str):
        for link in links:
            soup = self.get_soup(link)
            product_items = soup.find_all(
                class_=products_link_locator
            )

            for item in product_items:
                try:
                    name_elem = item.find(class_=name_elem_locator)
                    price_elem = item.find(class_=price_elem_locator)
                    article_elem = item.find(class_=article_elem_locator)

                    price = price_elem.text.strip().split('₴')[0].strip().replace(' ', '') if price_elem else "0"
                    article = article_elem.text.strip() if article_elem else "None"

                    card_item = {
                        "name": name_elem.text.strip() if name_elem else "N/A",
                        "price": price.split(',')[0],
                        "article": article,
                        "status": Status.in_stock
                    }
                    self.items.append(card_item)

                except Exception as ex:
                    print(f"Ошибка при обработке {link}: {ex}")

        return self.items

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

    def extract_price(self, element, locator=None, tag=None, attribute=None):
        if attribute and element.has_attr(attribute):
            return clean_price(element[attribute])
        if tag and locator:
            price_element = element.find(tag, class_=locator)
            if price_element:
                return clean_price(price_element.get_text(strip=True))

        return None


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
