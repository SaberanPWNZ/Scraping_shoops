
import django
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "scraper.settings"
django.setup()

from scraper.celery_config import app
from stores.KTC.ktc_info import KTC_ARTICLES
from stores.KTC.ktc_model import KtcStore
from stores.KTC.locators import KtcLocator
from utillities import custom_article_extractor
from ktc_info import KTC_ARTICLES
import logging


logger = logging.getLogger('scraping')

#@app.task()
def start_ktc_wacom():
    try:
        ktc = KtcStore(url=KtcLocator.WACOM_PAGE_URL)
        ktc.load_items(container_locator=KtcLocator.CATALOG_GOODS, item_locator=KtcLocator.ITEM_LOOP, pages=2)
        items = ktc.generate_info_xp_pen(partner_dict=KTC_ARTICLES)
        if not items:
            logger.info(f"Не вдалось спарсити данні KTC/WACOM - {len(items)} товарів")
            ktc.send_allert_notification()

        ktc.save_parsed_data(partner_name="KTC", items=items, brand='WACOM')
        logger.info(f"Збережено/Оновлено {len(items)} товарів для партнера KTC (бренд WACOM).")

    except Exception as e:
        logger.info(f"Помилка парсингу данних KTC/XP-Pen {e}")



#@app.task()
def start_ktc_xp_pen():
    try:
        ktc = KtcStore(url=KtcLocator.XP_PEN_PAGE_URL)
        ktc.load_items(container_locator=KtcLocator.CATALOG_GOODS, item_locator=KtcLocator.ITEM_LOOP, pages=2)
        items = ktc.generate_info_xp_pen(partner_dict=KTC_ARTICLES)
        if not items:
            logger.info(f"Не вдалось спарсити данні KTC/XP-Pen - {len(items)} товарів")
            ktc.send_allert_notification()

        ktc.save_parsed_data(partner_name="KTC", items=items, brand='XP-Pen')
        logger.info(f"Збережено/Оновлено {len(items)} товарів для партнера KTC (бренд XP-Pen).")

    except Exception as e:
        logger.info(f"Помилка парсингу данних KTC/XP-Pen {e}")

