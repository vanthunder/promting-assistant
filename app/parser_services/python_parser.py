# app/parser_services/python_parser.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Extract classes from Python files using the ast library.
# ---------------------------------------------------------------------

import ast
import logging

logger = logging.getLogger(__name__)

def extract_python_classes(file_path: str) -> str:
    """
    Reads a Python file, parses the AST, and returns a string
    listing class definitions found in the file, including the lines of code.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        lines = []
        file_lines = source.splitlines()
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                lines.append(f"Class: {node.name}")
                start = node.lineno - 1
                end = node.end_lineno
                class_body = "\n".join(file_lines[start:end])
                lines.append(class_body)
        return "\n".join(lines)
    except Exception as e:
        logger.error(f"Error reading Python file {file_path}: {e}")
        return f"Error reading {file_path}: {e}"
