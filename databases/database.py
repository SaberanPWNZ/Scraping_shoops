import logging

from databases.db_helper import update_database
from databases.parse_db import GoogleSheet
from scraper.celery_config import app

logger = logging.getLogger(__name__)


@app.task()
def shedule_updating_db_wacom():
    try:
        parser = GoogleSheet()
        data = parser.generate_info_from_google_sheet_list(
            google_sheet_url=parser.wacom_table_url,
            sheet_name='WACOM')
        cleared_data = parser.clear_info_from_sheets(list_of_items=data,
                                                     elem_positions=parser.wacom_elem_position,
                                                     len_items=parser.wacom_length_of_item_from_table)
        update_database(cleared_data)
    except Exception as ex:
        logger.error(F'не вдалось оновити БД - {ex}')


@app.task()
def shedule_updating_db_xp_pen():
    try:
        parser = GoogleSheet()
        data = parser.generate_info_from_google_sheet_list(
            google_sheet_url=parser.xp_pen_table_url,
            sheet_name='XP-PEN')
        cleared_data = parser.clear_info_from_sheets(list_of_items=data,
                                                     elem_positions=parser.xp_pen_elem_position,
                                                     len_items=parser.xp_pen_length_of_item_from_table)
        update_database(cleared_data)
    except Exception as ex:
        logger.error(F'не вдалось оновити БД - {ex}')
