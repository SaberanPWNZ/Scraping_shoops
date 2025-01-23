import os
import re
from dotenv import load_dotenv
import gspread

from databases.google_table_ranges import WACOM_RANGES, XP_PEN_RANGES, wacom_table_url, xp_pen_table_url
from utillities import _clean_price, check_length

load_dotenv()


def clear_data(items_list):
    return [item for sublist in items_list for item in sublist]


class GoogleSheet:
    ranges_wacom = WACOM_RANGES
    ranges_xppen = XP_PEN_RANGES
    google_token = os.getenv("GOOGLE_TOKEN")
    path_to_keys = gspread.api_key(token=google_token)
    xp_pen_table_url = xp_pen_table_url
    wacom_table_url = wacom_table_url

    def generate_info_from_google_sheet_list(self, google_sheet_url, sheet_name):
        try:
            data = self.path_to_keys.open_by_url(url=google_sheet_url)
            worksheet = data.worksheet(title=sheet_name)
            records = worksheet.get_all_values()

        except gspread.exceptions.WorksheetNotFound as error:
            raise error
        except gspread.exceptions.GSpreadException as error:
            raise error
        return records

    def generate_info_from_google_sheet(self, google_sheet_url, ranges):
        cleaned_data_list = []
        try:
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


    def clear_info_from_sheets(self, list_of_items: list):
        items = []
        try:
            for item in list_of_items:
                if len(item) == 7:
                    if check_length(item):
                        clear_data = {
                            'article': item[0],
                            'title': item[1],
                            'status': item[2],
                            'partner_price': _clean_price(item[3]) if 'підзапит' not in item[3] else 0.0,
                            'rrp_price': _clean_price(item[4]) if 'підзапит' not in item[4] else 0.0,
                            'warranty': item[5],
                            'ean': item[6],
                        }
                        items.append(clear_data)
        except Exception as error:
            raise error
        return items


