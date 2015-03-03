import os
import unittest

class TestContext(unittest.TestCase):

    def tearDown(self):
        folder = './tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path) and the_file != '.gitignore':
                    os.unlink(file_path)
            except Exception, e:
                print e
