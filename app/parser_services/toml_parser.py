# app/parser_services/toml_parser.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Provides functionality to read .toml files.
# ---------------------------------------------------------------------

import logging

logger = logging.getLogger(__name__)

def read_toml_content(file_path: str) -> str:
    """
    Reads the full content of a .toml file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading .toml file {file_path}: {e}")
        return f"Error reading {file_path}: {e}"
