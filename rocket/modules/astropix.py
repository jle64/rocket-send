"Gets astronomy picture of the day from NASA."
import requests as r
from bs4 import BeautifulSoup
from rocket.modulebase import ModuleBase


class Module(ModuleBase):
    def __get_message__(self):
        site_url = 'https://apod.nasa.gov/apod/'
        page_url = site_url + 'astropix.html'
        page = r.get(page_url).text
        soup = BeautifulSoup(page, "html.parser")
        # text between the first <b></b> tags should be the title
        img_title = soup.find_all('b')[0].contents[0]
        # src attribute of first <img> tag should be a relative path
        img_path = soup.find_all('img')[0].get('src')
        img_url = site_url + img_path

        return {'title': img_title, 'text': img_url}
