"""
BERTopic Pro - Download Worker
Background worker for downloading models from HuggingFace Hub.
"""

from pathlib import Path
from app.core.workers.base_worker import BaseWorker
from app.core.model_manager import ModelManager


class DownloadWorker(BaseWorker):
    """
    Worker thread for downloading models.

    Downloads embedding models from HuggingFace Hub with progress tracking.
    """

    def __init__(
        self,
        model_name: str,
        model_manager: ModelManager,
        force: bool = False,
    ):
        """
        Initialize download worker.

        Args:
            model_name: HuggingFace model identifier
            model_manager: ModelManager instance
            force: Force re-download even if cached
        """
        super().__init__()

        self.model_name = model_name
        self.model_manager = model_manager
        self.force = force

    def run(self):
        """Download model."""
        try:
            self.emit_status(f"Downloading model: {self.model_name}")
            self.emit_progress(0, "Starting download...")

            def progress_callback(pct, msg):
                if not self._is_cancelled:
                    self.emit_progress(pct, msg)
                    self.emit_status(msg)

            # Download model
            model_path = self.model_manager.download_model(
                model_name=self.model_name,
                progress_callback=progress_callback,
                force=self.force,
            )

            if self._is_cancelled:
                self.emit_status("Download cancelled")
                return

            # Emit result
            result = {
                'model_name': self.model_name,
                'model_path': model_path,
            }

            self.emit_finished(result)

        except Exception as e:
            self.emit_error(e)
