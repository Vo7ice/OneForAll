import leancloud
import requests
from bs4 import BeautifulSoup
from One import config

from requests.adapters import HTTPAdapter

__author__ = 'Vo7ice'


class Article:
    def __init__(self):
        leancloud.init("v87HMWzSFKhBWMlQJMAwV7zz-gzGzoHsz", "010HkHf27pPGD0KfW7oANxQb")
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def start(self, head=config.base_url, foot=config.article_url):
        url = head + foot
        print('url:', url)
        req = requests.get(url, headers=self.headers)
        print('req status_code:', req.status_code)
        if req.status_code == config.SUCCESS:
            soup = BeautifulSoup(req.content, 'html.parser')
            comilla_cerrar = soup.find('div', class_='comilla-cerrar').text.strip()
            print('comilla_cerrar:', comilla_cerrar)
            articulo_titulo = soup.find('h2', class_='articulo-titulo').text.strip()
            print('articulo-titulo:', articulo_titulo)
            articulo_autor = soup.find('p', class_='articulo-autor').text.strip()
            print('articulo-autor:', articulo_autor)
            content_list = soup.find('div', class_='articulo-contenido').findAll('p')
            print('content_list size:', len(content_list))
            paragraph = []
            for content in content_list:
                # print('content:', content.text)
                paragraph.append(content.text)
            content_after = '\n'.join(paragraph)
            print('content_after:', content_after)
            articulo_editor = soup.find('p', class_='articulo-editor').text.strip()
            print('articulo-editor:', articulo_editor)
        else:
            print('network error')


def main():
    s = requests.session()
    s.mount(config.base_url, HTTPAdapter(max_retries=5))
    s.keep_alive = False


main()
article = Article()
article.start()
