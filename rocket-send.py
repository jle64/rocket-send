#!/usr/bin/env python3
"""Usage:
        rocket-send message --url=<url> [options] <message>
        rocket-send module --url=<url> [options] <module>
        rocket-send list-channels --url=<url>
        rocket-send list-modules

Sends the specified message or a message from a module to a Rocket.Chat channel

Options:
  -u --url=<url>           URL in the form:
                           http(s)://user:password@rocket.chat/channel
  -a --alias=<alias>       user alias to use (username will stay visible)
  -t --title=<title>       message title (only when not using a module)
  -h --help                show this help
"""

import sys
from glob import glob
from importlib import import_module
from os.path import basename
from urllib.parse import urlparse

from docopt import docopt

import rocket.modules as modules
from rocket.rocket import Rocket

if __name__ == "__main__":
    arguments = docopt(__doc__)

    if arguments['list-modules']:
        for file in glob(modules.__path__._path[0] + '/*.py'):
            module_name = basename(file)[:-3]
            module = import_module('rocket.modules.' + module_name)
            print('{0} - {1}'.format(module_name, module.__doc__))
    else:
        rocket = Rocket()
        url = urlparse(arguments['--url'])
        rocket.url = '{0}://{1}{2}'.format(url.scheme,
                                           url.hostname,
                                           '/api/v1')
        rocket.user = {'username': url.username,
                       'password': url.password}
        rocket.alias = arguments['--alias'] or \
                       '{0}-Bot'.format(url.username)
        rocket.auth()
        message = {}
        if arguments['list-channels']:
            print(rocket.get_channels())
        elif arguments['message']:
            message['text'] = arguments['<message>']
            message['title'] = arguments['--title'] or ''
            rocket.send_message(message['title'],
                                message['text'],
                                url.path[1:])
        elif arguments['module']:
            module = import_module('rocket.modules.' + arguments['<module>'])
            message = module.get_message()
            rocket.send_message(message['title'],
                                message['text'],
                                url.path[1:])