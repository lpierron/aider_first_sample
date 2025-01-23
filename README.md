# Flask Arduino Code Generator

This Flask application generates Arduino code (specifically, a simple "Blink" sketch), zips it, and provides it as a downloadable file.

## Functionality

1.  **Web Interface:** A simple HTML page with a button to trigger the code generation.
2.  **Code Generation:** Generates a basic Arduino "Blink" sketch.
3.  **Zipping:** Zips the generated `.ino` file into a `.zip` archive.
4.  **Download:** Provides the zipped Arduino code as a downloadable file.
5.  **Temporary Directory Management:** Creates a temporary directory to store the generated files and cleans it up after the file has been sent to the user.

## Configuration

The application's settings are managed through a `config.py` file. Here's how you can configure it:

*   **`TEMP_DIR`:**  The directory where temporary files (the `.ino` file and the `.zip` archive) are stored.  By default, it's set to `temp` in the same directory as the application.
*   **`ARDUINO_FILE_NAME`:** The name of the Arduino sketch file (default: `blink.ino`).
*   **`ZIP_FILE_NAME`:** The name of the zip archive (default: `blink.zip`).
*   **`LOGGING_LEVEL`:** The logging level for the application.  Can be set to `INFO`, `DEBUG`, `WARNING`, `ERROR`, or `CRITICAL`.

To modify these settings, edit the `config.py` file.  For example:

