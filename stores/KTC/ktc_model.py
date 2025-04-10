from Classes.store import BaseStore, Scraper
from stores.KTC.locators import KtcLocator
from utillities import custom_article_extractor, clean_price

class KtcStore(BaseStore):
    def __init__(self, url):
        super().__init__(shop_url=url)
        self.scraper = Scraper()

    def generate_info_xp_pen(self, partner_dict: dict) -> None:
    
        return self._generate_info_with_articles(
            title_locator=KtcLocator.ITEM_TITLE,
            price_locator=KtcLocator.ITEM_PRICE,
            status_locator=KtcLocator.ITEM_STATUS,
            article_extractor=lambda name: custom_article_extractor(name, partner_dict),
            price_extractor=lambda elem: min(
                [
                    clean_price(p.get_text(strip=True))
                    for p in elem.select(KtcLocator.ITEM_PRICE)
                    if clean_price(p.get_text(strip=True)).isdigit()
                ],
                default=None,
            ),
        )
