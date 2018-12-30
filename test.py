from instagram2 import app
import unittest

class FlaskTestCase(unittest.TestCase):

	# ensures that flask was set up correctly 
	def test_index(self):
		tester = app.test_client(self)
		response = tester.get("/", content_type='html/text')
		self.assertEqual(response.status_code, 200)

	# ensures that main page loads correctly - test for actual test 
	def test_main_page_loads(self):
		tester = app.test_client(self)
		response = tester.get("/", content_type='html/text')
		self.assertTrue(b'Instagram 2.0' in response.data)

if __name__ == '__main__':
	unittest.main()