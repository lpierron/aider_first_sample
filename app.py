from flask import Flask, render_template, send_file
import os
import zipfile
import shutil
import logging
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(level=app.config.get('LOGGING_LEVEL'), format='%(asctime)s - %(levelname)s - %(message)s')


def generate_arduino_code():
    """Generates the Arduino code."""
    return """
    // Blink
    // Generated by Flask app

    void setup() {
      pinMode(13, OUTPUT);
    }

    void loop() {
      digitalWrite(13, HIGH);
      delay(1000);
      digitalWrite(13, LOW);
      delay(1000);
    }
    """


def zip_code(code, temp_dir, arduino_file_name, zip_file_name):
    """Zips the Arduino code into a zip file."""
    arduino_file_path = os.path.join(temp_dir, arduino_file_name)
    zip_file_path = os.path.join(temp_dir, zip_file_name)

    try:
        os.makedirs(temp_dir, exist_ok=True)
        with open(arduino_file_path, 'w') as f:
            f.write(code)

        with zipfile.ZipFile(zip_file_path, 'w') as z:
            z.write(arduino_file_path, arcname=arduino_file_name)

        return zip_file_path
    except Exception as e:
        logging.error(f"Error zipping code: {e}")
        return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate_blink')
def generate_blink():
    """Generates the Arduino code, zips it, and sends it as a download."""
    temp_dir = app.config['TEMP_DIR']
    arduino_file_name = app.config['ARDUINO_FILE_NAME']
    zip_file_name = app.config['ZIP_FILE_NAME']

    arduino_code = generate_arduino_code()
    zipped_code = zip_code(arduino_code, temp_dir, arduino_file_name, zip_file_name)

    if not zipped_code:
        return "Failed to generate the zip file.", 500

    try:
        return send_file(zipped_code, as_attachment=True, download_name=zip_file_name)
    finally:
        try:
            shutil.rmtree(temp_dir)
            logging.info(f"Temporary directory '{temp_dir}' removed.")
        except Exception as e:
            logging.error(f"Error removing temporary directory: {e}")


if __name__ == '__main__':
    app.run(debug=True)
