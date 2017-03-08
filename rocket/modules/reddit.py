"Gets top picture from specified subreddit (defaults to gentlemanboner)."
import requests as r
from bs4 import BeautifulSoup
from rocket.modulebase import ModuleBase


class Module(ModuleBase):
    def __get_message__(self, args='gentlemanboners'):
        site_url = 'https://www.reddit.com'
        subreddit = args
        page_url = '{0}/r/{1}/top/?sort=top&t=day'.format(site_url, subreddit)
        page = r.get(page_url).text
        soup = BeautifulSoup(page, "html.parser")
        a_tag = soup.findAll("a", { "class" : "outbound" })[1]
        img_title = a_tag.findAll(text=True)
        img_url = a_tag.get('data-href-url')

        return {'title': img_title, 'text': img_url}
