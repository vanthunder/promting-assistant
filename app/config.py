# app/config.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Defines the application-wide configuration for scanning and UI.
# ---------------------------------------------------------------------

from typing import Tuple

class Settings:
    """
    Holds application-wide settings. 
    Modify/add fields as needed for your app.
    """
    def __init__(self,
                 window_title: str = "Prompting Assistant",
                 window_size: Tuple[int, int] = (800, 600),
                 window_theme: str = "Dark",
                 skip_venv: bool = True,
                 show_py_content: bool = False,
                 show_docker_content: bool = False,
                 show_toml_content: bool = False):
        self.window_title = window_title
        self.window_size = window_size
        self.window_theme = window_theme
        self.skip_venv = skip_venv
        self.show_py_content = show_py_content
        self.show_docker_content = show_docker_content
        self.show_toml_content = show_toml_content
