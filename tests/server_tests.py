import os
import server
import unittest
import tempfile
from flask import json, jsonify
from src.config_parser import get_config
from src.s3_manager import S3Manager

class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		server.app.config['TESTING'] = True
		self.app = server.app.test_client()

	def test_getting_mp4(self):
		response = self.app.get('/convert?url=http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif')
		self.assertEqual(response.status_code, 200)

		data = json.loads(response.data)
		self.assertRegexpMatches(data['mp4'], 'https://s3.amazonaws.com/fusion-gif2html5-mp4')

		file_to_delete = data['mp4'].split('/')[-1]

		config = get_config()
		aws_access = config.get("AWS_ACCESS_KEY_ID")
		aws_secret = config.get("AWS_SECRET_ACCESS_KEY")
		s3Manager = S3Manager(aws_access, aws_secret)
		s3Manager.delete(file_to_delete)



if __name__ == '__main__':
    unittest.main()
