from src.date_manager import get_current_date

import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class S3Manager:
    def __init__(self, config):
        aws_access = config.get('AWS_ACCESS_KEY_ID')
        aws_secret = config.get('AWS_SECRET_ACCESS_KEY')
        bucket = config.get('BUCKET')
        self.folder = config.get('FOLDER')
        
        self.conn = S3Connection(aws_access, aws_secret)
        self.fusion_bucket = self.conn.get_bucket(bucket)

    def get_bucket(self):
        return self.fusion_bucket

    def upload(self, filename, filepath):
        k = Key(self.fusion_bucket)
        k.key = "%s/%s/%s" % (self.folder, get_current_date(), filename)
        k.set_contents_from_filename(filepath, policy='public-read')

        return k.generate_url(expires_in=0, query_auth=False)

    def delete(self, filename):
        k = Key(self.fusion_bucket)
        k.key = filename
        self.fusion_bucket.delete_key(k)
