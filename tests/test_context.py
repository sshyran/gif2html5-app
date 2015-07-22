from gif2html5.s3_manager import S3Manager
from gif2html5.config_parser import get_config
from gif2html5.date_manager import get_current_date

import os
import unittest
import tempfile

class TestContext(unittest.TestCase):

    def tearDown(self):
        self.delete_all_files_in_s3()
        
        folder = tempfile.gettempdir()
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path) and the_file != '.gitignore':
                    os.unlink(file_path)
            except(Exception, e):
                print(e)

    def delete_all_files_in_s3(self):
        s3Manager = S3Manager(get_config())
        
        bucket = s3Manager.get_bucket()
        bucketListResultSet = bucket.list()
        result = bucket.delete_keys([key.name for key in bucketListResultSet])

    def get_s3_path(self):
        config = get_config()
        
        return "https://%s.s3.amazonaws.com/%s/%s" % (config.get('BUCKET'), config.get('FOLDER'), get_current_date())


