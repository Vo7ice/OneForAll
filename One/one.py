import leancloud
import requests
from bs4 import BeautifulSoup
from One import config

from requests.adapters import HTTPAdapter

__author__ = 'Vo7ice'


class One:
    def __init__(self):
        leancloud.init("v87HMWzSFKhBWMlQJMAwV7zz-gzGzoHsz", "010HkHf27pPGD0KfW7oANxQb")
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def start(self, head=config.base_url, foot=config.one_url):
        url = head + foot
        print('url:', url)
        req = requests.get(url, headers=self.headers)
        print('req status_code:', req.status_code)
        if req.status_code == config.SUCCESS:
            soup = BeautifulSoup(req.content, 'html.parser')
            image = soup.find('div', class_='one-imagen').img['src']
            print('image:', image)
            image_titulo = soup.find('div', class_='one-titulo').text.strip()
            print('image_titulo:', image_titulo)
            image_leyenda = soup.find('div', class_='one-imagen-leyenda').text.strip()
            print('image_leyenda:', image_leyenda)
            one_cita = soup.find('div', class_='one-cita').text.strip()
            print('one_cita:', one_cita)
            dom = soup.find('p', class_='dom').text.strip()
            print('dom:', dom)
            may = soup.find('p', class_='may').text.strip()
            print('may:', may)
        else:
            print('network error')


def main():
    s = requests.session()
    s.mount(config.base_url, HTTPAdapter(max_retries=5))
    s.keep_alive = False


main()
one = One()
one.start()
