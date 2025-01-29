# Prompting Assistant

**Author**: Marvin Schubert  
**License**: MIT or another license of your choice (update as needed).  

## Description

The Prompting Assistant is a PySide6-based GUI tool for:

- Scanning a selected folder and building an ASCII tree of its contents.
- Optionally skipping well-known virtual environment folders (`venv`, `.venv`, etc.).
- Optionally extracting class definitions from `.py` files.
- Optionally extracting full content from Dockerfiles or `.toml` files.
- Displaying all results in the GUI, including progress updates, and allowing the user to copy the output.

## Key Features

1. **Non-blocking Scanning**:  
   Uses a background worker (`ScanWorker` via `QThread`) so large folder scans won’t freeze the UI.
2. **Configurable Settings**:  
   Users can toggle `.py` content, Dockerfiles, `.toml` display, and skip venv folders.
3. **Caching**:  
   If the same folder is re-scanned with the same relevant settings, results are loaded from cache, saving time.
4. **Theme Support**:  
   A simple “Dark” or “Light” theme can be applied.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/prompting-assistant.git
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```
3. Install dependencies (using Poetry or pip):
   - **Using Poetry**:
     ```bash
     poetry install
     ```
   - **Using pip** (if you’re not using `pyproject.toml`):
     ```bash
     pip install PySide6
     ```

## Usage

- Run the application:
  ```bash
  python main.py
  ```
- Click **“Select Path”** and choose a folder to scan.
- Adjust **Settings** (e.g., Show .py Content, Skip venv) before or after scanning.
- The results appear in the main text area, and you can copy them to the clipboard.

## Testing

- To run tests with **pytest**:
  ```bash
  pytest tests/
  ```

## Notes / Future Improvements

1. **Partial File Reading** for very large files (currently we read them fully).
2. **More Parsers**: You can easily add additional parser services (e.g., for `.yaml`, `.json`).
3. **Robust Logging**: Already partially implemented, but can be expanded (logging to file, etc.).
4. **Advanced Error Handling**: E.g., show user-friendly dialogs for permission errors.

---

© 2025, Marvin Schubert. All rights reserved.  
Feel free to adapt the license and usage instructions as needed.
