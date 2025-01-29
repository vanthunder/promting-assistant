# tests/test_app.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Basic test for the main app window initialization.
# ---------------------------------------------------------------------

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow
from app.config import Settings

@pytest.fixture
def app_fixture():
    """Creates a QApplication instance for testing."""
    return QApplication([])

def test_main_window_init(app_fixture):
    """Tests that the MainWindow can be created without error."""
    settings = Settings()
    window = MainWindow(settings)
    assert window is not None
    assert window.windowTitle() == settings.window_title
