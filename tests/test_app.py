import unittest
import os
import tempfile
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, zip_code, generate_arduino_code
from config import Config

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config()
        self.config.TEMP_DIR = self.temp_dir

    def tearDown(self):
        os.rmdir(self.temp_dir)

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Flask App', response.data)

    def test_generate_blink_route(self):
        response = self.app.get('/generate_blink')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/zip')
        self.assertEqual(response.headers['Content-Disposition'], 'attachment; filename=blink.zip')

    def test_generate_arduino_code(self):
        code = generate_arduino_code()
        self.assertIn("void setup()", code)
        self.assertIn("void loop()", code)

    def test_zip_code(self):
        code = generate_arduino_code()
        zip_file_path = zip_code(code, self.config.TEMP_DIR, self.config.ARDUINO_FILE_NAME, self.config.ZIP_FILE_NAME)
        self.assertTrue(os.path.exists(zip_file_path))
        self.assertTrue(zip_file_path.endswith(".zip"))
        os.remove(zip_file_path)


if __name__ == '__main__':
    unittest.main()
