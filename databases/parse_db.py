import _sqlite3
import os
import re

from dotenv import load_dotenv
import gspread

from Classes.item import Item

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'Wacom.db')
conn = _sqlite3.connect(db_path)
cursor = conn.cursor()


def clear_data(items_list):
    return [item for sublist in items_list for item in sublist]


class GoogleSheet:
    ranges = [('A3:A10', 'b3:b10', 'E3:E10'),
              ('A12:A14', 'b12:b14', 'E12:E14'),
              ('A17:A27', 'b17:b27', 'E17:E27'),
              ('A30:A32', 'b30:b32', 'E30:E32'),
              ('A34:A44', 'b34:b44', 'E34:E44'),
              ('A47:A60', 'b47:b60', 'E47:E60'),
              ('A62:A64', 'b62:b64', 'E62:E64'),
              ('A66:A67', 'b66:b67', 'E66:E67')]
    google_token = os.getenv("GOOGLE_TOKEN")
    path_to_keys = gspread.api_key(token=google_token)

    def generate_info_from_google_sheet(self):
        cleaned_data_list = []
        test_sheet = self.path_to_keys.open_by_url(
            "https://docs.google.com/spreadsheets/d/1v3LhZ__mm9G2F0nEdLlQzQ-YcqWYvXGpI9f6ijeC9jY/edit#gid=0")
        row_data_article = test_sheet.sheet1.batch_get([rng[0] for rng in GoogleSheet.ranges])
        row_data_title = test_sheet.sheet1.batch_get([rng[1] for rng in GoogleSheet.ranges])
        row_data_price = test_sheet.sheet1.batch_get([rng[2] for rng in GoogleSheet.ranges])

        clean_title = clear_data(row_data_title)
        clean_article = clear_data(row_data_article)
        clean_price = clear_data(row_data_price)

        final_data = [{'title': title, 'price': price, 'article': article}
                      for title, price, article in zip(clean_title, clean_price, clean_article)]

        for item in final_data:
            cleaned_data_list.append(
                item
            )

        return cleaned_data_list

    def insert_new_info(self, item: Item):
        # cursor.execute('''CREATE TABLE IF NOT EXISTS WACOM (
        #                     id INTEGER PRIMARY KEY,
        #                     article TEXT NOT NULL,
        #                     title TEXT NOT NULL,
        #                     price INTEGER NOT NULL
        #                 )''')

        # for item in items_list:
        #     article = item[2].strip()
        #     title = item[0].strip()
        #     price = item[1].strip().replace(' ', "").replace(',00', '').replace(',', "")
        cursor.execute('''INSERT INTO WACOM(article, title, price)
            VALUES (?, ?, ?)''', (item.article, item.title, item.price))

        conn.commit()

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
        yield item
    return items_from_db


