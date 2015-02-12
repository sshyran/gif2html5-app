import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Manager:
    def __init__(self, aws_access, aws_secret):
        self.conn = S3Connection(aws_access, aws_secret)
        self.fusion_mp4 = self.conn.get_bucket('fusion-gif2html5-mp4')

    def upload(self, filename, filepath):
        k = Key(self.fusion_mp4)
        k.key = filename
        k.set_contents_from_filename(filepath, policy='public-read')

        return "https://s3.amazonaws.com/fusion-gif2html5-mp4/%s" % (filename)

    def delete(self, filename):
        k = Key(self.fusion_mp4)
        k.key = filename
        self.fusion_mp4.delete_key(k)
