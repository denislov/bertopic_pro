"""
BERTopic Pro - Application Entry Point
Main entry point for the BERTopic Pro desktop application.
"""

import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import Qt

import config
from app.ui.main_window import MainWindow


def setup_fonts():
    """Set up application fonts for proper Chinese text rendering."""
    # Try to load custom fonts if available
    font_path = config.FONTS_DIR / "NotoSansCJK-Regular.ttc"
    if font_path.exists():
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id != -1:
            logging.info(f"Loaded custom font: {font_path}")

    # Set default application font with Chinese support
    app_font = QFont("Noto Sans CJK SC", 10)
    if not app_font.exactMatch():
        # Fallback to system Chinese fonts
        app_font = QFont("Microsoft YaHei", 10)
        if not app_font.exactMatch():
            app_font = QFont("SimHei", 10)

    return app_font


def load_stylesheet() -> str:
    """
    Load QSS stylesheet.

    Returns:
        Stylesheet content as string
    """
    style_path = config.BASE_DIR / "app" / "ui" / "styles" / "theme.qss"
    if style_path.exists():
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                stylesheet = f.read()
            logging.info(f"Loaded stylesheet: {style_path}")
            return stylesheet
        except Exception as e:
            logging.error(f"Failed to load stylesheet: {e}")
            return ""
    else:
        logging.warning(f"Stylesheet not found: {style_path}")
        return ""


def setup_exception_hook():
    """Set up global exception hook for unhandled exceptions."""

    def exception_hook(exctype, value, tb):
        """Handle uncaught exceptions."""
        logging.error("Uncaught exception", exc_info=(exctype, value, tb))

        # Show error dialog in GUI
        from PySide6.QtWidgets import QMessageBox

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("错误")
        msg.setText("应用程序遇到未处理的错误")
        msg.setDetailedText(f"{exctype.__name__}: {value}")
        msg.exec()

        # Call default handler
        sys.__excepthook__(exctype, value, tb)

    sys.excepthook = exception_hook


def setup_basic_logging():
    """Set up basic logging before Qt UI is initialized."""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )


def main():
    """Main application entry point."""
    # Set up basic logging first
    setup_basic_logging()

    logging.info("=" * 60)
    logging.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    logging.info("=" * 60)

    # Enable High DPI scaling (Qt 6.5+ handles this automatically)
    # These attributes are deprecated in Qt 6.5+, only set if available
    try:
        if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    except AttributeError:
        pass  # Qt 6.5+ doesn't need this

    try:
        if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        pass  # Qt 6.5+ doesn't need this

    # Create application
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    app.setOrganizationName(config.ORGANIZATION_NAME)

    # Set up fonts
    app_font = setup_fonts()
    app.setFont(app_font)
    logging.info(f"Application font: {app_font.family()}")

    # Load and apply stylesheet
    stylesheet = load_stylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)

    # Set up exception hook
    setup_exception_hook()

    # Log system information
    logging.info(f"Python version: {sys.version}")
    logging.info(f"PySide6 version: {app.applicationVersion()}")
    logging.info(f"Platform: {sys.platform}")
    logging.info(f"Working directory: {config.BASE_DIR}")
    logging.info(f"Device: {config.DEFAULT_DEVICE}")

    # Create and show main window
    try:
        window = MainWindow()
        window.show()
        logging.info("Main window created and shown")
    except Exception as e:
        logging.error(f"Failed to create main window: {e}", exc_info=True)
        return 1

    # Run application event loop
    logging.info("Entering application event loop")
    exit_code = app.exec()

    # Cleanup
    logging.info(f"Application exiting with code: {exit_code}")
    logging.info("=" * 60)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
