''' Custom exception because the url is not a gif so it cannot be converted '''

class BadContentType(Exception): 
    pass
