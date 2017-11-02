import leancloud
from leancloud import Object
import requests
from bs4 import BeautifulSoup
from One import config

from requests.adapters import HTTPAdapter

__author__ = 'Vo7ice'


class Question:
    def __init__(self):
        leancloud.init("v87HMWzSFKhBWMlQJMAwV7zz-gzGzoHsz", "010HkHf27pPGD0KfW7oANxQb")
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def start(self, head=config.base_url, foot=config.question_url, vol=-1):
        url = head + foot
        print('url:', url)
        req = requests.get(url, headers=self.headers)
        print('req status_code:', req.status_code)
        if req.status_code == config.SUCCESS:
            soup = BeautifulSoup(req.content, 'html.parser')
            question_title = soup.find('div', class_='one-cuestion').findAll('h4')[0].text.strip()
            print('question_title:', question_title)
            question_content = soup.findAll('div', class_='cuestion-contenido')
            question_title_content = question_content[0].text.strip()
            print('question_title_content:', question_title_content)
            question_paragraph_content = question_content[1].findAll('p')
            question_paragraph = []
            for con in question_paragraph_content:
                question_paragraph.append(con.text)
            content_after = '\n'.join(question_paragraph)
            print('content_after:', content_after)
            # for content in question_content:
            #     print('content:', content)
            question_editor = soup.find('p', class_='cuestion-editor').text.strip()
            print('question_editor:', question_editor)

            question_save = check_question_vol_exist(vol)
            if question_save is None:
                QuestionSave = leancloud.Object.extend('QuestionSave')
                question_save = QuestionSave()
                question_save.set('question_url', foot)
                question_save.set('question_vol', vol)
                question_save.set('question_title', question_title)
                question_save.set('question_title_content', question_title_content)
                question_save.set('question_content', content_after)
                question_save.set('question_editor', question_editor)
                question_save.save()
            else:
                pass
        else:
            print('network error')


class QuestionSave(Object):
    @property
    def question_url(self):
        return self.get('question_url')

    @question_url.setter
    def question_url(self, value):
        return self.set('question_url', value)

    @property
    def question_title(self):
        return self.get('question_title')

    @question_title.setter
    def question_title(self, value):
        return self.set('question_title', value)

    @property
    def question_title_content(self):
        return self.get('question_title_content')

    @question_title_content.setter
    def question_title_content(self, value):
        return self.set('question_title_content', value)

    @property
    def question_content(self):
        return self.get('question_content')

    @question_content.setter
    def question_content(self, value):
        return self.set('question_content', value)

    @property
    def question_editor(self):
        return self.get('question_editor')

    @question_editor.setter
    def question_editor(self, value):
        return self.set('question_editor', value)

    @property
    def question_vol(self):
        return self.get('question_vol')

    @question_vol.setter
    def question_vol(self, value):
        return self.set('question_vol', value)


def check_question_vol_exist(vol):
    if vol == -1:
        return not None
    else:
        QuestionSave = leancloud.Object.extend('QuestionSave')
        query = QuestionSave.query
        try:
            question_info = query.equal_to('question_vol', vol).find()[0]
        except IndexError as e:
            print('IndexError')
            question_info = None
        return question_info


def main():
    s = requests.session()
    s.mount(config.base_url, HTTPAdapter(max_retries=5))
    s.keep_alive = False


main()
question = Question()
question.start()
