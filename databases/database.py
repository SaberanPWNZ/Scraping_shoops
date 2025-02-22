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
        cleared_data = parser.clear_info_from_sheets(data)
        update_database(cleared_data)
    except Exception as ex:
        logger.error(F'не вдалось оновити БД - {ex}')