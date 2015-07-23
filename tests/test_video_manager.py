import unittest
import os

from mock import MagicMock, patch
from unittest.mock import patch

from gif2html5.video_manager import VideoManager
from tests.test_context import TestContext


class VideoManagerTests(TestContext):
    def setUp(self):
        self.video_manager = VideoManager()
   
    @patch('gif2html5.video_manager.uuid')
    def test_converting_the_videos(self, mock_uuid):
        mock_uuid.uuid1.return_value = 'test'
        gif_url = 'http://media.giphy.com/media/PTFRmGOgiPUS4/giphy.gif'
        result = self.video_manager.convert(gif_url)
        
        self.assertRegexpMatches(result['mp4'], 'test.mp4')
        self.assertRegexpMatches(result['ogv'], 'test.ogv')
        self.assertRegexpMatches(result['webm'], 'test.webm')
        self.assertRegexpMatches(result['snapshot'], 'test.jpg')

    def test_bad_url_to_convert_video(self):
        gif_url = 'http://www.google.com'
        self.assertRaises(Exception, lambda: self.video_manager.convert(gif_url))


        

if __name__ == '__main__':
    unittest.main()
