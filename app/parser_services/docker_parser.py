# app/parser_services/docker_parser.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Provides functionality to read Dockerfile content.
# ---------------------------------------------------------------------

import logging

logger = logging.getLogger(__name__)

def read_dockerfile_content(file_path: str) -> str:
    """
    Reads the full content of a Dockerfile or one of its variants.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading Dockerfile {file_path}: {e}")
        return f"Error reading {file_path}: {e}"
