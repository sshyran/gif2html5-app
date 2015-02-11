from boto.s3.connection import S3Connection

class S3Manager:
    def init(self):
        conn = S3Connection('<aws access key>', '<aws secret key>')
