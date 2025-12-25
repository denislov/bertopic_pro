"""
BERTopic Pro - Main Window
Main application window with tabbed interface and console.
"""

from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QPlainTextEdit,
    QSplitter,
    QMenuBar,
    QMenu,
    QStatusBar,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon

from app.ui.tabs.preprocess_tab import PreprocessTab
from app.ui.tabs.modeling_tab import ModelingTab
from app.ui.tabs.visualization_tab import VisualizationTab
from app.ui.tabs.settings_tab import SettingsTab
from app.utils.logger import get_logger, setup_logging
from app.utils.config_manager import get_config_manager
import config


class MainWindow(QMainWindow):
    """
    Main application window.

    Contains:
    - Menu bar (File, View, Help)
    - Tab widget with 4 tabs (Preprocess, Modeling, Visualization, Settings)
    - Bottom console for logging
    - Status bar
    """

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        # Get config manager
        self.config_manager = get_config_manager()

        # Get logger (will be set up after console is created)
        self.logger = get_logger(self.__class__.__name__)

        # Initialize UI components
        self.tab_widget: Optional[QTabWidget] = None
        self.console: Optional[QPlainTextEdit] = None
        self.preprocess_tab: Optional[PreprocessTab] = None
        self.modeling_tab: Optional[ModelingTab] = None
        self.visualization_tab: Optional[VisualizationTab] = None
        self.settings_tab: Optional[SettingsTab] = None

        # Set up the UI
        self.setup_ui()

        # Set up logging (now that console exists)
        self.qt_logger = setup_logging(self.console)

        # Restore window geometry
        self.restore_geometry()

        self.logger.info(f"{config.APP_NAME} v{config.APP_VERSION} started")

    def setup_ui(self):
        """Set up the main window UI."""
        # Window properties
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.resize(config.WINDOW_DEFAULT_WIDTH, config.WINDOW_DEFAULT_HEIGHT)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create splitter for tabs and console
        splitter = QSplitter(Qt.Vertical)

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setMovable(False)

        # Create tabs
        self.preprocess_tab = PreprocessTab()
        self.modeling_tab = ModelingTab()
        self.visualization_tab = VisualizationTab()
        self.settings_tab = SettingsTab()

        # Add tabs to tab widget
        self.tab_widget.addTab(self.preprocess_tab, "1. 数据预处理")
        self.tab_widget.addTab(self.modeling_tab, "2. BERTopic 建模")
        self.tab_widget.addTab(self.visualization_tab, "3. 可视化生成")
        self.tab_widget.addTab(self.settings_tab, "4. 系统设置")

        # Initially disable tabs 2 and 3 (until data is loaded and model trained)
        self.tab_widget.setTabEnabled(1, False)  # Modeling tab
        self.tab_widget.setTabEnabled(2, False)  # Visualization tab

        # Create console
        self.console = QPlainTextEdit()
        self.console.setObjectName("console")  # For QSS styling
        self.console.setReadOnly(True)
        self.console.setMaximumBlockCount(config.CONSOLE_LOG_MAX_LINES)
        self.console.setPlaceholderText("应用日志将显示在这里...")

        # Add to splitter
        splitter.addWidget(self.tab_widget)
        splitter.addWidget(self.console)

        # Set initial splitter sizes (70% tabs, 30% console)
        splitter.setSizes([700, 300])

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        # Create menu bar
        self.create_menu_bar()

        # Create status bar
        self.create_status_bar()

        # Connect tab signals
        self.connect_tab_signals()

    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("文件")

        # Open action
        open_action = QAction("打开数据文件...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open_file)
        file_menu.addAction(open_action)

        # Recent files submenu
        recent_menu = file_menu.addMenu("最近打开")
        self.update_recent_files_menu(recent_menu)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("视图")

        # Toggle console action
        toggle_console_action = QAction("显示/隐藏控制台", self)
        toggle_console_action.setShortcut("Ctrl+`")
        toggle_console_action.triggered.connect(self.toggle_console)
        view_menu.addAction(toggle_console_action)

        # Clear console action
        clear_console_action = QAction("清空控制台", self)
        clear_console_action.triggered.connect(self.clear_console)
        view_menu.addAction(clear_console_action)

        # Help menu
        help_menu = menubar.addMenu("帮助")

        # About action
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_status_bar(self):
        """Create the status bar."""
        self.statusBar().showMessage("就绪")

    def connect_tab_signals(self):
        """Connect signals between tabs."""
        # When data is loaded in preprocess tab, enable modeling tab
        self.preprocess_tab.data_loaded.connect(self.on_data_loaded)

        # When model is trained in modeling tab, enable visualization tab
        self.modeling_tab.model_trained.connect(self.on_model_trained)

        # Connect error signals to status bar
        for tab in [
            self.preprocess_tab,
            self.modeling_tab,
            self.visualization_tab,
            self.settings_tab,
        ]:
            tab.error_occurred.connect(self.on_error)
            tab.status_changed.connect(self.on_status_change)

    # ========================================================================
    # Slot Methods
    # ========================================================================

    def on_open_file(self):
        """Handle open file action."""
        self.logger.info("Open file dialog triggered")
        # Switch to preprocess tab
        self.tab_widget.setCurrentIndex(0)
        self.statusBar().showMessage("请在数据预处理标签中选择文件", 3000)

    def on_data_loaded(self, data):
        """
        Handle data loaded signal.

        Args:
            data: Loaded data object (pandas DataFrame)
        """
        self.logger.info("Data loaded, enabling modeling tab")
        self.tab_widget.setTabEnabled(1, True)

        # Pass processed data to modeling tab if it has processed text
        if hasattr(data, 'columns') and 'text_processed' in data.columns:
            self.modeling_tab.set_processed_data(data)
            self.statusBar().showMessage("处理后的数据已传递到建模模块", 3000)
        else:
            self.statusBar().showMessage("数据加载完成，建模功能已启用", 3000)

    def on_model_trained(self, model):
        """
        Handle model trained signal.

        Args:
            model: Trained model result dict containing 'topic_analyzer'
        """
        self.logger.info("Model trained, enabling visualization tab")
        self.tab_widget.setTabEnabled(2, True)

        # Pass topic analyzer to visualization tab
        if isinstance(model, dict) and 'topic_analyzer' in model:
            topic_analyzer = model['topic_analyzer']
            self.visualization_tab.set_topic_analyzer(topic_analyzer)
            self.statusBar().showMessage("模型训练完成，可视化功能已启用", 3000)
        else:
            self.statusBar().showMessage("模型训练完成", 3000)

    def on_error(self, error_message: str):
        """
        Handle error signal.

        Args:
            error_message: Error message
        """
        self.statusBar().showMessage(f"错误: {error_message}", 5000)

    def on_status_change(self, status_message: str):
        """
        Handle status change signal.

        Args:
            status_message: Status message
        """
        self.statusBar().showMessage(status_message, 3000)

    def toggle_console(self):
        """Toggle console visibility."""
        self.console.setVisible(not self.console.isVisible())

    def clear_console(self):
        """Clear console content."""
        self.console.clear()
        self.logger.info("Console cleared")

    def update_recent_files_menu(self, menu: QMenu):
        """
        Update recent files menu.

        Args:
            menu: Recent files menu
        """
        menu.clear()
        recent_files = self.config_manager.get_recent_files()

        if not recent_files:
            no_files_action = QAction("(无最近文件)", self)
            no_files_action.setEnabled(False)
            menu.addAction(no_files_action)
        else:
            for file_path in recent_files:
                action = QAction(file_path, self)
                action.triggered.connect(lambda checked, f=file_path: self.open_recent_file(f))
                menu.addAction(action)

            menu.addSeparator()
            clear_action = QAction("清空列表", self)
            clear_action.triggered.connect(self.clear_recent_files)
            menu.addAction(clear_action)

    def open_recent_file(self, file_path: str):
        """
        Open a recent file.

        Args:
            file_path: Path to the file
        """
        self.logger.info(f"Opening recent file: {file_path}")
        # TODO: Implement file opening logic
        self.statusBar().showMessage(f"正在打开: {file_path}", 3000)

    def clear_recent_files(self):
        """Clear recent files list."""
        self.config_manager.clear_recent_files()
        self.logger.info("Recent files cleared")

    def show_about(self):
        """Show about dialog."""
        from PySide6.QtWidgets import QMessageBox

        QMessageBox.about(
            self,
            "关于 BERTopic Pro",
            f"""
            <h3>{config.APP_NAME}</h3>
            <p>版本: {config.APP_VERSION}</p>
            <p>专业的主题建模分析平台</p>
            <p>基于 BERTopic 和 PySide6 构建</p>
            <p>设备: {config.DEFAULT_DEVICE.upper()}</p>
            """,
        )

    # ========================================================================
    # Window State Management
    # ========================================================================

    def restore_geometry(self):
        """Restore window geometry from config."""
        geometry = self.config_manager.load_window_geometry()
        if geometry:
            self.restoreGeometry(geometry)

    def save_geometry(self):
        """Save window geometry to config."""
        self.config_manager.save_window_geometry(self.saveGeometry())

    def closeEvent(self, event):
        """
        Handle window close event.

        Args:
            event: Close event
        """
        self.logger.info("Application closing")

        # Save window geometry
        self.save_geometry()

        # Cleanup tabs
        for tab in [
            self.preprocess_tab,
            self.modeling_tab,
            self.visualization_tab,
            self.settings_tab,
        ]:
            if tab:
                tab.cleanup()

        event.accept()
