#!/usr/bin/env python3
"""Usage:
        madame --url=<url> --channel=<channel> [--user=<user>] [--password=<password>]

Sends a pic of the day from Bonjour Madame to a Rocket Chat channel

Options:
  --url=<url>               Rocket Chat URL
  --channel=<channel>       Rocket Chat channel
  -u --user=<user>          Rocket Chat username (can be set in ~/.netrc)
  -p --password=<password>  Rocket Chat password (can be set in ~/.netrc)
  -h --help                 show this help
"""

import netrc
import sys

import feedparser
from bs4 import BeautifulSoup
from docopt import docopt

from rocket import Rocket


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

    url = arguments['--url']
    channel = arguments['--channel']
    user = arguments['--user']
    password = arguments['--password']

    if not user and not password:
        authenticators = netrc.netrc().authenticators(url)
        user = authenticators[0]
        password = authenticators[2]

    if not user or not password:
        print('Missing user and/or password.\n'
              'Make sure to specify them in command line or in ~/.netrc.',
              file=sys.stderr)
        sys.exit(1)

    rocket = Rocket()
    rocket.url = url + '/api/v1'
    rocket.user = {'username': user,
                   'password': password}

    rocket.auth()
    rocket.alias = 'BonjourBot'

    img = get_img_from_rss()
    rocket.send_message(img['title'], img['url'], channel)
