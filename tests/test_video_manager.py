import unittest
import urllib.error

from mock import patch

from gif2html5.video_manager import convert
from gif2html5.exceptions.bad_content_type import BadContentType
from tests.test_context import TestContext


class VideoManagerTests(TestContext):

    @patch('gif2html5.video_manager.uuid')
    def test_converting_the_videos(self, mock_uuid):
        mock_uuid.uuid1.return_value = 'test'
        gif_url = 'http://media.giphy.com/media/PTFRmGOgiPUS4/giphy.gif'
        result = convert(gif_url)

        self.assertRegexpMatches(result['mp4'], 'test.mp4')
        self.assertRegexpMatches(result['ogv'], 'test.ogv')
        self.assertRegexpMatches(result['webm'], 'test.webm')
        self.assertRegexpMatches(result['snapshot'], 'test.jpg')

    def test_bad_url_to_convert_video(self):
        gif_url = 'http://www.google.com'
        self.assertRaises(BadContentType, lambda: convert(gif_url))

    def test_invalid_url(self):
        gif_url = 'http://www.goo.c'
        self.assertRaises(urllib.error.URLError, lambda: convert(gif_url))


if __name__ == '__main__':
    unittest.main()
