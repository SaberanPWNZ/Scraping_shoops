def get_article_from_title(title: str):
    article = title.split('(')
    article = article[1].replace(')', "")
    return article

#print(get_article_from_title("Графічний планшет WACOM Intuos Pro L (PTH-860-N)"))


