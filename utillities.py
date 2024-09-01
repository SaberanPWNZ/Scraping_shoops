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
