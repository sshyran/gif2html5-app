from src.s3_manager import S3Manager
from src.config_parser import get_config
from tests.test_context import TestContext

import os,binascii
import unittest
import os

class S3Tests(TestContext):
    def setUp(self):
        self.s3Manager = S3Manager(get_config())

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
