# app/file_scanner.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# Encapsulates logic for walking directories, building an ASCII tree,
# and optionally parsing specialized files (.py, Docker, .toml).
# ---------------------------------------------------------------------

import os
import logging
from typing import Callable, Tuple
from .parser_services.python_parser import extract_python_classes
from .parser_services.docker_parser import read_dockerfile_content
from .parser_services.toml_parser import read_toml_content
from .config import Settings

logger = logging.getLogger(__name__)

class FileScanner:
    """
    Responsible for:
      - Counting all entries (files + folders)
      - Building an ASCII tree of the directory structure
      - Gathering specialized file contents based on user settings
    """

    def __init__(self,
                 settings: Settings,
                 root_folder: str,
                 progress_callback: Callable[[int], None] = None):
        """
        :param settings: Settings object containing user preferences.
        :param root_folder: The folder to be scanned.
        :param progress_callback: Optional function to call upon processing each item (for UI updates).
        """
        self.settings = settings
        self.root_folder = root_folder
        self.progress_callback = progress_callback

        # Known virtual environment folder names
        self.venv_names = {"venv", ".venv", "env", ".env"}

        # Pre-calculate total entries for progress bar
        self.total_entries = self.count_entries()
        self.processed_count = 0

    def count_entries(self) -> int:
        """
        Counts all files/folders under root_folder,
        skipping venv folders if skip_venv is True.
        """
        total_count = 0
        for root, dirs, files in os.walk(self.root_folder):
            if self.settings.skip_venv:
                dirs[:] = [d for d in dirs if d.lower() not in self.venv_names]
            total_count += len(dirs) + len(files)
        return total_count

    def build_tree(self, path: str = "", prefix: str = "") -> Tuple[str, str]:
        """
        Recursively builds an ASCII tree of the directory structure
        and collects relevant file contents (Python classes, Docker, .toml).
        
        :param path: Current directory to scan. Defaults to root_folder if empty.
        :param prefix: Current prefix for the ASCII tree lines.
        :return: A tuple (tree_string, combined_file_contents).
        """
        if not path:
            path = self.root_folder

        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            logger.warning(f"Permission denied when accessing: {path}")
            return f"[Access Denied]: {path}\n", ""

        tree_lines = []
        file_contents = []

        for i, entry in enumerate(entries):
            full_path = os.path.join(path, entry)
            connector = "├── " if i < len(entries) - 1 else "└── "

            # Update progress
            self.processed_count += 1
            if self.progress_callback:
                self.progress_callback(self.processed_count)

            # Skip venv folders if requested
            if (
                self.settings.skip_venv and
                os.path.isdir(full_path) and
                entry.lower() in self.venv_names
            ):
                tree_lines.append(f"{prefix}{connector}{entry} [venv skipped]")
                continue

            tree_lines.append(f"{prefix}{connector}{entry}")

            # If it's a directory, recurse
            if os.path.isdir(full_path):
                sub_prefix = f"{prefix}│   " if i < len(entries) - 1 else f"{prefix}    "
                sub_tree, sub_content = self.build_tree(full_path, sub_prefix)
                if sub_tree:
                    tree_lines.append(sub_tree)
                if sub_content:
                    file_contents.append(sub_content)
            else:
                # If it's a file, possibly parse content
                lower_entry = entry.lower()
                # Python
                if lower_entry.endswith(".py") and self.settings.show_py_content:
                    py_classes = extract_python_classes(full_path)
                    if py_classes.strip():
                        file_contents.append(f"File: {full_path}\n{py_classes}\n------")

                # Docker
                if self.settings.show_docker_content and self._is_dockerfile(lower_entry):
                    content = read_dockerfile_content(full_path)
                    if content.strip():
                        file_contents.append(f"File: {full_path}\n{content}\n------")

                # TOML
                if self.settings.show_toml_content and lower_entry.endswith(".toml"):
                    content = read_toml_content(full_path)
                    if content.strip():
                        file_contents.append(f"File: {full_path}\n{content}\n------")

        return "\n".join(tree_lines), "\n".join(file_contents)

    def _is_dockerfile(self, filename: str) -> bool:
        """
        Checks if the file is a Dockerfile variant.
        """
        dockerfile_variants = {"dockerfile", "dockerfile.dev", "dockerfile.prod", "dockerfile.test"}
        if filename in dockerfile_variants or filename.startswith("dockerfile."):
            return True
        return False
