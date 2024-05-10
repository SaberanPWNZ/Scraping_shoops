import requests



class BaseStore:
    def __init__(self, url, headers=None, cookies=None):
        self.url = url
        self.headers = headers
        self.cookies = cookies

    def get(self):
        return requests.get(self.url, self.headers)

    def post(self):
        return requests.post(self.url, self.headers)




