import os
import server
import unittest
import tempfile
from flask import json, jsonify

class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		server.app.config['TESTING'] = True
		self.app = server.app.test_client()

	def test_tryout_response(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)

	# def test_getting_mp4(self):
	# 	response = self.app.get('/convert?url=http://www.example.com/test.gif')
	# 	self.assertEqual(response.status_code, 200)
	#
	# 	data = json.loads(response.data)
	# 	self.assert_equal(data['url'], 'http://www.example.com/test.mp4')


if __name__ == '__main__':
    unittest.main()
