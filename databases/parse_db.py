import logging
import os
import re
from dotenv import load_dotenv
import gspread

from databases.google_table_ranges import WACOM_RANGES, XP_PEN_RANGES, wacom_table_url, xp_pen_table_url
from utillities import _clean_price, check_length

load_dotenv()
logger = logging.getLogger(__name__)


def clear_data(items_list):
    return [item for sublist in items_list for item in sublist]


class GoogleSheet:
    ranges_wacom = WACOM_RANGES
    ranges_xppen = XP_PEN_RANGES
    google_token = os.getenv("GOOGLE_TOKEN")
    path_to_keys = gspread.api_key(token=google_token)
    xp_pen_table_url = xp_pen_table_url
    wacom_table_url = wacom_table_url
    xp_pen_length_of_item_from_table = 8
    wacom_length_of_item_from_table = 7
    xp_pen_elem_position = {
        'article': 1,
        'title': 2,
        'status': 3,
        'partner_price': 4,
        'rrp_price': 5,
        'warranty': 6,
        'ean': 7
    }
    wacom_elem_position = {
        'article': 0,
        'title': 1,
        'status': 2,
        'partner_price': 3,
        'rrp_price': 4,
        'warranty': 5,
        'ean': 6
    }

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

    def clear_info_from_sheets(self, list_of_items: list, elem_positions: dict, len_items: int):
        items = []
        try:

            for item in list_of_items:
                if len(item) == len_items:
                    if check_length(item):
                        try:
                            partner_price_raw = item[elem_positions['partner_price']]
                            rrp_price_raw = item[elem_positions['rrp_price']]

                            clear_data = {
                                'article': item[elem_positions['article']],
                                'title': item[elem_positions['title']],
                                'status': item[elem_positions['status']],
                                'partner_price': _clean_price(
                                    partner_price_raw) if 'підзапит' not in partner_price_raw else 0.0,
                                'rrp_price': _clean_price(rrp_price_raw) if 'підзапит' not in rrp_price_raw else 0.0,
                                'warranty': item[5],
                                'ean': item[6],
                            }
                            items.append(clear_data)
                        except Exception as e:
                            logger.error(f'Ошибка обработки элемента {item}: {e}', exc_info=True)
        except Exception as error:
            logger.error(f'Ошибка в clear_info_from_sheets: {error}', exc_info=True)
            raise error
        logger.info(f'Обработано {len(items)} элементов')
        return items
