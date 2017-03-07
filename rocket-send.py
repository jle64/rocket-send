#!/usr/bin/env python3
"""Usage:    rocket-send message --url=<url> [options] <message>
          rocket-send module --url=<url> [options] <module>
          rocket-send daemonize --url=<url> [options] <modules>
          rocket-send list-channels --url=<url>
          rocket-send list-modules

Send the specified message or a message from a module to a Rocket.Chat channel
or run as a daemon and continuously send module messages

Options:
  -h --help              show this help
  -u --url=<url>         URL in the form:
                         http(s)://user:password@rocket.chat/channel
  -a --alias=<alias>     user alias to use (username will stay visible)

Message mode options:
  -t --title=<title>     message title

Daemon mode options:
  -f --foreground        keep the process in foreground
  -p --pidfile=<pidfile> path to pidfile (defaults to /tmp/rocket-send.pid)
"""

import sys
from glob import glob
from importlib import import_module
from os.path import basename
from urllib.parse import urlparse
from time import sleep

from docopt import docopt
from daemonize import Daemonize

import rocket.modules as modules
from rocket.rocket import Rocket

class RocketSend():
    def __init__(self):
        self.url = None
        self.rocket = Rocket()

    def list_modules(self):
        for file in glob(modules.__path__._path[0] + '/*.py'):
            module_name = basename(file)[:-3]
            module = import_module('rocket.modules.' + module_name)
            print('{0} - {1}'.format(module_name, module.__doc__))

    def list_channels(self):
        print(self.rocket.get_channels())

    def send_message(self):
        message = {}
        message['text'] = arguments['<message>']
        message['title'] = arguments['--title'] or ''
        self.rocket.send_message(message['title'],
                                 message['text'],
                                 self.url.path[1:])

    def call_module(self):
        message = {}
        module_name = arguments['<module>']
        module = import_module('rocket.modules.' + module_name).Module()
        message = module.get_message()
        self.rocket.send_message(message['title'],
                                 message['text'],
                                 self.url.path[1:])

    def setup_rocket(self):
        self.url = urlparse(arguments['--url'])
        self.rocket.url = '{0}://{1}{2}'.format(self.url.scheme,
                                                self.url.hostname,
                                                '/api/v1')
        self.rocket.user = {'username': self.url.username,
                            'password': self.url.password}
        self.rocket.alias = arguments['--alias'] or \
                        '{0}-Bot'.format(self.url.username)
        try:
            self.rocket.auth()
        except:
            print('Authentication failed.', file=sys.stderr)
            sys.exit(1)

    def main(self):
        module_names = arguments['<modules>'].split(',')
        modules = []
        for module_name in module_names:
            module = import_module('rocket.modules.' + module_name).Module()
            modules.append(module)
        while True:
            for module in modules:
                try:
                    message = module.get_message()
                    if message:
                        self.rocket.send_message(message['title'],
                                                 message['text'],
                                                 self.url.path[1:])
                except ConnectionError:
                    pass
            sleep(10)

if __name__ == "__main__":
    arguments = docopt(__doc__)

    rs = RocketSend()

    if arguments['list-modules']:
        rs.list_modules()
    else:
        rs.setup_rocket()
        if arguments['list-channels']:
            rs.list_channels()
        elif arguments['message']:
            rs.send_message()
        elif arguments['module']:
            rs.call_module()
        elif arguments['daemonize']:
            pidfile = arguments['--pidfile'] or '/tmp/rocket-send.pid'
            daemon = Daemonize(app='rocket-send',
                               action=rs.main,
                               pid=pidfile,
                               foreground=arguments['--foreground'])
            daemon.start()
