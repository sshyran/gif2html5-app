import os
import server
import unittest
import tempfile
import urllib
from flask import json, jsonify
from src.config_parser import get_config
from src.s3_manager import S3Manager
from tests.test_context import TestContext
from mock import MagicMock, ANY
import requests
from gfycat.gfycat import gfycat


class JsonPayloadAttachmentIdMatcher(object):
	def __init__(self, o):
		self.o = o

	def __eq__(self, o):
		return o['attachment_id'] == '123'


class FlaskTestCase(TestContext):

	def setUp(self):
		server.app.config['TESTING'] = True
		server.app.config['API_KEY'] = '123456'
		self.app = server.app.test_client()

	def test_authentication(self):
		payload = {
			'url': 'http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif',
		}
		response = self.app.post('/convert', data = json.dumps(payload), follow_redirects = True)
		self.assertEqual(response.status_code, 401)

	def test_getting_mp4(self):
		payload = {
			'url': 'http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif',
			'api_key': '123456',
		}
                
                response = self.app.post('/convert', data = json.dumps(payload), follow_redirects = True)
                
                self.assertEqual(response.status_code, 200)
                
                data = json.loads(response.data)
                self.assertRegexpMatches(data['mp4'], '\.mp4')
                self.assertRegexpMatches(data['ogv'], '\.ogv')
                self.assertRegexpMatches(data['webm'], '\.webm')
                self.assertRegexpMatches(data['snapshot'], '\.png')

		file_to_delete = data['mp4'].split('/')[-1]

		s3Manager = S3Manager(get_config())
		s3Manager.delete(file_to_delete)

	def test_malformed_json_request(self):
		payload = '{"url":"http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif" "webhook":"http://google.com" }'

		response = self.app.post('/convert', data = payload, follow_redirects = True)

		self.assertEqual(response.status_code, 406)

	def test_getting_mp4_without_payload(self):
		response = self.app.post('/convert', follow_redirects = True)

		self.assertEqual(response.status_code, 406)

	def test_webhook(self):
		server.convert_video.delay = MagicMock()
		payload = {
			'api_key': '123456',
			'url': 'http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif',
			'webhook' : 'http://www.google.com',
		}

		response = self.app.post('/convert', data = json.dumps(payload), follow_redirects = True)

		self.assertEqual(response.status_code, 200)
		server.convert_video.delay.assert_called_with(ANY, 'http://www.google.com')

	def test_video_converter_task(self):
		requests.post = MagicMock()
                gcat = gfycat()
                gcat.uploadFile = MagicMock(return_value= {'webmUrl':'file.webm', 'mp4Url':'file.mp4'})
                
                urllib.URLopener = MagicMock()
                urllib.URLopener.retrieve = MagicMock()
                
                server.upload_resources = MagicMock(return_value = {})
		server.convert_video.apply(args=('http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif', 'http://www.google.com?attachment_id=123', gcat)).get()

		payload = {'attachment_id' : '123'}

		requests.post.assert_called_with('http://www.google.com?attachment_id=123', data=JsonPayloadAttachmentIdMatcher(payload))


	def test_video_converter_task_without_attachment_id(self):
		requests.post = MagicMock()

		server.convert_video.apply(args=('http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif', 'http://www.google.com')).get()

		requests.post.assert_called_with('http://www.google.com', data={'message' : 'It looks like you are missing attachment_id'})

if __name__ == '__main__':
    unittest.main()
