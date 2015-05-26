from src.video_manager import VideoManager
from tests.test_context import TestContext
from lib.gfycat.gfycat import gfycat

from mock import MagicMock
import urllib
import unittest
import os

class VideoManagerTests(TestContext):
    def setUp(self):
        self.videoManager = VideoManager()
        
    def test_converting_the_videos(self):
        urllib.URLopener = MagicMock()
        urllib.URLopener.retrieve = MagicMock()
        
        gcat = gfycat()
        gcat.uploadFile = MagicMock(return_value={'webm' : 'file.webm', 'mp4': 'file.mp4'})
        
        test_gif_filepath = "%s/tests/resources/test.gif" % os.getcwd()

        result = self.videoManager.convert(test_gif_filepath, gcat)

        self.assertRegexpMatches(result['mp4'], 'test.mp4')
        self.assertRegexpMatches(result['ogv'], 'test.ogv')
        self.assertRegexpMatches(result['webm'], 'test.webm')
        self.assertRegexpMatches(result['snapshot'], 'test.png')

if __name__ == '__main__':
    unittest.main()
