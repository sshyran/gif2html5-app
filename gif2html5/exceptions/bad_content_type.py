''' Custom exception because the url is not a gif so it cannot be converted '''

class BadContentType(Exception):

    def __init__(self, message):
        self.message = message
