import os, uuid
import unittest

from gif2html5.s3_manager import S3Manager
from gif2html5.config_parser import get_config
from gif2html5.date_manager import get_current_date
from tests.test_context import TestContext


class S3Tests(TestContext):
    def setUp(self):
        self.s3Manager = S3Manager(get_config())

    def test_convert_gif(self):
        filepath = "tests/resources/test.gif"
        random_filename = "%s.mp4" % uuid.uuid1()

        s3_path = self.s3Manager.upload(random_filename, filepath)
        
        expected_filepath = "%s/%s" % (self.get_s3_path(), random_filename)
        self.assertEquals(expected_filepath, s3_path)

if __name__ == '__main__':
    unittest.main()
