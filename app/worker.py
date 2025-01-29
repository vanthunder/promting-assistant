# app/worker.py
# ---------------------------------------------------------------------
# Author: Marvin Schubert
# © 2025, Marvin Schubert. All rights reserved.
#
# Description:
# A QThread-based worker that handles directory scanning in the background.
# ---------------------------------------------------------------------

import logging
from typing import Optional
from PySide6.QtCore import QThread, Signal
from .file_scanner import FileScanner
from .config import Settings

logger = logging.getLogger(__name__)

class ScanWorker(QThread):
    """
    Performs file scanning in a separate thread.
    Emits signals to update the UI with progress and results.
    """
    progressUpdated = Signal(int)        # Emitted when a single file/directory is processed
    scanningFinished = Signal(str, str)  # Emitted when scanning is complete, with the tree and file content

    def __init__(self, folder_path: str, settings: Settings, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.settings = settings
        self._stop_requested = False

        # Results
        self.tree_str: Optional[str] = None
        self.classes_str: Optional[str] = None

    def run(self):
        """
        Called when thread.start() is invoked. This method does the actual scanning
        in the background.
        """
        logger.info("Background scanning thread started.")
        scanner = FileScanner(self.settings, self.folder_path,
                              progress_callback=self.on_progress_callback)
        tree_str, classes_str = scanner.build_tree()
        self.tree_str = tree_str
        self.classes_str = classes_str

        # Emit the final result
        self.scanningFinished.emit(tree_str, classes_str)
        logger.info("Background scanning thread finished.")

    def on_progress_callback(self, count: int):
        """Updates the progress in the UI thread by emitting a signal."""
        self.progressUpdated.emit(count)

    def stop(self):
        """
        If you want to gracefully stop the thread in a more advanced scenario.
        """
        self._stop_requested = True
        self.quit()
        self.wait()
