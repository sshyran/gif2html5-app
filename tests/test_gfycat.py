import unittest

from gif2html5.gfycat import convert_gif


class GfycatTests(unittest.TestCase):

    def setUp(self):
        self.test_gif = 'http://media.giphy.com/media/PTFRmGOgiPUS4/giphy.gif'
        self.big_gif = 'http://img.pandawhale.com/post-58020-Big-Hero-6-Baymax-hug-there-th-NwXV.gif'

    def test_convert_gif(self):
        response = convert_gif(self.test_gif)

        expected_mp4 = 'http://zippy.gfycat.com/GreatAgitatedCaimanlizard.mp4'
        expected_webm = 'http://zippy.gfycat.com/GreatAgitatedCaimanlizard.webm'
        self.assertEquals(expected_mp4, response['mp4'])
        self.assertEquals(expected_webm, response['webm'])

    def test_convert_bad_url(self):
        response = convert_gif('non gif')
        self.assertEquals(None, response)

    def test_large_gif(self):
        response = convert_gif(self.big_gif)

        expected_mp4 = 'http://zippy.gfycat.com/InfamousVillainousDore.mp4'
        expected_webm = 'http://zippy.gfycat.com/InfamousVillainousDore.webm'
        self.assertEquals(expected_mp4, response['mp4'])
        self.assertEquals(expected_webm, response['webm'])
