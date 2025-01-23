import os

class Config:
    TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')
    ARDUINO_FILE_NAME = 'blink.ino'
    ZIP_FILE_NAME = 'blink.zip'
    LOGGING_LEVEL = 'INFO'  # You can set the logging level here
