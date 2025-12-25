"""
BERTopic Pro - Base Tab Class
Abstract base class for all tab widgets in the application.
"""

from typing import Optional
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from app.utils.logger import get_logger


class BaseTab(QWidget):
    """
    Abstract base class for all tabs in the main window.

    Provides common functionality and signals for inter-tab communication.

    Signals:
        data_loaded: Emitted when data is successfully loaded (with data object)
        model_trained: Emitted when a model is successfully trained (with model object)
        error_occurred: Emitted when an error occurs (with error message)
        status_changed: Emitted when tab status changes (with status message)
        tab_enabled: Emitted to enable/disable this tab (bool)
    """

    # Common signals for all tabs
    data_loaded = Signal(object)  # Emits loaded data (DataFrame, etc.)
    model_trained = Signal(object)  # Emits trained model
    error_occurred = Signal(str)  # Emits error message
    status_changed = Signal(str)  # Emits status update
    tab_enabled = Signal(bool)  # Requests to enable/disable tab

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the base tab.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Set up logger for this tab
        self.logger = get_logger(self.__class__.__name__)

        # Initialize UI
        self.setup_ui()

        # Connect signals
        self.connect_signals()

        # Initial state
        self.is_enabled = True

        self.logger.debug(f"{self.__class__.__name__} initialized")

    def setup_ui(self):
        """
        Set up the user interface for this tab.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement setup_ui()")

    def connect_signals(self):
        """
        Connect signals and slots.

        Can be overridden by subclasses to add custom connections.
        """
        # Connect error signal to logger
        self.error_occurred.connect(self.on_error)

        # Connect status signal to logger
        self.status_changed.connect(self.on_status_change)

    def on_error(self, error_message: str):
        """
        Handle error occurrences.

        Args:
            error_message: Error message to log
        """
        self.logger.error(error_message)

    def on_status_change(self, status_message: str):
        """
        Handle status changes.

        Args:
            status_message: Status message to log
        """
        self.logger.info(status_message)

    def enable_tab(self):
        """Enable this tab for user interaction."""
        self.setEnabled(True)
        self.is_enabled = True
        self.logger.debug(f"{self.__class__.__name__} enabled")

    def disable_tab(self):
        """Disable this tab from user interaction."""
        self.setEnabled(False)
        self.is_enabled = False
        self.logger.debug(f"{self.__class__.__name__} disabled")

    def reset_tab(self):
        """
        Reset the tab to its initial state.

        Can be overridden by subclasses to implement custom reset logic.
        """
        self.logger.info(f"{self.__class__.__name__} reset")

    def cleanup(self):
        """
        Clean up resources when tab is closed or application exits.

        Can be overridden by subclasses to implement custom cleanup logic.
        """
        self.logger.debug(f"{self.__class__.__name__} cleanup")
