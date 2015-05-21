from src.s3_manager import S3Manager
from src.config_parser import get_config

import os
import unittest

class TestContext(unittest.TestCase):

    def tearDown(self):
        self.delete_all_files_in_s3()
        
        folder = './tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path) and the_file != '.gitignore':
                    os.unlink(file_path)
            except Exception, e:
                print e

    def delete_all_files_in_s3(self):
        self.s3Manager = S3Manager(get_config())
        
        bucket = self.s3Manager.get_bucket()
        bucketListResultSet = bucket.list()
        result = bucket.delete_keys([key.name for key in bucketListResultSet])


