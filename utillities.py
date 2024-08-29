import re


def get_article_from_title(title: str):
    if '(' not in title:
        return None
    article = title.split('(')[1].replace(')', "")
    return article


def clean_price(price: str):
    return re.sub(r'\D', '', price)





