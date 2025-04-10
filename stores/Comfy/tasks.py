import logging
import os

import django

from scraper.celery_config import app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraper.settings")
django.setup()
from stores.Comfy.comfy_info import ComfyLocators, wacom_comfy_payload, xp_pen_comfy_payload
from stores.Comfy.comfy_model import ComfyStore

logger = logging.getLogger('scraping')


@app.task()
def start_comfy_wacom():
    try:
        comfy = ComfyStore()
        items = comfy.generate_info(payload=wacom_comfy_payload, articles_dict=ComfyLocators.COMFY_WACOM_ARICLES)
        if not items:
            logger.info(f"Не вдалось спарсити данні Comfy/WACOM - {len(items)} товарів")
            comfy.send_allert_notification()
        logger.info(f"Збережено/Оновлено {len(items)} товарів для партнера Comfy (бренд WACOM).")
        comfy.save_parsed_data(partner_name="Comfy", items=items, brand="WACOM")
    except Exception as e:
        logger.info(f"Помилка парсингу данних Comfy/WACOM {e}")


@app.task()
def start_comfy_xp_pen():
    try:
        comfy = ComfyStore()
        items = comfy.generate_info(payload=xp_pen_comfy_payload, articles_dict=ComfyLocators.COMFY_XP_PEN_ARTICLES)
        if not items:
            logger.info(f"Не вдалось спарсити данні Comfy/XP-Pen - {len(items)} товарів")
            comfy.send_allert_notification()
        logger.info(f"Збережено/Оновлено {len(items)} товарів для партнера Comfy (бренд XP-Pen).")
        comfy.save_parsed_data(partner_name="Comfy", items=items, brand="XP-Pen")
    except Exception as e:
        logger.info(f"Помилка парсингу данних Comfy/XP-Pen {e}")
