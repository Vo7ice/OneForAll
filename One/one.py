import leancloud
from leancloud import Object
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

    def start(self, head=config.base_url, foot=config.one_url, vol='-1'):
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

            one_save = check_vol_exist(vol)
            print('vol', vol)
            if one_save is None:
                OneSave = leancloud.Object.extend('OneSave')
                one_save = OneSave()
                one_save.set('image_url', foot)
                one_save.set('image_src', image)
                one_save.set('image_vol', image_titulo)
                one_save.set('image_spec', image_leyenda)
                one_save.set('image_banner', one_cita)
                one_save.set('image_day', dom)
                one_save.set('image_date', may)
                one_save.save()
            else:
                pass
        else:
            print('network error')


class OneSave(Object):
    @property
    def vol(self):
        return self.get('vol')

    @vol.setter
    def vol(self, value):
        return self.set('vol', value)

    @property
    def image_url(self):
        return self.get('image_url')

    @image_url.setter
    def image_url(self, value):
        return self.set('image_url', value)

    @property
    def image_src(self):
        return self.get('image_src')

    @image_src.setter
    def image_src(self, value):
        return self.set('image_src', value)

    @property
    def image_vol(self):
        return self.get('image_vol')

    @image_vol.setter
    def image_vol(self, value):
        return self.set('image_vol', value)

    @property
    def image_spec(self):
        return self.get('image_spec')

    @image_spec.setter
    def image_spec(self, value):
        return self.set('image_spec', value)

    @property
    def image_banner(self):
        return self.get('image_banner')

    @image_banner.setter
    def image_banner(self, value):
        return self.set('image_banner', value)

    @property
    def image_day(self):
        return self.get('image_day')

    @image_day.setter
    def image_day(self, value):
        return self.set('image_day', value)

    @property
    def image_date(self):
        return self.get('image_date')

    @image_date.setter
    def image_date(self, value):
        return self.set('image_date', value)


def check_vol_exist(vol):
    if vol == '-1':
        return not None
    else:
        OneSave = leancloud.Object.extend('OneSave')
        query = OneSave.query
        try:
            one_info = query.equal_to('image_vol', vol).find()[0]
        except IndexError as e:
            print('IndexError')
            one_info = None
        return one_info


def check_one_exist(url):
    OneSave = leancloud.Object.extend('OneSave')
    query = OneSave.query
    try:
        one_info = query.equal_to('image_url', url).find()[0]
    except IndexError as e:
        print('IndexError')
        one_info = None
    return one_info


def main():
    s = requests.session()
    s.mount(config.base_url, HTTPAdapter(max_retries=5))
    s.keep_alive = False


main()
one = One()
one.start()
