import requests as r

class Rocket():
    "Rocket API doc: https://rocket.chat/docs/developer-guides/rest-api/"
    def __init__(self):
        self.url = ''
        self.user = {}
        self.headers = {}
        self.alias = 'BonjourBOT'

    def auth(self):
        authdata = r.post(self.url + "/login", data=self.user).json()['data']
        self.headers = {'X-Auth-Token': authdata['authToken'],
                        'X-User-Id': authdata['userId']}

    def get_channels(self):
        return r.get(self.url + "/channels.list", headers=headers)

    def send_message(self, message_title, message_text, channel, attachments=None):
        # attachment example:
        # [{'title':'My title',
        #   'text':'My text',
        #   'collapsed': 'false'}]
        message = {'channel': channel,
                   'title': message_title,
                   'text': message_text,
                   'alias': self.alias,
                   'attachments': attachments}
        return r.post(self.url + "/chat.postMessage",
                      headers=self.headers,
                      data=message)