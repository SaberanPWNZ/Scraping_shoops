import os
import django
import requests
from bs4 import BeautifulSoup

os.environ["DJANGO_SETTINGS_MODULE"] = "scraper.settings"
django.setup()

from scraper.celery_config import app
from stores.telemart.telemart_info import TelemartLocators, TELEMART_ARTICLES_XP_PEN, TELEMART_ARTICLES_WACOM
from stores.telemart.telemart_model import Telemart
from utillities import custom_article_extractor


@app.task()
def start_telemart_wacom():
    telemart = Telemart(url=TelemartLocators.WACOM_URL)
    telemart.load_items(container_locator=TelemartLocators.CONTAINER_LOCATOR, pages=2,
                        item_locator=TelemartLocators.ITEM_BOX_LOCATOR, tag=TelemartLocators.CONTAINER_LOCATOR_TAG)
    items = telemart.generate_info_with_articles(
        title_locator=TelemartLocators.ITEM_TITLE,
        price_extractor=lambda elem: telemart.extract_price(
            elem,
            tag=TelemartLocators.CONTAINER_LOCATOR_TAG,
            locator=TelemartLocators.ITEM_PRICE),
        price_locator=TelemartLocators.ITEM_PRICE,
        status_locator=TelemartLocators.ITEM_STATUS,
        article_extractor=lambda name: custom_article_extractor(name, TELEMART_ARTICLES_WACOM)
    )

    telemart.save_parsed_data(partner_name="Telemart", items=items, brand='WACOM')


@app.task()
def start_telemart_xp_pen():
    telemart = Telemart(url=TelemartLocators.XP_PEN_URL)
    telemart.load_items(container_locator=TelemartLocators.CONTAINER_LOCATOR, pages=2,
                        item_locator=TelemartLocators.ITEM_BOX_LOCATOR, tag=TelemartLocators.CONTAINER_LOCATOR_TAG)
    items = telemart.generate_info_with_articles(
        title_locator=TelemartLocators.ITEM_TITLE,
        price_extractor=lambda elem: telemart.extract_price(
            elem,
            tag=TelemartLocators.CONTAINER_LOCATOR_TAG,
            locator=TelemartLocators.ITEM_PRICE),
        price_locator=TelemartLocators.ITEM_PRICE,
        status_locator=TelemartLocators.ITEM_STATUS,
        article_extractor=lambda name: custom_article_extractor(name, TELEMART_ARTICLES_XP_PEN)
    )

    telemart.save_parsed_data(partner_name="Telemart", items=items, brand='XP-Pen')

