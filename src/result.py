class Result(object):
    mp4 = ""
    snapshot = ""

    def __init__(self, mp4, ogv, webm, snapshot):
        self.mp4 = mp4
        self.ogv = ogv
        self.webm = webm
        self.snapshot = snapshot
