"""
BERTopic Pro - Modeling Tab
Tab 2: BERTopic model training with parameter configuration.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFileDialog, QGroupBox,
    QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox,
    QProgressBar, QMessageBox, QSplitter, QWidget,
    QTextEdit, QLineEdit, QInputDialog,
)
from PySide6.QtCore import Qt, Signal, QThread

from app.ui.tabs.base_tab import BaseTab
from app.core.model_manager import ModelManager
from app.core.topic_analyzer import TopicAnalyzer, TopicModelParams
from app.core.workers.bertopic_worker import BertopicWorker
from app.core.workers.download_worker import DownloadWorker
import config


class ModelingTab(BaseTab):
    """Tab for BERTopic model training."""

    def setup_ui(self):
        """Set up the UI for this tab."""
        main_layout = QVBoxLayout(self)

        # Splitter for top and bottom sections
        splitter = QSplitter(Qt.Vertical)

        # Top section: Parameters
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Title
        title = QLabel("2. BERTopic 建模")
        title.setProperty("class", "title")
        top_layout.addWidget(title)

        # Embedding model section
        embedding_group = self.create_embedding_section()
        top_layout.addWidget(embedding_group)

        # Parameters layout (2 columns)
        params_layout = QHBoxLayout()

        # Left: UMAP parameters
        umap_group = self.create_umap_section()
        params_layout.addWidget(umap_group)

        # Right: HDBSCAN parameters
        hdbscan_group = self.create_hdbscan_section()
        params_layout.addWidget(hdbscan_group)

        top_layout.addLayout(params_layout)

        # Advanced settings (collapsible)
        advanced_group = self.create_advanced_section()
        top_layout.addWidget(advanced_group)

        # Action buttons
        button_layout = QHBoxLayout()

        self.train_btn = QPushButton("开始训练")
        # self.train_btn.setEnabled(False)
        self.train_btn.clicked.connect(self.start_training)
        button_layout.addWidget(self.train_btn)

        self.save_model_btn = QPushButton("保存模型")
        self.save_model_btn.setEnabled(False)
        self.save_model_btn.clicked.connect(self.save_model)
        button_layout.addWidget(self.save_model_btn)

        self.load_model_btn = QPushButton("加载模型")
        self.load_model_btn.clicked.connect(self.load_model)
        button_layout.addWidget(self.load_model_btn)

        button_layout.addStretch()

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        button_layout.addWidget(self.progress_bar)

        top_layout.addLayout(button_layout)

        splitter.addWidget(top_widget)

        # Bottom section: Results
        results_widget = QWidget()
        results_layout = QVBoxLayout(results_widget)

        results_label = QLabel("训练结果")
        results_label.setProperty("class", "subtitle")
        results_layout.addWidget(results_label)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("训练完成后将在此显示主题信息...")
        results_layout.addWidget(self.results_text)

        splitter.addWidget(results_widget)

        # Set splitter sizes
        splitter.setSizes([500, 300])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # State variables
        self.processed_data: Optional[pd.DataFrame] = None
        self.model_manager = ModelManager()
        self.topic_analyzer: Optional[TopicAnalyzer] = None
        self.worker_thread: Optional[QThread] = None
        self.worker = None

        # Connect to preprocessing tab
        self._setup_connections()

    def create_embedding_section(self) -> QGroupBox:
        """Create embedding model selection section."""
        group = QGroupBox("嵌入模型")
        layout = QGridLayout()

        # Model selection
        layout.addWidget(QLabel("模型:"), 0, 0)
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)

        # Add recommended models
        recommended_models = [
            config.DEFAULT_EMBEDDING_MODEL,
            "sentence-transformers/distiluse-base-multilingual-cased-v1",
            "BAAI/bge-base-zh-v1.5",
            "shibing624/text2vec-base-chinese",
        ]
        self.model_combo.addItems(recommended_models)

        layout.addWidget(self.model_combo, 0, 1)

        # Browse local model
        browse_btn = QPushButton("本地模型...")
        browse_btn.clicked.connect(self.browse_local_model)
        layout.addWidget(browse_btn, 0, 2)

        # Download button
        self.download_btn = QPushButton("下载模型")
        self.download_btn.clicked.connect(self.download_model)
        layout.addWidget(self.download_btn, 0, 3)

        # Model info label
        self.model_info_label = QLabel("未选择模型")
        self.model_info_label.setProperty("class", "hint")
        layout.addWidget(self.model_info_label, 1, 0, 1, 4)

        group.setLayout(layout)
        return group

    def create_umap_section(self) -> QGroupBox:
        """Create UMAP parameters section."""
        group = QGroupBox("UMAP 参数")
        layout = QGridLayout()

        # n_neighbors
        layout.addWidget(QLabel("n_neighbors:"), 0, 0)
        self.umap_n_neighbors_spin = QSpinBox()
        self.umap_n_neighbors_spin.setRange(2, 200)
        self.umap_n_neighbors_spin.setValue(config.DEFAULT_UMAP_N_NEIGHBORS)
        self.umap_n_neighbors_spin.setToolTip("较大值保留全局结构，较小值保留局部结构")
        layout.addWidget(self.umap_n_neighbors_spin, 0, 1)

        # n_components
        layout.addWidget(QLabel("n_components:"), 1, 0)
        self.umap_n_components_spin = QSpinBox()
        self.umap_n_components_spin.setRange(2, 100)
        self.umap_n_components_spin.setValue(config.DEFAULT_UMAP_N_COMPONENTS)
        self.umap_n_components_spin.setToolTip("降维后的维度数")
        layout.addWidget(self.umap_n_components_spin, 1, 1)

        # min_dist
        layout.addWidget(QLabel("min_dist:"), 2, 0)
        self.umap_min_dist_spin = QDoubleSpinBox()
        self.umap_min_dist_spin.setRange(0.0, 1.0)
        self.umap_min_dist_spin.setSingleStep(0.01)
        self.umap_min_dist_spin.setValue(config.DEFAULT_UMAP_MIN_DIST)
        self.umap_min_dist_spin.setToolTip("控制点之间的最小距离")
        layout.addWidget(self.umap_min_dist_spin, 2, 1)

        # metric
        layout.addWidget(QLabel("metric:"), 3, 0)
        self.umap_metric_combo = QComboBox()
        self.umap_metric_combo.addItems(['cosine', 'euclidean', 'manhattan'])
        self.umap_metric_combo.setToolTip("距离度量方式")
        layout.addWidget(self.umap_metric_combo, 3, 1)

        group.setLayout(layout)
        return group

    def create_hdbscan_section(self) -> QGroupBox:
        """Create HDBSCAN parameters section."""
        group = QGroupBox("HDBSCAN 参数")
        layout = QGridLayout()

        # min_cluster_size
        layout.addWidget(QLabel("min_cluster_size:"), 0, 0)
        self.hdbscan_min_cluster_spin = QSpinBox()
        self.hdbscan_min_cluster_spin.setRange(2, 500)
        self.hdbscan_min_cluster_spin.setValue(config.DEFAULT_HDBSCAN_MIN_CLUSTER_SIZE)
        self.hdbscan_min_cluster_spin.setToolTip("最小簇大小")
        layout.addWidget(self.hdbscan_min_cluster_spin, 0, 1)

        # min_samples
        layout.addWidget(QLabel("min_samples:"), 1, 0)
        self.hdbscan_min_samples_spin = QSpinBox()
        self.hdbscan_min_samples_spin.setRange(1, 100)
        self.hdbscan_min_samples_spin.setValue(config.DEFAULT_HDBSCAN_MIN_SAMPLES)
        self.hdbscan_min_samples_spin.setToolTip("核心点的最小邻居数")
        layout.addWidget(self.hdbscan_min_samples_spin, 1, 1)

        # metric
        layout.addWidget(QLabel("metric:"), 2, 0)
        self.hdbscan_metric_combo = QComboBox()
        self.hdbscan_metric_combo.addItems(['euclidean', 'manhattan', 'cosine'])
        self.hdbscan_metric_combo.setToolTip("距离度量方式")
        layout.addWidget(self.hdbscan_metric_combo, 2, 1)

        group.setLayout(layout)
        return group

    def create_advanced_section(self) -> QGroupBox:
        """Create advanced settings section."""
        group = QGroupBox("高级设置")
        layout = QGridLayout()

        # top_n_words
        layout.addWidget(QLabel("每主题词数:"), 0, 0)
        self.top_n_words_spin = QSpinBox()
        self.top_n_words_spin.setRange(5, 50)
        self.top_n_words_spin.setValue(config.DEFAULT_TOP_N_WORDS)
        layout.addWidget(self.top_n_words_spin, 0, 1)

        # min_topic_size
        layout.addWidget(QLabel("最小主题大小:"), 1, 0)
        self.min_topic_size_spin = QSpinBox()
        self.min_topic_size_spin.setRange(2, 100)
        self.min_topic_size_spin.setValue(config.DEFAULT_MIN_TOPIC_SIZE)
        layout.addWidget(self.min_topic_size_spin, 1, 1)

        # nr_topics
        layout.addWidget(QLabel("目标主题数 (可选):"), 2, 0)
        self.nr_topics_spin = QSpinBox()
        self.nr_topics_spin.setRange(0, 1000)
        self.nr_topics_spin.setValue(0)
        self.nr_topics_spin.setSpecialValueText("自动")
        self.nr_topics_spin.setToolTip("设为 0 表示自动确定主题数")
        layout.addWidget(self.nr_topics_spin, 2, 1)

        # calculate_probabilities
        self.calc_probs_cb = QCheckBox("计算主题概率")
        self.calc_probs_cb.setToolTip("计算文档的主题概率分布（较慢）")
        layout.addWidget(self.calc_probs_cb, 3, 0, 1, 2)

        group.setLayout(layout)
        return group

    def _setup_connections(self):
        """Set up connections to other tabs."""
        # This will be called when data is loaded from preprocessing tab
        pass

    def browse_local_model(self):
        """Browse for local embedding model."""
        model_path = QFileDialog.getExistingDirectory(
            self,
            "选择本地嵌入模型目录",
            str(config.MODEL_DIR),
        )

        if model_path:
            self.model_combo.setCurrentText(model_path)
            self.model_info_label.setText(f"本地模型: {Path(model_path).name}")

    def download_model(self):
        """Download embedding model."""
        model_name = self.model_combo.currentText().strip()

        if not model_name:
            QMessageBox.warning(self, "错误", "请先选择或输入模型名称")
            return

        # Check if it's a local path
        if Path(model_name).exists():
            QMessageBox.information(self, "提示", "这是本地模型，无需下载")
            return

        # Start download worker
        self.worker = DownloadWorker(model_name, self.model_manager)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        # Connect signals
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.on_status_change)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_download_error)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)

        # Update UI
        self.download_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Start
        self.worker_thread.start()
        self.logger.info(f"Downloading model: {model_name}")

    def on_download_finished(self, result):
        """Handle download completion."""
        self.progress_bar.setVisible(False)
        self.download_btn.setEnabled(True)

        model_name = result['model_name']
        model_path = result['model_path']

        self.model_info_label.setText(f"模型已下载: {model_name}")
        QMessageBox.information(self, "下载完成", f"模型已下载到:\\n{model_path}")
        self.logger.info(f"Model downloaded: {model_name}")

    def on_download_error(self, error):
        """Handle download error."""
        self.progress_bar.setVisible(False)
        self.download_btn.setEnabled(True)

        QMessageBox.critical(self, "下载失败", f"模型下载失败:\\n{str(error)}")
        self.error_occurred.emit(str(error))

    def set_processed_data(self, df: pd.DataFrame):
        """
        Set processed data from preprocessing tab.

        Args:
            df: DataFrame with processed text
        """
        self.processed_data = df
        self.train_btn.setEnabled(True)
        self.logger.info(f"Received processed data: {len(df)} documents")

    def start_training(self):
        """Start BERTopic training."""
        if self.processed_data is None:
            QMessageBox.warning(self, "错误", "请先在 Tab 1 中加载和处理数据")
            return

        # Check if processed text column exists
        if 'text_processed' not in self.processed_data.columns:
            QMessageBox.warning(self, "错误", "未找到处理后的文本列 'text_processed'")
            return

        # Get documents
        documents = self.processed_data['text_processed'].tolist()

        if not documents:
            QMessageBox.warning(self, "错误", "没有可用的文档进行训练")
            return

        # Get model name
        embedding_model = self.model_combo.currentText().strip()

        if not embedding_model:
            QMessageBox.warning(self, "错误", "请选择嵌入模型")
            return

        # Collect parameters
        params = TopicModelParams(
            embedding_model=embedding_model,
            umap_n_neighbors=self.umap_n_neighbors_spin.value(),
            umap_n_components=self.umap_n_components_spin.value(),
            umap_min_dist=self.umap_min_dist_spin.value(),
            umap_metric=self.umap_metric_combo.currentText(),
            hdbscan_min_cluster_size=self.hdbscan_min_cluster_spin.value(),
            hdbscan_min_samples=self.hdbscan_min_samples_spin.value(),
            hdbscan_metric=self.hdbscan_metric_combo.currentText(),
            top_n_words=self.top_n_words_spin.value(),
            min_topic_size=self.min_topic_size_spin.value(),
            nr_topics=self.nr_topics_spin.value() if self.nr_topics_spin.value() > 0 else None,
            calculate_probabilities=self.calc_probs_cb.isChecked(),
        )

        # Create topic analyzer
        self.topic_analyzer = TopicAnalyzer(model_manager=self.model_manager)

        # Start training worker
        self.worker = BertopicWorker(
            documents=documents,
            topic_analyzer=self.topic_analyzer,
            params=params,
        )
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        # Connect signals
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.on_status_change)
        self.worker.finished.connect(self.on_training_finished)
        self.worker.error.connect(self.on_training_error)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)

        # Update UI
        self.train_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.results_text.clear()
        self.results_text.append("训练开始...\n")

        # Start
        self.worker_thread.start()
        self.logger.info("BERTopic training started")

    def update_progress(self, value: int):
        """Update progress bar."""
        self.progress_bar.setValue(value)

    def on_training_finished(self, result):
        """Handle training completion."""
        self.progress_bar.setVisible(False)
        self.train_btn.setEnabled(True)
        self.save_model_btn.setEnabled(True)

        # Get results
        topics = result['topics']
        topic_analyzer = result['topic_analyzer']

        # Display results
        topic_info = topic_analyzer.get_topic_info()

        if topic_info is not None:
            num_topics = len(topic_info) - 1  # Exclude outlier topic (-1)

            self.results_text.append(f"\n训练完成！\n")
            self.results_text.append(f"发现主题数: {num_topics}\n")
            self.results_text.append(f"总文档数: {len(topics)}\n")
            self.results_text.append(f"\n主题信息:\n")
            self.results_text.append("=" * 60 + "\n")

            # Show top topics
            for idx, row in topic_info.head(10).iterrows():
                topic_id = row['Topic']
                count = row['Count']
                words = row['Name']

                self.results_text.append(f"\n主题 {topic_id}: ({count} 文档)\n")
                self.results_text.append(f"  {words}\n")

        # Emit signal
        self.model_trained.emit(result)

        QMessageBox.information(self, "训练完成", f"成功训练 BERTopic 模型！\n发现 {num_topics} 个主题")
        self.logger.info("BERTopic training completed")

    def on_training_error(self, error):
        """Handle training error."""
        self.progress_bar.setVisible(False)
        self.train_btn.setEnabled(True)

        self.results_text.append(f"\n训练失败: {str(error)}\n")

        QMessageBox.critical(self, "训练失败", f"训练过程出错:\n{str(error)}")
        self.error_occurred.emit(str(error))

    def save_model(self):
        """Save trained model."""
        if self.topic_analyzer is None or self.topic_analyzer.model is None:
            QMessageBox.warning(self, "错误", "没有可保存的模型")
            return

        # Ask for save path
        default_name = f"bertopic_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        name, ok = QInputDialog.getText(
            self,
            "保存模型",
            "输入模型名称:",
            text=default_name,
        )

        if ok and name:
            try:
                model_path = self.topic_analyzer.save_model(name=name)
                QMessageBox.information(self, "保存成功", f"模型已保存到:\n{model_path}")
                self.logger.info(f"Model saved: {model_path}")

            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"无法保存模型:\n{str(e)}")
                self.error_occurred.emit(str(e))

    def load_model(self):
        """Load saved model."""
        model_dir = QFileDialog.getExistingDirectory(
            self,
            "选择模型目录",
            str(config.MODEL_DIR / 'bertopic'),
        )

        if model_dir:
            try:
                self.topic_analyzer = TopicAnalyzer(model_manager=self.model_manager)
                self.topic_analyzer.load_model(Path(model_dir))

                # Display loaded model info
                topic_info = self.topic_analyzer.get_topic_info()

                if topic_info is not None:
                    num_topics = len(topic_info) - 1

                    self.results_text.clear()
                    self.results_text.append(f"模型加载成功！\n")
                    self.results_text.append(f"主题数: {num_topics}\n")

                self.save_model_btn.setEnabled(True)

                QMessageBox.information(self, "加载成功", f"模型已加载:\n{Path(model_dir).name}")
                self.logger.info(f"Model loaded: {model_dir}")

            except Exception as e:
                QMessageBox.critical(self, "加载失败", f"无法加载模型:\n{str(e)}")
                self.error_occurred.emit(str(e))
