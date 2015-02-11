import os
import server
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		server.app.config['TESTING'] = True
		self.app = server.app.test_client()

	def test_tryout_response(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
