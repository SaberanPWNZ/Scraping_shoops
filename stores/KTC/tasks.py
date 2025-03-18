
import os

import bs4
import django
import requests

os.environ["DJANGO_SETTINGS_MODULE"] = "scraper.settings"
django.setup()

from scraper.celery_config import app
from stores.KTC.ktc_info import KTC_ARTICLES
from stores.KTC.ktc_model import KtcStore
from stores.KTC.locators import KtcLocator
from utillities import custom_article_extractor
from items.models import Item


@app.task()
def start_ktc_wacom():
    ktc = KtcStore(url=KtcLocator.WACOM_PAGE_URL)
    ktc.load_items(container_locator=KtcLocator.CATALOG_GOODS, item_locator=KtcLocator.ITEM_LOOP)
    items = ktc.generate_info_with_articles(
        title_locator=KtcLocator.ITEM_TITLE,
        price_extractor=lambda elem: ktc.extract_price(elem, locator=KtcLocator.ITEM_PRICE,
                                                       tag=KtcLocator.CONTAINER_LOCATOR_TAG),
        price_locator=KtcLocator.ITEM_PRICE,
        status_locator=KtcLocator.ITEM_STATUS,
        article_extractor=lambda name: custom_article_extractor(name, KTC_ARTICLES)),
    ktc.save_parsed_data(partner_name="KTC", items=items, brand='WACOM')

@app.task()
def start_ktc_xp_pen():
    ktc = KtcStore(url=KtcLocator.XP_PEN_PAGE_URL)
    ktc.load_items(container_locator=KtcLocator.CATALOG_GOODS, item_locator=KtcLocator.ITEM_LOOP)
    items = ktc.generate_info_with_articles(
        price_extractor=lambda elem: ktc.extract_price(elem, locator=KtcLocator.ITEM_PRICE,
                                                       tag=KtcLocator.CONTAINER_LOCATOR_TAG),
        title_locator=KtcLocator.ITEM_TITLE,
        price_locator=KtcLocator.ITEM_PRICE,
        status_locator=KtcLocator.ITEM_STATUS,
        article_extractor=lambda name: custom_article_extractor(name, KTC_ARTICLES)
    )
    ktc.save_parsed_data(partner_name="KTC", items=items, brand='XP-Pen')
