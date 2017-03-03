#!/usr/bin/env python3
"""Usage:
        madame --rocket=<rocket-url> --user=<user> --password=<password> --channel=<channel>

Sends a pic of the day from Bonjour Madame to a Rocket Chat channel

Options:
  --rocket=<rocket-url>     Rocket Chat URL
  --channel=<channel>       Rocket Chat channel
  -u --user=<user>          Rocket Chat username
  -p --password=<password>  Rocket Chat password
  -h --help                 show this help
"""

from rocket import Rocket
import feedparser
from bs4 import BeautifulSoup
from docopt import docopt


def get_img_from_rss():
    feed_url = 'http://feeds.feedburner.com/BonjourMadame?format=xml'
    rss = feedparser.parse(feed_url)
    last_post = rss['entries'][0]
    img_title = last_post['title']
    summary = last_post['summary_detail']['value']
    soup = BeautifulSoup(summary, "html.parser")
    img_url = soup.find_all('img')[0].get('src')

    return {'title': img_title, 'url': img_url}


if __name__ == "__main__":
    arguments = docopt(__doc__)

    rocket = Rocket()
    rocket.url = arguments['--rocket'] + '/api/v1'
    rocket.user = {'username': arguments['--user'],
                   'password': arguments['--password']}
    rocket.alias = 'BonjourBot'
    rocket.auth()

    channel = arguments['--channel']

    img = get_img_from_rss()

    rocket.send_message(img['title'], img['url'], channel)
