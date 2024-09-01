import sqlite3
import os
import re

import _sqlite3
from dotenv import load_dotenv
import gspread

from Classes.item import Item
from databases.google_table_ranges import WACOM_RANGES, XP_PEN_RANGES, wacom_table_url, xp_pen_table_url

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'Wacom.db')
conn = _sqlite3.connect(db_path)
cursor = conn.cursor()


def clear_data(items_list):
    return [item for sublist in items_list for item in sublist]


class GoogleSheet:
    ranges_wacom = WACOM_RANGES
    ranges_xppen = XP_PEN_RANGES
    google_token = os.getenv("GOOGLE_TOKEN")
    path_to_keys = gspread.api_key(token=google_token)
    xp_pen_table_url = xp_pen_table_url
    wacom_table_url = wacom_table_url

    def generate_info_from_google_sheet_list(self, google_sheet_url):
        try:
            data = self.path_to_keys.open_by_url(url=google_sheet_url)
            worksheet = data.worksheet(title='WACOM')
            records = worksheet.get_all_values()

        except gspread.exceptions.WorksheetNotFound as error:
            raise error
        except gspread.exceptions.GSpreadException as error:
            raise error
        return records

    def generate_info_from_google_sheet(self, google_sheet_url, ranges):
        global cleaned_data_list
        try:
            cleaned_data_list = []
            test_sheet = self.path_to_keys.open_by_url(url=google_sheet_url)
            row_data_article = test_sheet.sheet1.batch_get([rng[0] for rng in ranges])
            row_data_title = test_sheet.sheet1.batch_get([rng[1] for rng in ranges])
            row_data_price = test_sheet.sheet1.batch_get([rng[2] for rng in ranges])

            clean_title = clear_data(row_data_title)
            clean_article = clear_data(row_data_article)
            clean_price = clear_data(row_data_price)

            final_data = [{'title': title, 'price': price, 'article': article}
                          for title, price, article in zip(clean_title, clean_price, clean_article)]

            for item in final_data:
                cleaned_data_list.append(
                    item
                )
        except:
            raise Exception
        finally:
            return cleaned_data_list

    def clear_info_from_sheets_lists(self, list_of_items: list):
        items = []
        try:
            for item in list_of_items:
                if len(item[1]) > 0:
                    price_raw = item[4]
                    price_clean = (re.sub(r'\xa0', '', price_raw).strip().
                               replace(',00', '').replace(' ', ''))

                    clear_data = {
                        'title': item[1],
                        'price': price_clean,
                        'article': item[0]
                    }
                    items.append(clear_data)
                else:
                    continue
            return items
        except Exception as error:
            raise error

    def clear_info_from_sheets(self, list_of_items: list):
        items = []
        for item in list_of_items:
            price_raw = item['price'][0]
            price_clean = (re.sub(r'\xa0', '', price_raw).strip().
                           replace(',00', '').replace(' ', ''))

            clear_data = {
                'title': item['title'][0],
                'price': price_clean,
                'article': item['article'][0]
            }
            items.append(clear_data)
        return items


# DELETE AFTER TESTS
def get_info_from_db():
    items_from_db = []
    cursor.execute('''SELECT * FROM WACOM''')
    all_from_table = cursor.fetchall()

    for elem in all_from_table:
        item = Item.from_tuple(elem)
        items_from_db.append(item)
    return items_from_db






