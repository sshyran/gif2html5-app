from src.s3_manager import S3Manager
import os,binascii
import unittest
import os

class S3Tests(unittest.TestCase):
    def setUp(self):
        aws_access = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.s3Manager = S3Manager(aws_access, aws_secret)
    
    def test_upload_gif(self):
        f = open('resources/test.gif', 'r')
        random_filename = binascii.b2a_hex(os.urandom(15))

        self.s3Manager.upload(random_filename, f.read())

        // check if file is there

        // delete file


if __name__ == '__main__':
    unittest.main()
