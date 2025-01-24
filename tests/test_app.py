import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from app import app, zip_code
from config import Config


class TestApp(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.temp_dir = tempfile.mkdtemp()
        self.arduino_file_name = "test_arduino_code.ino"
        self.zip_file_name = "test_arduino_code.zip"
        self.arduino_file_path = os.path.join(self.temp_dir, self.arduino_file_name)
        self.zip_file_path = os.path.join(self.temp_dir, self.zip_file_name)

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            os.rmdir(self.temp_dir)


    def test_generate_arduino_code(self):
        with app.test_client() as client:
            response = client.post("/", data={"prompt": "test prompt"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Arduino Code:", response.data)

    def test_zip_code(self):
        test_code = "void setup() { }"
        with open(self.arduino_file_path, "w") as f:
            f.write(test_code)
        zip_code(test_code, self.temp_dir, self.arduino_file_name, self.zip_file_name)
        self.assertTrue(os.path.exists(self.zip_file_path))

    @patch("app.openai.chat.completions.create")
    def test_generate_code_from_prompt(self, mock_openai):
        mock_openai.return_value.choices = [
            type("choice", (object,), {"message": type("message", (object,), {"content": "test code"})})()
        ]
        with app.test_client() as client:
            response = client.post("/", data={"prompt": "test prompt"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"test code", response.data)
