# tests/test_parser_services.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Basic tests for parser services (python_parser, docker_parser, toml_parser).
# ---------------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tempfile
from app.parser_services.python_parser import extract_python_classes
from app.parser_services.docker_parser import read_dockerfile_content
from app.parser_services.toml_parser import read_toml_content

def test_extract_python_classes():
    """Create a temporary Python file and check if classes are extracted."""
    sample_py = """
class Foo:
    def bar(self):
        pass

class Baz:
    pass
"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        try:
            tmp.write(sample_py.encode("utf-8"))
            tmp_path = tmp.name
        finally:
            tmp.close()

        # Test the parser
        result = extract_python_classes(tmp_path)
        os.unlink(tmp_path)  # cleanup

    assert "Class: Foo" in result
    assert "Class: Baz" in result

def test_read_dockerfile_content():
    """Create a temporary Dockerfile and test reading its content."""
    sample_docker = """FROM python:3.9\nRUN echo 'Hello Docker!'"""
    with tempfile.NamedTemporaryFile(delete=False, prefix="Dockerfile") as tmp:
        try:
            tmp.write(sample_docker.encode("utf-8"))
            tmp_path = tmp.name
        finally:
            tmp.close()

        content = read_dockerfile_content(tmp_path)
        os.unlink(tmp_path)

    assert "FROM python:3.9" in content

def test_read_toml_content():
    """Create a temporary .toml file and test reading its content."""
    sample_toml = """[tool.poetry]\nname="test"\nversion="0.1.0\""""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".toml") as tmp:
        try:
            tmp.write(sample_toml.encode("utf-8"))
            tmp_path = tmp.name
        finally:
            tmp.close()

        content = read_toml_content(tmp_path)
        os.unlink(tmp_path)

    assert "name=\"test\"" in content
