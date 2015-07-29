import mimetypes
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from gif2html5.date_manager import get_current_date


class S3Manager:
    def __init__(self, config):
        aws_access = config.get('AWS_ACCESS_KEY_ID')
        aws_secret = config.get('AWS_SECRET_ACCESS_KEY')
        bucket = config.get('BUCKET')
        self.folder = config.get('FOLDER')
        self.cache_header = config.get('CACHE_HEADER')

        self.conn = S3Connection(aws_access, aws_secret)
        self.fusion_bucket = self.conn.get_bucket(bucket)

    def get_bucket(self):
        return self.fusion_bucket

    def upload(self, filename, filepath):
        k = Key(self.fusion_bucket)
        k.key = "%s/%s/%s" % (self.folder, get_current_date(), filename)
        k.set_contents_from_filename(filepath, policy='public-read')

        content_type = mimetypes.guess_type(filename)[0]
        k.set_remote_metadata({'Cache-Control': self.cache_header, 'Content-Type': content_type}, {}, True)

        return k.generate_url(expires_in=0, query_auth=False)

    def delete(self, filename):
        k = Key(self.fusion_bucket)
        k.key = filename
        self.fusion_bucket.delete_key(k)
