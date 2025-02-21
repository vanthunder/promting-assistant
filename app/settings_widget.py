# app/settings_widget.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# A widget that displays user settings, updates the Settings object,
# and emits a signal when the theme changes.
# ---------------------------------------------------------------------

from PySide6.QtCore import Signal, Qt
from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox,
    QGridLayout, QCheckBox, QPushButton
)

class SettingsWidget(QWidget):
    """
    A widget for user settings. Updates the Settings object
    and emits a theme_changed signal when the theme is updated.
    """
    theme_changed = Signal(str)  # Emitted when the theme changes

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Title label
        self.title_label = QLabel("Settings")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(self.title_label)

        # Theme selection
        theme_layout = QHBoxLayout()
        self.theme_label = QLabel("Theme:")
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(["Dark", "Light"])
        self.theme_combobox.setCurrentText(self.settings.window_theme)
        self.theme_combobox.setFixedWidth(100)
        theme_layout.addWidget(self.theme_label)
        theme_layout.addWidget(self.theme_combobox)
        theme_layout.addStretch()
        main_layout.addLayout(theme_layout)

        # Checkboxes
        checkbox_layout = QGridLayout()
        checkbox_layout.setSpacing(5)
        
        self.show_py_content_checkbox = QCheckBox("Show .py Content")
        self.show_py_content_checkbox.setChecked(self.settings.show_py_content)

        self.skip_venv_checkbox = QCheckBox("Skip venv folder")
        self.skip_venv_checkbox.setChecked(self.settings.skip_venv)

        self.show_docker_content_checkbox = QCheckBox("Show Dockerfiles")
        self.show_docker_content_checkbox.setChecked(self.settings.show_docker_content)

        self.show_toml_content_checkbox = QCheckBox("Show .toml files")
        self.show_toml_content_checkbox.setChecked(self.settings.show_toml_content)

        self.skip_git_checkbox = QCheckBox("Skip .git Folders/Files")
        self.skip_git_checkbox.setChecked(self.settings.skip_git)

        self.skip_python_aux_checkbox = QCheckBox("Skip .pyc etc.")  # <--- NEU
        self.skip_python_aux_checkbox.setChecked(self.settings.skip_python_aux)

        checkbox_layout.addWidget(self.show_py_content_checkbox, 0, 0)
        checkbox_layout.addWidget(self.skip_venv_checkbox, 0, 1)
        checkbox_layout.addWidget(self.show_docker_content_checkbox, 1, 0)
        checkbox_layout.addWidget(self.show_toml_content_checkbox, 1, 1)
        checkbox_layout.addWidget(self.skip_git_checkbox, 2, 0)
        checkbox_layout.addWidget(self.skip_python_aux_checkbox, 2, 1)

        main_layout.addLayout(checkbox_layout)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(100)
        main_layout.addWidget(self.save_button, 0, Qt.AlignRight)

        self.setLayout(main_layout)

        # Connect signals
        self.theme_combobox.currentTextChanged.connect(self.on_theme_changed)
        self.show_py_content_checkbox.stateChanged.connect(self.on_show_py_content_toggled)
        self.skip_venv_checkbox.stateChanged.connect(self.on_skip_venv_toggled)
        self.show_docker_content_checkbox.stateChanged.connect(self.on_show_docker_toggled)
        self.show_toml_content_checkbox.stateChanged.connect(self.on_show_toml_toggled)
        self.skip_git_checkbox.stateChanged.connect(self.on_skip_git_toggled)
        self.skip_python_aux_checkbox.stateChanged.connect(self.on_skip_python_aux_toggled)  # <--- NEU
        self.save_button.clicked.connect(self.on_save_clicked)

        # Rahmen um das gesamte Widget (optional)
        self.setStyleSheet("border: 1px solid gray; border-radius: 4px;")

    def on_theme_changed(self, theme_text: str):
        self.settings.window_theme = theme_text
        self.theme_changed.emit(theme_text)

    def on_show_py_content_toggled(self, state: int):
        self.settings.show_py_content = bool(state)

    def on_skip_venv_toggled(self, state: int):
        self.settings.skip_venv = bool(state)

    def on_show_docker_toggled(self, state: int):
        self.settings.show_docker_content = bool(state)

    def on_show_toml_toggled(self, state: int):
        self.settings.show_toml_content = bool(state)

    def on_skip_git_toggled(self, state: int):
        self.settings.skip_git = bool(state)

    def on_skip_python_aux_toggled(self, state: int):  # <--- NEU
        self.settings.skip_python_aux = bool(state)

    def on_save_clicked(self):
        # Placeholder for saving settings to a file, DB, etc.
        print("Settings saved (placeholder).")
        self.settings.skip_git = self.skip_git_checkbox.isChecked()
        self.settings.skip_venv = self.skip_venv_checkbox.isChecked()
        self.settings.show_py_content = self.show_py_content_checkbox.isChecked()
        self.settings.skip_python_aux = self.skip_python_aux_checkbox.isChecked()  # <--- NEU
