# main.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Main entry point for the "Prompting Assistant" application.
# ---------------------------------------------------------------------

import sys
import logging
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow
from app.config import Settings

def main():
    """
    Launches the PySide6 application.
    Initializes settings, logging, and creates the main window.
    """
    # Configure basic logging.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    app = QApplication(sys.argv)

    # Instantiate the global settings (could also be loaded from a config file).
    settings = Settings(
        window_title="Prompting Assistant",
        window_size=(800, 600),
        window_theme="Dark",
        skip_venv=True,
        show_py_content=False,
        show_docker_content=False,
        show_toml_content=False
    )

    window = MainWindow(settings)
    window.show()

    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()
