from src.date_manager import get_current_date

import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Manager:
    def __init__(self, config):
        aws_access = config.get('AWS_ACCESS_KEY_ID')
        aws_secret = config.get('AWS_SECRET_ACCESS_KEY')
        self.bucket = config.get('BUCKET')
        self.folder = config.get('FOLDER')
        
        self.conn = S3Connection(aws_access, aws_secret)
        self.fusion_mp4 = self.conn.get_bucket(self.bucket)

    def upload(self, filename, filepath):
        k = Key(self.fusion_mp4)
        k.key = "%s/%s/%s" % (self.folder, get_current_date(), filename)
        k.set_contents_from_filename(filepath, policy='public-read')

        return "https://s3.amazonaws.com/%s/%s/%s/%s" % (self.bucket, self.folder, get_current_date(), filename)

    def delete(self, filename):
        k = Key(self.fusion_mp4)
        k.key = filename
        self.fusion_mp4.delete_key(k)
