import leancloud
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

    def start(self, head=config.base_url, foot=config.question_url):
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
        else:
            print('network error')


def main():
    s = requests.session()
    s.mount(config.base_url, HTTPAdapter(max_retries=5))
    s.keep_alive = False


main()
question = Question()
question.start()
