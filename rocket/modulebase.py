class ModuleBase():
    def __init__(self):
        self.last_message = ''

    def get_message(self, args=None):
        message = self.__get_message__()
        if message != self.last_message:
            self.last_message = message
            return message
        else:
            return None

    def __get_message__(self, args=None):
        pass
