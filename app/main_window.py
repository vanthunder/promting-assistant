# app/main_window.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Main GUI window for the "Prompting Assistant" application.
# Now includes an expanded cache key to account for .py, Docker, .toml toggles.
# ---------------------------------------------------------------------

import os
import logging

from PySide6.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QProgressBar, QPlainTextEdit,
    QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QApplication
)
from PySide6.QtCore import Slot

from .settings_widget import SettingsWidget
from .worker import ScanWorker
from .config import Settings

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """
    Main GUI window for the Prompting Assistant application.
    """

    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.setWindowTitle(self.settings.window_title)
        self.setMinimumSize(*self.settings.window_size)

        # UI Elements
        self.select_button = QPushButton("Select Path")
        self.path_label = QLabel("/... ")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        self.copy_button = QPushButton("Copy Output")

        # Layout for output
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(self.copy_button)

        # Settings widget
        self.settings_widget = SettingsWidget(self.settings)

        # Central widget layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.select_button)
        layout.addWidget(self.path_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.settings_widget)
        layout.addLayout(output_layout)

        # Connect signals
        self.select_button.clicked.connect(self.open_folder_dialog)
        self.copy_button.clicked.connect(self.copy_output)
        self.settings_widget.theme_changed.connect(self.apply_theme)

        # For caching scan results:
        # Key = (folder_path, skip_venv, show_py_content, show_docker, show_toml)
        self._scan_cache = {}

        # Current folder path
        self.current_folder_path = None

    def open_folder_dialog(self):
        """
        Lets user select a folder. Then starts a background scan if 
        we have not cached the result yet (or if relevant settings changed).
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder_path:
            return

        self.path_label.setText(folder_path)
        self.current_folder_path = folder_path

        # Build an expanded cache key that accounts for all relevant toggles.
        cache_key = (
            folder_path,
            self.settings.skip_venv,
            self.settings.show_py_content,
            self.settings.show_docker_content,
            self.settings.show_toml_content
        )

        if cache_key in self._scan_cache:
            logger.info("Cache hit! Using cached results.")
            tree_str, classes_str = self._scan_cache[cache_key]
            self.show_scan_results(folder_path, tree_str, classes_str)
        else:
            logger.info("Cache miss. Starting background scan.")
            # Clear UI
            self.output_text.clear()
            self.progress_bar.setValue(0)

            # Start background worker
            self.worker = ScanWorker(folder_path, self.settings)
            self.worker.progressUpdated.connect(self.on_progress_updated)
            self.worker.scanningFinished.connect(self.on_scanning_finished)
            self.worker.start()

    @Slot(int)
    def on_progress_updated(self, value: int):
        """
        Updates progress bar from worker signals.
        """
        self.progress_bar.setValue(value)

    @Slot(str, str)
    def on_scanning_finished(self, tree_str: str, classes_str: str):
        """
        Called when the background thread finishes scanning.
        """
        if not self.current_folder_path:
            return

        cache_key = (
            self.current_folder_path,
            self.settings.skip_venv,
            self.settings.show_py_content,
            self.settings.show_docker_content,
            self.settings.show_toml_content
        )

        # Cache the results
        self._scan_cache[cache_key] = (tree_str, classes_str)

        self.show_scan_results(self.current_folder_path, tree_str, classes_str)

    def show_scan_results(self, folder_path: str, tree_str: str, classes_str: str):
        """
        Shows the final results (directory tree + class/file content) in the UI.
        """
        root_name = os.path.basename(folder_path.rstrip(os.sep))
        output_lines = [root_name, tree_str]

        if classes_str.strip():
            output_lines.append("\n----- Python / Additional Contents -----\n" + classes_str)

        final_text = "\n".join(output_lines)
        self.output_text.setPlainText(final_text)
        # Optionally set the progress bar to full
        self.progress_bar.setValue(self.progress_bar.maximum())

    def copy_output(self):
        """
        Copy the displayed text to the system clipboard.
        """
        QApplication.clipboard().setText(self.output_text.toPlainText())

    def apply_theme(self, theme: str):
        """
        Dynamically change the stylesheet of the window to Dark or Light.
        """
        if theme == "Dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2e2e2e;
                    color: #ffffff;
                }
                QLabel, QCheckBox, QPushButton, QComboBox {
                    color: #ffffff;
                }
                QPlainTextEdit {
                    background-color: #3c3c3c;
                    color: #ffffff;
                }
                QProgressBar {
                    text-align: center;
                    color: #ffffff;
                    background-color: #555555;
                }
                QProgressBar::chunk {
                    background-color: #05B8CC;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ffffff;
                    color: #000000;
                }
                QLabel, QCheckBox, QPushButton, QComboBox {
                    color: #000000;
                }
                QPlainTextEdit {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QProgressBar {
                    text-align: center;
                    color: #000000;
                    background-color: #cccccc;
                }
                QProgressBar::chunk {
                    background-color: #05B8CC;
                }
            """)
