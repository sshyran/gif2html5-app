from src.video_manager import VideoManager
from tests.test_context import TestContext

from mock import MagicMock, patch
import unittest
import os

class VideoManagerTests(TestContext):
    def setUp(self):
        self.videoManager = VideoManager()
    
    def test_converting_the_videos(self):
        test_gif_filepath = "%s/tests/resources/test.gif" % os.getcwd()

        result = self.videoManager.convert(test_gif_filepath)
        self.assertRegexpMatches(result['mp4'], 'test.mp4')
        self.assertRegexpMatches(result['ogv'], 'test.ogv')
        self.assertRegexpMatches(result['webm'], 'test.webm')
        self.assertRegexpMatches(result['snapshot'], 'test.jpg')

if __name__ == '__main__':
    unittest.main()
