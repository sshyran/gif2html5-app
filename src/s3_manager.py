import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Manager:
    def __init__(self, aws_access, aws_secret):
        self.conn = S3Connection(aws_access, aws_secret)

    def upload(self, filename, filepath):
        fusion_mp4 = self.conn.get_bucket('fusion-gif2html5-mp4')

        k = Key(fusion_mp4)
        k.key = filename
        k.set_contents_from_filename(filepath, policy='public-read')
