def get_article_from_title(title: str):
    article = title.split('(')
    article = article[1].replace(')', "")
    return article




