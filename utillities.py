import re
from datetime import datetime


def get_article_from_title(title: str):
    if '(' not in title:
        return None
    article = title.split('(')[1].replace(')', "")
    return article


def clean_price(price: str):
    return re.sub(r'\D', '', price)


from datetime import datetime


def create_message(partner_name: str, price: float, article: str,
                   time: datetime, price_prediction:bool) -> str:
    formatted_time = time.strftime("%d.%m.%Y %H:%M")
    price_moving = 'ціна збільшилась' if price_prediction else 'ціна зменшилась'
    text = (
        f"<b>{partner_name}</b> - {price_moving}\n"
        f"<code>{article}</code> - "
        f"<b>{price:.2f} грн</b> "
        f"({formatted_time})"
    )
    return text



def _clean_price(price_raw):
    if not price_raw:
        return 0.0

    try:
        price_clean = re.sub(r'\xa0|\s', '', price_raw).replace(',', '.')
        return float(price_clean)
    except (ValueError, TypeError):
        return 0.0



def custom_article_extractor(name, articles_dict):
    return articles_dict.get(name, get_article_from_title(name))


def check_length(lst):
    for item in lst:
        if item == "":
            return False
    return True
