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
        expected_filepath = "%s/%s" % (self.get_s3_path(), random_filename)
        self.assertEquals(expected_filepath, s3_path)

if __name__ == '__main__':
    unittest.main()
