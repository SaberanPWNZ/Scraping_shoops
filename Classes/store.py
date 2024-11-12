import requests
from bs4 import BeautifulSoup

from databases.db_helper import get_info_from_db, get_session
from stores.Itbox.itbox_info import ITBOX_HEADERS


class BaseStore:
    def __init__(self, shop_url, headers=ITBOX_HEADERS, cookies=None, ):
        self.item_list = []
        self.url = shop_url
        self.headers = headers
        self.cookies = cookies
        self.all_items = []

    @staticmethod
    def get(self, shop_url):
        response = requests.get(url=shop_url, headers=self.headers)
        return response

    def compare_data(self, partner_list):
        session = get_session()
        items_from_db = list(get_info_from_db(session=get_session()))
        items_dict = {item.article: item for item in items_from_db}

        missing_items = []

        for elem in partner_list:
            try:
                article = elem.get('article', '').upper()
                if not article:
                    raise ValueError(f'Article is missing or empty in element: {elem}')

                price_partner = int(elem['price'])

                if article in items_dict:
                    item = items_dict[article]
                    item_price = int(item.price.decode('utf-8')) if isinstance(item.price, bytes) else int(item.price)
                    if price_partner == item_price:

                        missing_items.append(f'✅{article} - Ціна партнера- {price_partner} грн, РРЦ {item_price} грн')

                    elif price_partner < item_price:
                        missing_items.append(
                            f'🛑 Ціна нижча за РРЦ {article} - {price_partner} грн, Ціна РРЦ = {item_price} грн')

                    elif price_partner > item_price:
                        missing_items.append(
                            f'⚠️ Ціна вища за РРЦ {article} - {price_partner} грн, Ціна РРЦ = {item_price} грн')
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


class Soup:
    def __init__(self, response):
        self.soup = BeautifulSoup(response.text, 'lxml')

    def find_element(self, **kwargs):
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
