import requests as r

class Rocket():
    "Rocket API doc: https://rocket.chat/docs/developer-guides/rest-api/"
    def __init__(self):
        self.url = ''
        self.user = {}
        self.headers = {}
        self.alias = ''

    def auth(self):
        authdata = r.post(self.url + "/login", data=self.user).json()['data']
        self.headers = {'X-Auth-Token': authdata['authToken'],
                        'X-User-Id': authdata['userId']}

    def get_channels(self):
        channels = r.get(self.url + "/channels.list", headers=self.headers)
        channel_names = []
        for channel in channels.json()['channels']:
            channel_names.append(channel['name'])
        return channel_names

    def send_message(self, message_title, message_text, channel):
        message = {'channel': channel,
                   'title': message_title,
                   'text': message_text,
                   'alias': self.alias}
        return r.post(self.url + "/chat.postMessage",
                      headers=self.headers,
                      data=message)
