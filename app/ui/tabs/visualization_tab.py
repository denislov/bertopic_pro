"""
BERTopic Pro - Visualization Tab
Tab 3: Interactive visualization generation with Plotly and QWebEngineView.
"""

from pathlib import Path
from typing import Optional, Dict, Any
import tempfile

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QGroupBox,
    QListWidget, QListWidgetItem, QMessageBox,
    QSplitter, QWidget, QComboBox,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

from app.ui.tabs.base_tab import BaseTab
from app.core.visualization_generator import VisualizationGenerator
from app.core.topic_analyzer import TopicAnalyzer
import config


class VisualizationTab(BaseTab):
    """Tab for BERTopic visualization."""

    def setup_ui(self):
        """Set up the UI for this tab."""
        main_layout = QVBoxLayout(self)

        # Title
        title = QLabel("3. 可视化生成")
        title.setProperty("class", "title")
        main_layout.addWidget(title)

        # Main splitter (left: controls, right: visualization)
        splitter = QSplitter(Qt.Horizontal)

        # Left panel: Controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Visualization type selector
        viz_group = self.create_visualization_selector()
        left_layout.addWidget(viz_group)

        # Export controls
        export_group = self.create_export_controls()
        left_layout.addWidget(export_group)

        left_layout.addStretch()

        # Set fixed width for left panel
        left_widget.setMaximumWidth(300)

        splitter.addWidget(left_widget)

        # Right panel: Web view
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Info label
        self.info_label = QLabel("请在建模完成后选择可视化类型")
        self.info_label.setProperty("class", "hint")
        self.info_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.info_label)

        # Web view for Plotly
        self.web_view = QWebEngineView()
        self.web_view.setVisible(False)
        right_layout.addWidget(self.web_view)

        splitter.addWidget(right_widget)

        # Set splitter sizes
        splitter.setSizes([300, 900])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # State variables
        self.topic_analyzer: Optional[TopicAnalyzer] = None
        self.viz_generator: Optional[VisualizationGenerator] = None
        self.current_figure = None
        self.current_viz_id: Optional[str] = None

    def create_visualization_selector(self) -> QGroupBox:
        """Create visualization type selector."""
        group = QGroupBox("可视化类型")
        layout = QVBoxLayout()

        # List of visualization types
        self.viz_list = QListWidget()
        self.viz_list.setSelectionMode(QListWidget.SingleSelection)
        self.viz_list.itemClicked.connect(self.on_visualization_selected)

        # Add placeholder items (will be populated when model is loaded)
        placeholder_item = QListWidgetItem("(请先训练模型)")
        placeholder_item.setFlags(Qt.NoItemFlags)
        self.viz_list.addItem(placeholder_item)

        layout.addWidget(self.viz_list)

        # Generate button
        self.generate_btn = QPushButton("生成可视化")
        self.generate_btn.setEnabled(False)
        self.generate_btn.clicked.connect(self.generate_visualization)
        layout.addWidget(self.generate_btn)

        group.setLayout(layout)
        return group

    def create_export_controls(self) -> QGroupBox:
        """Create export controls."""
        group = QGroupBox("导出")
        layout = QVBoxLayout()

        # Export format selector
        layout.addWidget(QLabel("导出格式:"))
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["HTML", "PNG (需要 kaleido)"])
        layout.addWidget(self.export_format_combo)

        # Export button
        self.export_btn = QPushButton("导出图表")
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.export_visualization)
        layout.addWidget(self.export_btn)

        group.setLayout(layout)
        return group

    def set_topic_analyzer(self, topic_analyzer: TopicAnalyzer):
        """
        Set topic analyzer from modeling tab.

        Args:
            topic_analyzer: Trained TopicAnalyzer instance
        """
        try:
            self.topic_analyzer = topic_analyzer

            # Create visualization generator
            self.viz_generator = VisualizationGenerator(topic_analyzer)

            # Populate visualization list
            self.populate_visualization_list()

            # Enable controls
            self.generate_btn.setEnabled(True)

            # Update info
            self.info_label.setText("请选择可视化类型")

            self.logger.info("Topic analyzer set, visualization generator ready")

        except Exception as e:
            self.logger.error(f"Failed to set topic analyzer: {e}")
            QMessageBox.critical(self, "错误", f"无法初始化可视化生成器:\n{str(e)}")

    def populate_visualization_list(self):
        """Populate visualization list with available types."""
        if self.viz_generator is None:
            return

        # Clear existing items
        self.viz_list.clear()

        # Get available visualizations
        visualizations = self.viz_generator.get_available_visualizations()

        # Add items
        for viz in visualizations:
            item = QListWidgetItem(viz['name'])
            item.setToolTip(viz['description'])
            item.setData(Qt.UserRole, viz['id'])
            self.viz_list.addItem(item)

        self.logger.info(f"Populated {len(visualizations)} visualization types")

    def on_visualization_selected(self, item: QListWidgetItem):
        """Handle visualization selection."""
        viz_id = item.data(Qt.UserRole)

        if viz_id:
            self.current_viz_id = viz_id
            self.info_label.setText(f"已选择: {item.text()}\n{item.toolTip()}")
            self.generate_btn.setEnabled(True)
            self.logger.info(f"Selected visualization: {viz_id}")

    def generate_visualization(self):
        """Generate selected visualization."""
        if self.viz_generator is None or self.current_viz_id is None:
            QMessageBox.warning(self, "错误", "请先选择可视化类型")
            return

        try:
            self.info_label.setText("正在生成可视化...")
            self.generate_btn.setEnabled(False)

            # Generate figure based on type
            if self.current_viz_id == "topics":
                fig = self.viz_generator.visualize_topics()

            elif self.current_viz_id == "hierarchy":
                fig = self.viz_generator.visualize_hierarchy()

            elif self.current_viz_id == "barchart":
                fig = self.viz_generator.visualize_barchart()

            elif self.current_viz_id == "documents":
                # Sample 20% for performance
                fig = self.viz_generator.visualize_documents(sample=0.2)

            elif self.current_viz_id == "heatmap":
                fig = self.viz_generator.visualize_heatmap()

            elif self.current_viz_id == "term_rank":
                fig = self.viz_generator.visualize_term_rank()

            elif self.current_viz_id == "topics_over_time":
                # TODO: Need to compute topics_over_time first
                QMessageBox.information(
                    self,
                    "功能提示",
                    "主题时间演化需要时间戳数据。\n请在数据预处理时选择时间戳列。"
                )
                self.generate_btn.setEnabled(True)
                return

            else:
                raise ValueError(f"Unknown visualization type: {self.current_viz_id}")

            # Store current figure
            self.current_figure = fig

            # Display in web view
            self.display_figure(fig)

            # Enable export
            self.export_btn.setEnabled(True)

            self.info_label.setText("可视化生成完成")
            self.generate_btn.setEnabled(True)

            self.logger.info(f"Visualization generated: {self.current_viz_id}")

        except Exception as e:
            self.logger.error(f"Failed to generate visualization: {e}")
            QMessageBox.critical(self, "生成失败", f"无法生成可视化:\n{str(e)}")
            self.generate_btn.setEnabled(True)
            self.info_label.setText("生成失败，请重试")

    def display_figure(self, fig):
        """
        Display Plotly figure in web view.

        Args:
            fig: Plotly figure
        """
        try:
            # Create temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                html_content = fig.to_html(
                    include_plotlyjs='cdn',
                    config={
                        'displayModeBar': True,
                        'responsive': True,
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': 'bertopic_visualization',
                            'height': 800,
                            'width': 1000,
                            'scale': 2,
                        },
                    },
                )

                f.write(html_content)
                temp_path = f.name

            # Load in web view
            self.web_view.setUrl(QUrl.fromLocalFile(temp_path))
            self.web_view.setVisible(True)
            self.info_label.setVisible(False)

            self.logger.info(f"Figure displayed in web view: {temp_path}")

        except Exception as e:
            self.logger.error(f"Failed to display figure: {e}")
            raise

    def export_visualization(self):
        """Export current visualization."""
        if self.current_figure is None:
            QMessageBox.warning(self, "错误", "没有可导出的可视化")
            return

        # Get export format
        format_text = self.export_format_combo.currentText()

        if format_text.startswith("HTML"):
            file_filter = "HTML Files (*.html)"
            default_ext = "html"
            export_format = "html"

        elif format_text.startswith("PNG"):
            file_filter = "PNG Files (*.png)"
            default_ext = "png"
            export_format = "png"

        else:
            QMessageBox.warning(self, "错误", "不支持的导出格式")
            return

        # Ask for save path
        default_name = f"bertopic_{self.current_viz_id}.{default_ext}"
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "导出可视化",
            str(config.CACHE_DIR / default_name),
            file_filter,
        )

        if filepath:
            try:
                # Save figure
                self.viz_generator.save_figure(
                    self.current_figure,
                    Path(filepath),
                    format=export_format,
                )

                QMessageBox.information(self, "导出成功", f"可视化已导出到:\n{filepath}")
                self.logger.info(f"Visualization exported: {filepath}")

            except Exception as e:
                self.logger.error(f"Failed to export visualization: {e}")

                # Check if it's kaleido error
                if "kaleido" in str(e).lower():
                    QMessageBox.critical(
                        self,
                        "导出失败",
                        f"PNG 导出需要安装 kaleido 库:\n\npip install kaleido\n\n错误: {str(e)}"
                    )
                else:
                    QMessageBox.critical(self, "导出失败", f"无法导出可视化:\n{str(e)}")

    def cleanup(self):
        """Clean up resources."""
        # Clear web view
        if self.web_view:
            self.web_view.setHtml("")

        super().cleanup()

