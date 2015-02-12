from src.s3_manager import S3Manager
from src.config_parser import get_config
import os,binascii
import unittest
import os

class S3Tests(unittest.TestCase):
    def setUp(self):
        config = get_config()
        aws_access = config.get("AWS_ACCESS_KEY_ID")
        aws_secret = config.get("AWS_SECRET_ACCESS_KEY")
        self.s3Manager = S3Manager(aws_access, aws_secret)

    def test_convert_gif(self):
        filepath = "tests/resources/test.gif"
        f = open(filepath, 'r')
        random_filename = binascii.b2a_hex(os.urandom(15))

        s3_path = self.s3Manager.upload(random_filename, filepath)
        expected_filepath = "https://s3.amazonaws.com/fusion-gif2html5-mp4/%s" % (random_filename)
        self.assertEquals(expected_filepath, s3_path)

        self.s3Manager.delete(random_filename)


if __name__ == '__main__':
    unittest.main()
