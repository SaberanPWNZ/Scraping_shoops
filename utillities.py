import re


def get_article_from_title(title: str):
    if '(' not in title:
        return None
    article = title.split('(')[1].replace(')', "")
    return article


def clean_price(price: str):
    return re.sub(r'\D', '', price)


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}


AUCHAN_ARTICLES = {
    'Графический планшет Wacom Intuos M Bluetooth Black': 'CTL-6100WLK-N',
    'Графический планшет Wacom Intuos S Bluetooth Black': 'CTL-4100WLK-N',
    'Графический планшет Wacom Intuos S Black': 'CTL-4100K-N',
    'Графический планшет Wacom Intuos M Black': 'CTL-6100K-B',
    'Графический планшет Wacom Intuos Pro L': 'PTH-860-N',
    'Монитор-планшет Wacom Cintiq 22': 'DTK2260K0A',
    'Монитор-планшет Wacom Cintiq 16FHD': 'DTK1660K0B',
    'Графический планшет Wacom Intuos S Bluetooth Manga черный': 'CTL-4100WLK-M',
    'Монитор-планшет Wacom Cintiq 24 Pro UHD': 'DTK-2420',
    'Графический планшет Wacom One by Medium Red': 'CTL-672-N',
    'Графический планшет Wacom Intuos Pro M': 'PTH-660-N',
    'Графический планшет Wacom Intuos Pro S': 'PTH460K0B',
    'Монитор-планшет Wacom Cintiq 24 ProTouch': 'DTH-2420',
    'Монитор-планшет Wacom Cintiq Pro 16 2021': 'DTH167K0B',
    'Графический планшет Wacom Intuos M Bluetooth Pistachio': 'CTL-6100WLE-N',
    'Графический планшет Wacom One by Small Black': 'CTL-472-N',
    'Графический планшет Wacom Intuos S Bluetooth Pistachio': 'CTL-4100WLE-N'

}



