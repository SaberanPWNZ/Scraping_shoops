from Classes.store import BaseStore, Scraper
from stores.Telemart.telemart_info import TelemartLocators


class Telemart(BaseStore):
    def __init__(self, url):
        super().__init__(shop_url=url)
        self.scraper = Scraper()

    def generate_info_xp_pen(self):
        return self.generate_info(
            title_locator=TelemartLocators.ITEM_TITLE,
            price_locator=TelemartLocators.ITEM_PRICE,
            status_locator=TelemartLocators.ITEM_STATUS
        )

