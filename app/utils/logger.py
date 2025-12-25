"""
BERTopic Pro - Logging System
Custom Qt-integrated logging handler that displays logs in the UI console.
"""

import logging
from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QTextCursor, QColor, QTextCharFormat

import config


class QTextEditLogger(QObject, logging.Handler):
    """
    Custom logging handler that emits Qt signals for thread-safe logging to a QPlainTextEdit widget.

    This handler can be used from any thread and will safely update the UI in the main thread.
    """

    # Signal emitted when a new log message arrives (thread-safe)
    log_signal = Signal(str, str)  # (formatted_message, level_name)

    def __init__(self, text_edit: Optional[QPlainTextEdit] = None):
        """
        Initialize the logger.

        Args:
            text_edit: QPlainTextEdit widget to display logs (can be set later)
        """
        QObject.__init__(self)
        logging.Handler.__init__(self)

        self.text_edit = text_edit

        # Connect signal to slot if text_edit is provided
        if self.text_edit:
            self.log_signal.connect(self.append_log)

        # Set up formatter
        formatter = logging.Formatter(
            config.LOG_FORMAT,
            datefmt=config.LOG_DATE_FORMAT
        )
        self.setFormatter(formatter)

    def set_text_edit(self, text_edit: QPlainTextEdit):
        """
        Set or update the text edit widget.

        Args:
            text_edit: QPlainTextEdit widget to display logs
        """
        self.text_edit = text_edit
        self.log_signal.connect(self.append_log)

    def emit(self, record: logging.LogRecord):
        """
        Called from any thread when a log message is emitted.

        Args:
            record: The log record to emit
        """
        try:
            msg = self.format(record)
            level_name = record.levelname
            # Emit signal (thread-safe) instead of directly modifying UI
            self.log_signal.emit(msg, level_name)
        except Exception:
            self.handleError(record)

    @Slot(str, str)
    def append_log(self, message: str, level_name: str):
        """
        Append log message to the text edit widget (called in main thread only).

        Args:
            message: Formatted log message
            level_name: Log level name (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        if not self.text_edit:
            return

        # Set color based on log level
        color_map = {
            "DEBUG": QColor("#9e9e9e"),      # Gray
            "INFO": QColor("#ffffff"),       # White
            "WARNING": QColor("#ffa726"),    # Orange
            "ERROR": QColor("#ef5350"),      # Red
            "CRITICAL": QColor("#d32f2f"),   # Dark Red
        }

        color = color_map.get(level_name, QColor("#ffffff"))

        # Create text format with color
        text_format = QTextCharFormat()
        text_format.setForeground(color)

        # Move cursor to end
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)

        # Insert colored text
        cursor.insertText(message + "\n", text_format)

        # Auto-scroll to bottom
        self.text_edit.moveCursor(QTextCursor.End)

        # Limit maximum lines to prevent memory issues
        max_lines = config.CONSOLE_LOG_MAX_LINES
        if self.text_edit.blockCount() > max_lines:
            # Remove old lines from top
            cursor = self.text_edit.textCursor()
            cursor.movePosition(QTextCursor.Start)
            for _ in range(self.text_edit.blockCount() - max_lines):
                cursor.select(QTextCursor.BlockUnderCursor)
                cursor.removeSelectedText()
                cursor.deleteChar()  # Remove the newline


def setup_logging(text_edit: Optional[QPlainTextEdit] = None) -> QTextEditLogger:
    """
    Set up application-wide logging with file and optional Qt UI handlers.

    Args:
        text_edit: Optional QPlainTextEdit widget for UI logging

    Returns:
        QTextEditLogger instance for UI integration
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Clear any existing handlers
    root_logger.handlers.clear()

    # File handler (always enabled)
    file_handler = logging.handlers.RotatingFileHandler(
        config.LOG_FILE_PATH,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # Console handler (for terminal output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    console_formatter = logging.Formatter(
        "%(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Qt UI handler (if text_edit provided)
    qt_handler = QTextEditLogger(text_edit)
    qt_handler.setLevel(logging.INFO)  # Only INFO and above for UI
    root_logger.addHandler(qt_handler)

    # Log startup message
    logging.info(f"{config.APP_NAME} v{config.APP_VERSION} - Logging initialized")
    logging.info(f"Log file: {config.LOG_FILE_PATH}")
    logging.info(f"Device: {config.DEFAULT_DEVICE}")

    return qt_handler


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Import for convenience
import logging.handlers
