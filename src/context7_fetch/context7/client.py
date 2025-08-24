from requests import Session


class Client:
    BASE_URL = "https://context7.com"

    def __init__(self):
        self.base_url = self.BASE_URL
        self.session = Session()
