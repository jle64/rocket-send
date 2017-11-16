"Gets last picture from Bonjour Madame."
import requests as r
from bs4 import BeautifulSoup
from rocket.modulebase import ModuleBase


class Module(ModuleBase):
    def __get_message__(self, args=None):
        page_url = 'http://dites.bonjourmadame.fr/'
        page = r.get(page_url).text
        soup = BeautifulSoup(page, "html.parser")
        img = soup.find_all('img')[3]
        img_url = img.get('src')
        img_title = img.get('alt')
        return {'title': img_title, 'text': img_url}
