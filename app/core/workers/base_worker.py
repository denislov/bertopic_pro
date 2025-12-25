"""
BERTopic Pro - Base Worker Class
Abstract base class for all QThread workers in the application.
"""

from typing import Any, Optional
from PySide6.QtCore import QObject, Signal
from app.utils.logger import get_logger


class BaseWorker(QObject):
    """
    Abstract base class for all worker threads.

    Provides standard signals for progress tracking, status updates, and completion.

    Signals:
        progress: Emitted to report progress (0-100)
        status: Emitted to report status messages
        finished: Emitted when work is completed successfully (with result object)
        error: Emitted when an error occurs (with Exception object)
    """

    # Standard signals for all workers
    progress = Signal(int)  # Progress percentage (0-100)
    status = Signal(str)  # Status message
    finished = Signal(object)  # Result object
    error = Signal(Exception)  # Exception object

    def __init__(self):
        """Initialize the base worker."""
        super().__init__()

        # Cancellation flag
        self._is_cancelled = False

        # Logger
        self.logger = get_logger(self.__class__.__name__)

        self.logger.debug(f"{self.__class__.__name__} initialized")

    def run(self):
        """
        Main worker execution method.

        Must be implemented by subclasses. This method will be executed in a separate thread.

        The implementation should:
        1. Check self._is_cancelled periodically
        2. Emit progress signals
        3. Emit status signals
        4. Emit finished signal with result on success
        5. Emit error signal on failure
        """
        raise NotImplementedError("Subclasses must implement run()")

    def cancel(self):
        """
        Request cancellation of the worker.

        Sets the cancellation flag which should be checked in the run() method.
        """
        self._is_cancelled = True
        self.logger.info(f"{self.__class__.__name__} cancellation requested")
        self.status.emit("Cancelling...")

    def is_cancelled(self) -> bool:
        """
        Check if cancellation has been requested.

        Returns:
            True if cancelled, False otherwise
        """
        return self._is_cancelled

    def emit_progress(self, value: int, message: Optional[str] = None):
        """
        Emit progress signal with optional status message.

        Args:
            value: Progress value (0-100)
            message: Optional status message
        """
        # Clamp value to 0-100
        value = max(0, min(100, value))
        self.progress.emit(value)

        if message:
            self.emit_status(message)

    def emit_status(self, message: str):
        """
        Emit status signal.

        Args:
            message: Status message
        """
        self.status.emit(message)
        self.logger.info(message)

    def emit_error(self, exception: Exception):
        """
        Emit error signal.

        Args:
            exception: Exception object
        """
        self.error.emit(exception)
        self.logger.error(f"Error in {self.__class__.__name__}: {str(exception)}", exc_info=True)

    def emit_finished(self, result: Any = None):
        """
        Emit finished signal with result.

        Args:
            result: Result object (can be None)
        """
        if not self._is_cancelled:
            self.finished.emit(result)
            self.logger.info(f"{self.__class__.__name__} completed successfully")
        else:
            self.logger.info(f"{self.__class__.__name__} was cancelled")
