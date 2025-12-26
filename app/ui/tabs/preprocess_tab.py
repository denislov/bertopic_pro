"""
BERTopic Pro - Preprocessing Tab
Tab 1: Data import and text preprocessing with full functionality.
"""

from pathlib import Path
from typing import Optional
import pandas as pd

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QComboBox, QGroupBox,
    QCheckBox, QProgressBar, QLineEdit, QMessageBox,
    QSplitter, QWidget, QHeaderView
)
from PySide6.QtCore import Qt, Signal, QThread

from app.ui.tabs.base_tab import BaseTab
from app.utils.file_helpers import read_file, preview_dataframe, save_dataframe, get_column_info
from app.utils.validators import (
    validate_file_path, validate_text_column,
    validate_timestamp_column, get_recommended_columns
)
from app.core.processor import TextProcessor
from app.core.workers.base_worker import BaseWorker
import config


class ProcessingWorker(BaseWorker):
    """Worker thread for text processing."""

    def __init__(self, df: pd.DataFrame, text_column: str, processor: TextProcessor, options: dict):
        super().__init__()
        self.df = df
        self.text_column = text_column
        self.processor = processor
        self.options = options

    def run(self):
        """Process texts in background."""
        try:
            def progress_callback(pct, msg):
                if not self._is_cancelled:
                    self.emit_progress(pct, msg)

            # Process dataframe
            processed_df = self.processor.process_dataframe(
                self.df,
                self.text_column,
                progress_callback=progress_callback,
                **self.options
            )

            self.emit_finished(processed_df)

        except Exception as e:
            self.emit_error(e)


class PreprocessTab(BaseTab):
    """Tab for data preprocessing with full functionality."""

    def setup_ui(self):
        """Set up the UI for this tab."""
        main_layout = QVBoxLayout(self)

        # Splitter for top and bottom sections
        splitter = QSplitter(Qt.Vertical)

        # Top section: File loading and options
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Title
        title = QLabel("1. 数据预处理")
        title.setProperty("class", "title")
        top_layout.addWidget(title)

        row_layout = QHBoxLayout()
        # File selection section
        file_group = self.create_file_section()
        row_layout.addWidget(file_group)

        # Column mapping section
        column_group = self.create_column_section()
        row_layout.addWidget(column_group)
        top_layout.addLayout(row_layout)

        # Processing options section
        options_layout = QHBoxLayout()

        # Left: Text cleaning options
        cleaning_group = self.create_cleaning_section()
        options_layout.addWidget(cleaning_group)

        # Right: Jieba settings
        jieba_group = self.create_jieba_section()
        options_layout.addWidget(jieba_group)

        top_layout.addLayout(options_layout)

        # Process button and progress
        process_layout = QHBoxLayout()

        self.process_btn = QPushButton("开始处理")
        self.process_btn.setEnabled(False)
        self.process_btn.clicked.connect(self.start_processing)
        process_layout.addWidget(self.process_btn)

        self.save_btn = QPushButton("保存结果")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_results)
        process_layout.addWidget(self.save_btn)

        process_layout.addStretch()

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        process_layout.addWidget(self.progress_bar)

        top_layout.addLayout(process_layout)

        splitter.addWidget(top_widget)

        # Bottom section: Data preview table
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)

        preview_label = QLabel("数据预览")
        preview_label.setProperty("class", "subtitle")
        preview_layout.addWidget(preview_label)

        self.data_table = QTableWidget()
        self.data_table.setAlternatingRowColors(True)
        preview_layout.addWidget(self.data_table)

        splitter.addWidget(preview_widget)

        # Set splitter sizes
        splitter.setSizes([400, 400])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # State variables
        self.current_df: Optional[pd.DataFrame] = None
        self.processed_df: Optional[pd.DataFrame] = None
        self.processor: Optional[TextProcessor] = None
        self.worker_thread: Optional[QThread] = None
        self.worker: Optional[ProcessingWorker] = None

    def create_file_section(self) -> QGroupBox:
        """Create file selection section."""
        group = QGroupBox("文件导入")
        layout = QGridLayout()

        # File path input
        layout.addWidget(QLabel("文件路径:"), 0, 0)
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("选择 CSV、Excel 或 TXT 文件...")
        layout.addWidget(self.file_path_input, 0, 1)

        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_btn, 0, 2)

        self.load_btn = QPushButton("加载数据")
        self.load_btn.clicked.connect(self.load_file)
        layout.addWidget(self.load_btn, 0, 3)

        # File info label
        self.file_info_label = QLabel("未加载数据")
        self.file_info_label.setProperty("class", "hint")
        layout.addWidget(self.file_info_label, 1, 0, 1, 4)

        group.setLayout(layout)
        return group

    def create_column_section(self) -> QGroupBox:
        """Create column mapping section."""
        group = QGroupBox("列映射")
        layout = QGridLayout()

        # Text column
        layout.addWidget(QLabel("文本列:"), 0, 0)
        self.text_column_combo = QComboBox()
        self.text_column_combo.setPlaceholderText("选择包含文本的列...")
        layout.addWidget(self.text_column_combo, 0, 1)

        # Timestamp column (optional)
        layout.addWidget(QLabel("时间戳列 (可选):"), 1, 0)
        self.timestamp_column_combo = QComboBox()
        self.timestamp_column_combo.addItem("(无)")
        self.timestamp_column_combo.setPlaceholderText("选择时间戳列...")
        layout.addWidget(self.timestamp_column_combo, 1, 1)

        group.setLayout(layout)
        return group

    def create_cleaning_section(self) -> QGroupBox:
        """Create text cleaning options section."""
        group = QGroupBox("文本清洗选项")
        layout = QVBoxLayout()

        self.remove_urls_cb = QCheckBox("去除 URL")
        self.remove_urls_cb.setChecked(config.DEFAULT_REMOVE_URLS)
        self.remove_urls_cb.setToolTip("移除文本中的网址链接")
        layout.addWidget(self.remove_urls_cb)

        self.remove_emails_cb = QCheckBox("去除邮箱地址")
        self.remove_emails_cb.setChecked(config.DEFAULT_REMOVE_EMAILS)
        self.remove_emails_cb.setToolTip("移除文本中的电子邮件地址")
        layout.addWidget(self.remove_emails_cb)

        self.remove_punct_cb = QCheckBox("去除标点符号")
        self.remove_punct_cb.setChecked(config.DEFAULT_REMOVE_PUNCTUATION)
        self.remove_punct_cb.setToolTip("移除所有标点符号")
        layout.addWidget(self.remove_punct_cb)

        self.lowercase_cb = QCheckBox("转换为小写")
        self.lowercase_cb.setChecked(config.DEFAULT_LOWERCASE)
        self.lowercase_cb.setToolTip("将所有文本转换为小写（适用于英文）")
        layout.addWidget(self.lowercase_cb)

        self.segment_cb = QCheckBox("Jieba 分词")
        self.segment_cb.setChecked(True)
        self.segment_cb.setToolTip("使用 Jieba 进行中文分词")
        layout.addWidget(self.segment_cb)

        self.remove_stopwords_cb = QCheckBox("去除停用词")
        self.remove_stopwords_cb.setChecked(True)
        self.remove_stopwords_cb.setToolTip("移除常见停用词")
        layout.addWidget(self.remove_stopwords_cb)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def create_jieba_section(self) -> QGroupBox:
        """Create Jieba settings section."""
        group = QGroupBox("Jieba 设置")
        layout = QVBoxLayout()

        # Custom dictionary
        dict_layout = QHBoxLayout()
        dict_layout.addWidget(QLabel("自定义词典:"))
        self.custom_dict_input = QLineEdit()
        self.custom_dict_input.setPlaceholderText("(可选)")
        dict_layout.addWidget(self.custom_dict_input)
        browse_dict_btn = QPushButton("...")
        browse_dict_btn.setMaximumWidth(40)
        browse_dict_btn.clicked.connect(self.browse_custom_dict)
        dict_layout.addWidget(browse_dict_btn)
        layout.addLayout(dict_layout)

        # Stopwords file
        stopwords_layout = QHBoxLayout()
        stopwords_layout.addWidget(QLabel("停用词表:"))
        self.stopwords_input = QLineEdit()
        self.stopwords_input.setPlaceholderText("(可选，默认使用内置)")
        stopwords_layout.addWidget(self.stopwords_input)
        browse_stop_btn = QPushButton("...")
        browse_stop_btn.setMaximumWidth(40)
        browse_stop_btn.clicked.connect(self.browse_stopwords)
        stopwords_layout.addWidget(browse_stop_btn)
        layout.addLayout(stopwords_layout)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def browse_file(self):
        """Browse for data file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择数据文件",
            str(config.RAW_DATA_DIR),
            "数据文件 (*.csv *.xlsx *.xls *.txt);;All Files (*)"
        )

        if file_path:
            self.file_path_input.setText(file_path)

    def browse_custom_dict(self):
        """Browse for custom Jieba dictionary."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择自定义词典",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            self.custom_dict_input.setText(file_path)

    def browse_stopwords(self):
        """Browse for stopwords file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择停用词表",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            self.stopwords_input.setText(file_path)

    def load_file(self):
        """Load data file."""
        file_path = self.file_path_input.text().strip()

        # Validate file path
        is_valid, error = validate_file_path(file_path)
        if not is_valid:
            QMessageBox.warning(self, "文件错误", error)
            return

        try:
            # Read file
            self.status_changed.emit(f"正在加载文件: {Path(file_path).name}")
            df = read_file(file_path)

            self.current_df = df

            # Update file info
            self.file_info_label.setText(
                f"已加载: {len(df)} 行, {len(df.columns)} 列"
            )

            # Update column combos
            self.update_column_combos()

            # Show preview
            self.show_preview(df)

            # Enable processing
            self.process_btn.setEnabled(True)

            # Emit signal
            self.data_loaded.emit(df)

            self.status_changed.emit(f"文件加载成功: {len(df)} 行")
            self.logger.info(f"Loaded file: {file_path}")

        except Exception as e:
            self.logger.error(f"Failed to load file: {e}")
            QMessageBox.critical(self, "加载失败", f"无法加载文件:\n{str(e)}")
            self.error_occurred.emit(str(e))

    def update_column_combos(self):
        """Update column combo boxes."""
        if self.current_df is None:
            return

        # Clear combos
        self.text_column_combo.clear()
        self.timestamp_column_combo.clear()
        self.timestamp_column_combo.addItem("(无)")

        # Add columns
        for col in self.current_df.columns:
            self.text_column_combo.addItem(col)
            self.timestamp_column_combo.addItem(col)

        # Set recommended columns
        text_recs = get_recommended_columns(self.current_df, for_text=True)
        if text_recs:
            idx = self.text_column_combo.findText(text_recs[0])
            if idx >= 0:
                self.text_column_combo.setCurrentIndex(idx)

        time_recs = get_recommended_columns(self.current_df, for_text=False)
        if time_recs:
            idx = self.timestamp_column_combo.findText(time_recs[0])
            if idx >= 0:
                self.timestamp_column_combo.setCurrentIndex(idx)

    def show_preview(self, df: pd.DataFrame):
        """Show data preview in table."""
        preview = preview_dataframe(df)

        # Set table dimensions
        self.data_table.setRowCount(len(preview))
        self.data_table.setColumnCount(len(preview.columns))
        self.data_table.setHorizontalHeaderLabels(preview.columns.tolist())

        # Fill table
        for i, row in preview.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.data_table.setItem(i, j, item)

        # Resize columns
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def start_processing(self):
        """Start text processing."""
        if self.current_df is None:
            QMessageBox.warning(self, "错误", "请先加载数据文件")
            return

        text_column = self.text_column_combo.currentText()
        if not text_column:
            QMessageBox.warning(self, "错误", "请选择文本列")
            return

        # Validate text column
        is_valid, error, stats = validate_text_column(self.current_df, text_column)
        if not is_valid:
            QMessageBox.warning(self, "列验证失败", error)
            return

        # Initialize processor
        stopwords_path = Path(self.stopwords_input.text()) if self.stopwords_input.text() else None
        custom_dict_path = Path(self.custom_dict_input.text()) if self.custom_dict_input.text() else None

        self.processor = TextProcessor(
            stopwords_path=stopwords_path,
            custom_dict_path=custom_dict_path
        )

        # Get processing options
        options = {
            'segment': self.segment_cb.isChecked(),
            'remove_stopwords': self.remove_stopwords_cb.isChecked(),
            'clean_options': {
                'remove_urls': self.remove_urls_cb.isChecked(),
                'remove_emails': self.remove_emails_cb.isChecked(),
                'remove_punctuation': self.remove_punct_cb.isChecked(),
                'lowercase': self.lowercase_cb.isChecked(),
            }
        }

        # Start worker
        self.worker = ProcessingWorker(self.current_df, text_column, self.processor, options)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        # Connect signals
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.on_status_change)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)

        # Update UI
        self.process_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Start
        self.worker_thread.start()
        self.logger.info("Text processing started")

    def update_progress(self, value: int):
        """Update progress bar."""
        self.progress_bar.setValue(value)

    def on_processing_finished(self, result: pd.DataFrame):
        """Handle processing completion."""
        self.processed_df = result
        self.data_loaded.emit(result)

        # Update UI
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.save_btn.setEnabled(True)

        # Show processed preview
        self.show_preview(result)

        QMessageBox.information(self, "处理完成", f"成功处理 {len(result)} 行数据")
        self.logger.info("Text processing completed")

    def on_processing_error(self, error: Exception):
        """Handle processing error."""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)

        QMessageBox.critical(self, "处理失败", f"文本处理出错:\n{str(error)}")
        self.error_occurred.emit(str(error))

    def save_results(self):
        """Save processed results."""
        if self.processed_df is None:
            QMessageBox.warning(self, "错误", "没有可保存的处理结果")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存处理结果",
            str(config.PROCESSED_DATA_DIR / "processed_data.csv"),
            "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )

        if file_path:
            try:
                save_dataframe(self.processed_df, file_path)
                QMessageBox.information(self, "保存成功", f"数据已保存到:\n{file_path}")
                self.logger.info(f"Saved processed data to: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"无法保存文件:\n{str(e)}")
                self.error_occurred.emit(str(e))
