import re

import leancloud
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

from One import config
from One.one import One


class Index:
    def __init__(self):
        leancloud.init("v87HMWzSFKhBWMlQJMAwV7zz-gzGzoHsz", "010HkHf27pPGD0KfW7oANxQb")
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def start(self, url=config.base_url):
        print('url:', url)
        req = requests.get(url, headers=self.headers)
        print('req status_code:', req.status_code)
        if req.status_code == config.SUCCESS:
            soup = BeautifulSoup(req.content, 'html.parser')
            one_urls = []
            article_urls = []
            question_urls = []
            # 找到所有图片的url
            item_list = soup.findAll('div', class_='item')
            print('item_list size:', len(item_list))
            for i in item_list:
                print('oen url:', i.a['href'])
                one_urls.append(i.a['href'][-len(config.one_url):])
                # one = One()
                # one.start(config.base_url, one_foot_url)

            # 找到所有文章的url
            active = soup.find('p', class_='one-articulo-titulo').a['href'][-len(config.article_url):]
            article_urls.append(active)
            article_list = soup.find('div', class_='fp-one-articulo') \
                .find('ul', class_='list-unstyled pasado').findAll('li')
            print('article_list size:', len(article_list))
            for i in article_list:
                print('article url:', i.a['href'])
                article_urls.append(i.a['href'][-len(config.article_url):])

            # 找到所有问题的url
            active = soup.find('p', class_='one-cuestion-titulo').a['href'][-len(config.question_url):]
            question_urls.append(active)
            question_list = soup.find('div', class_='fp-one-cuestion') \
                .find('ul', class_='list-unstyled pasado').findAll('li')
            for i in question_list:
                print('question url:', i.a['href'])
                question_urls.append(i.a['href'][-len(config.question_url):])

            for j in one_urls:
                print('one url:', j)

            for x in article_urls:
                print('article url:', x)

            for k in question_urls:
                print('question url:', k)
        else:
            print('network error')


def main():
    s = requests.session()
    s.mount(config.base_url, HTTPAdapter(max_retries=5))
    s.keep_alive = False
    index = Index()
    index.start(config.base_url)


main()
