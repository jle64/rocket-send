"Gets last picture from Bonjour Madame."
import feedparser
from bs4 import BeautifulSoup
from rocket.modulebase import ModuleBase


class Module(ModuleBase):
    def __get_message__(self):
        feed_url = 'http://feeds.feedburner.com/BonjourMadame?format=xml'
        rss = feedparser.parse(feed_url)
        last_post = rss['entries'][0]
        img_title = last_post['title']
        summary = last_post['summary_detail']['value']
        soup = BeautifulSoup(summary, "html.parser")
        img_url = soup.find_all('img')[0].get('src')

        return {'title': img_title, 'text': img_url}
