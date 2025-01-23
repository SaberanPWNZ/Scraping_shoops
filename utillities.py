import re


def get_article_from_title(title: str):
    if '(' not in title:
        return None
    article = title.split('(')[1].replace(')', "")
    return article


def clean_price(price: str):
    return re.sub(r'\D', '', price)


def create_message(shop_name, text, brand_name):
    answer = '\n'.join([str(item) for item in text])
    return f"🛒 {shop_name}/{brand_name}:\n\n{answer}"


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
