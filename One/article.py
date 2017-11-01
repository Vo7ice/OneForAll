import leancloud
from leancloud import Object
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

    def start(self, head=config.base_url, foot=config.article_url, vol='-1'):
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

            article_save = check_article_vol_exist(vol)
            if article_save is None:
                ArticleSave = leancloud.Object.extend('ArticleSave')
                article_save = ArticleSave()
                article_save.set('article_url', foot)
                article_save.set('article_vol', vol)
                article_save.set('article_quote', comilla_cerrar)
                article_save.set('article_title', articulo_titulo)
                article_save.set('article_author', articulo_autor)
                article_save.set('article_content', content_after)
                article_save.set('article_editor', articulo_editor)
                article_save.save()
            else:
                pass
        else:
            print('network error')


class ArticleSave(Object):
    @property
    def article_url(self):
        return self.get('article_url')

    @article_url.setter
    def article_url(self, value):
        return self.set('article_url', value)

    @property
    def article_quote(self):
        return self.get('article_quote')

    @article_quote.setter
    def article_quote(self, value):
        return self.set('article_quote', value)

    @property
    def article_title(self):
        return self.get('article_title')

    @article_title.setter
    def article_title(self, value):
        return self.set('article_title', value)

    @property
    def article_author(self):
        return self.get('article_author')

    @article_author.setter
    def article_author(self, value):
        return self.set('article_author', value)

    @property
    def article_content(self):
        return self.get('article_content')

    @article_content.setter
    def article_content(self, value):
        return self.set('article_content', value)

    @property
    def article_editor(self):
        return self.get('article_editor')

    @article_editor.setter
    def article_editor(self, value):
        return self.set('article_editor', value)

    @property
    def article_vol(self):
        return self.get('article_vol')

    @article_vol.setter
    def article_vol(self, value):
        return self.set('article_vol', value)


def check_article_vol_exist(vol):
    if vol == -1:
        return True
    ArticleSave = leancloud.Object.extend('ArticleSave')
    query = ArticleSave.query
    try:
        article_info = query.equal_to('article_vol', vol).find()[0]
    except IndexError as e:
        print('IndexError')
        article_info = None
    return article_info


def main():
    s = requests.session()
    s.mount(config.base_url, HTTPAdapter(max_retries=5))
    s.keep_alive = False


main()
article = Article()
article.start()
