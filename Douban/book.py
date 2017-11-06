import leancloud
from leancloud import Object
import requests
from requests.adapters import HTTPAdapter

from Douban import config


class Book:
    def __init__(self):
        leancloud.init("v87HMWzSFKhBWMlQJMAwV7zz-gzGzoHsz", "010HkHf27pPGD0KfW7oANxQb")
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def start(self, base_url=config.base_book_url, foot_url=config.foot_book_url):
        pass


def main():
    s = requests.session()
    s.mount(config.base_book_url, HTTPAdapter(max_retries=5))
    s.keep_alive = False


if __name__ == '__main__':
    main()
    book = Book()
    book.start()
