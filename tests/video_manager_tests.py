from src.video_manager import VideoManager
from tests.test_context import TestContext

import unittest
import os

class VideoManagerTests(TestContext):
    def setUp(self):
        self.videoManager = VideoManager()

    def test_converting_the_video(self):
        test_gif_filepath = "tests/resources/test.gif"

        result = self.videoManager.convert(test_gif_filepath)

        self.assertRegexpMatches(result.mp4, 'test.mp4')
        self.assertRegexpMatches(result.snapshot, 'test.png')

if __name__ == '__main__':
    unittest.main()
