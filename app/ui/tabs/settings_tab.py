"""
BERTopic Pro - Settings Tab
Tab 4: System settings, LLM configuration, and model repository management.
"""

from pathlib import Path
from typing import Optional, List
import os

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFileDialog, QGroupBox,
    QLineEdit, QComboBox, QCheckBox, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QScrollArea, QWidget, QTabWidget,
)
from PySide6.QtCore import Qt

from app.ui.tabs.base_tab import BaseTab
from app.core.model_manager import ModelManager
from app.utils.config_manager import get_config_manager
import config


class SettingsTab(BaseTab):
    """Tab for system settings and configuration."""

    def setup_ui(self):
        """Set up the UI for this tab."""
        main_layout = QVBoxLayout(self)

        # Create tab widget for different setting categories
        self.settings_tabs = QTabWidget()

        # Initialize state
        self.config_manager = get_config_manager()
        self.model_manager = ModelManager()
        
        # Create setting pages
        self.create_model_repository_page()
        self.create_llm_config_page()
        self.create_hardware_page()
        self.create_paths_page()

        main_layout.addWidget(self.settings_tabs)

        # Bottom buttons
        button_layout = QHBoxLayout()

        self.save_btn = QPushButton("保存设置")
        self.save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("重置为默认")
        self.reset_btn.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_btn)

        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        

        # Load current settings
        self.load_settings()

    def create_model_repository_page(self):
        """Create model repository management page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Description
        desc = QLabel("管理已缓存的嵌入模型")
        layout.addWidget(desc)

        # Model table
        self.model_table = QTableWidget()
        self.model_table.setColumnCount(4)
        self.model_table.setHorizontalHeaderLabels([
            "模型名称", "大小 (MB)", "下载日期", "操作"
        ])
        self.model_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.model_table.setAlternatingRowColors(True)
        layout.addWidget(self.model_table)

        # Refresh and clear buttons
        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("刷新列表")
        refresh_btn.clicked.connect(self.refresh_model_list)
        button_layout.addWidget(refresh_btn)

        clear_cache_btn = QPushButton("清空缓存")
        clear_cache_btn.clicked.connect(self.clear_model_cache)
        button_layout.addWidget(clear_cache_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Add to tabs
        self.settings_tabs.addTab(page, "模型仓库")

    def create_llm_config_page(self):
        """Create LLM configuration page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Scroll area for long content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Description
        desc = QLabel("配置 LLM 用于主题标签生成和表示学习")
        scroll_layout.addWidget(desc)

        # OpenAI configuration
        openai_group = QGroupBox("OpenAI 配置")
        openai_layout = QGridLayout()

        openai_layout.addWidget(QLabel("API Key:"), 0, 0)
        self.openai_api_key_input = QLineEdit()
        self.openai_api_key_input.setEchoMode(QLineEdit.Password)
        self.openai_api_key_input.setPlaceholderText("sk-...")
        openai_layout.addWidget(self.openai_api_key_input, 0, 1)

        show_openai_btn = QPushButton("显示")
        show_openai_btn.setMaximumWidth(60)
        show_openai_btn.clicked.connect(
            lambda: self.toggle_password_visibility(self.openai_api_key_input)
        )
        openai_layout.addWidget(show_openai_btn, 0, 2)

        openai_layout.addWidget(QLabel("模型:"), 1, 0)
        self.openai_model_combo = QComboBox()
        self.openai_model_combo.addItems([
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
        ])
        openai_layout.addWidget(self.openai_model_combo, 1, 1, 1, 2)

        openai_group.setLayout(openai_layout)
        scroll_layout.addWidget(openai_group)

        # Ollama configuration
        ollama_group = QGroupBox("Ollama 配置（本地 LLM）")
        ollama_layout = QGridLayout()

        ollama_layout.addWidget(QLabel("Base URL:"), 0, 0)
        self.ollama_base_url_input = QLineEdit()
        self.ollama_base_url_input.setPlaceholderText("http://localhost:11434")
        ollama_layout.addWidget(self.ollama_base_url_input, 0, 1)

        ollama_layout.addWidget(QLabel("模型:"), 1, 0)
        self.ollama_model_input = QLineEdit()
        self.ollama_model_input.setPlaceholderText("llama2, mistral, etc.")
        ollama_layout.addWidget(self.ollama_model_input, 1, 1)

        test_ollama_btn = QPushButton("测试连接")
        test_ollama_btn.clicked.connect(self.test_ollama_connection)
        ollama_layout.addWidget(test_ollama_btn, 2, 0, 1, 2)

        ollama_group.setLayout(ollama_layout)
        scroll_layout.addWidget(ollama_group)

        # Zhipu AI configuration
        zhipu_group = QGroupBox("Zhipu AI 配置")
        zhipu_layout = QGridLayout()

        zhipu_layout.addWidget(QLabel("API Key:"), 0, 0)
        self.zhipu_api_key_input = QLineEdit()
        self.zhipu_api_key_input.setEchoMode(QLineEdit.Password)
        self.zhipu_api_key_input.setPlaceholderText("...")
        zhipu_layout.addWidget(self.zhipu_api_key_input, 0, 1)

        show_zhipu_btn = QPushButton("显示")
        show_zhipu_btn.setMaximumWidth(60)
        show_zhipu_btn.clicked.connect(
            lambda: self.toggle_password_visibility(self.zhipu_api_key_input)
        )
        zhipu_layout.addWidget(show_zhipu_btn, 0, 2)

        zhipu_layout.addWidget(QLabel("模型:"), 1, 0)
        self.zhipu_model_combo = QComboBox()
        self.zhipu_model_combo.addItems([
            "glm-4",
            "glm-3-turbo",
        ])
        zhipu_layout.addWidget(self.zhipu_model_combo, 1, 1, 1, 2)

        zhipu_group.setLayout(zhipu_layout)
        scroll_layout.addWidget(zhipu_group)

        # LLM provider selection
        provider_group = QGroupBox("默认 LLM 提供商")
        provider_layout = QVBoxLayout()

        self.llm_provider_combo = QComboBox()
        self.llm_provider_combo.addItems(["无", "OpenAI", "Ollama", "Zhipu AI"])
        provider_layout.addWidget(self.llm_provider_combo)

        hint = QLabel("选择 LLM 提供商用于主题标签生成")
        provider_layout.addWidget(hint)

        provider_group.setLayout(provider_layout)
        scroll_layout.addWidget(provider_group)

        scroll_layout.addStretch()

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Add to tabs
        self.settings_tabs.addTab(page, "LLM 配置")

    def create_hardware_page(self):
        """Create hardware settings page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Description
        desc = QLabel("配置硬件和设备选项")
        layout.addWidget(desc)

        # Device selection
        device_group = QGroupBox("计算设备")
        device_layout = QVBoxLayout()

        self.device_combo = QComboBox()
        self.device_combo.addItems(["自动检测", "CPU", "CUDA"])
        device_layout.addWidget(self.device_combo)

        # Device info
        self.device_info_label = QLabel()
        device_layout.addWidget(self.device_info_label)

        # Update device info
        self.update_device_info()

        device_group.setLayout(device_layout)
        layout.addWidget(device_group)

        # Performance settings
        perf_group = QGroupBox("性能设置")
        perf_layout = QGridLayout()

        perf_layout.addWidget(QLabel("Jieba 并行进程数:"), 0, 0)
        self.jieba_processes_combo = QComboBox()
        self.jieba_processes_combo.addItems(["1", "2", "4", "8"])
        self.jieba_processes_combo.setCurrentText(str(config.JIEBA_PARALLEL_PROCESSES))
        perf_layout.addWidget(self.jieba_processes_combo, 0, 1)

        self.jieba_parallel_cb = QCheckBox("启用 Jieba 并行模式")
        self.jieba_parallel_cb.setChecked(config.JIEBA_PARALLEL_MODE)
        perf_layout.addWidget(self.jieba_parallel_cb, 1, 0, 1, 2)

        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)

        layout.addStretch()

        # Add to tabs
        self.settings_tabs.addTab(page, "硬件设置")

    def create_paths_page(self):
        """Create paths configuration page."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Description
        desc = QLabel("配置数据和模型存储路径")
        layout.addWidget(desc)

        # Paths group
        paths_group = QGroupBox("目录路径")
        paths_layout = QGridLayout()

        # Data directory
        paths_layout.addWidget(QLabel("数据目录:"), 0, 0)
        self.data_dir_input = QLineEdit()
        self.data_dir_input.setText(str(config.DATA_DIR))
        paths_layout.addWidget(self.data_dir_input, 0, 1)

        browse_data_btn = QPushButton("浏览...")
        browse_data_btn.clicked.connect(
            lambda: self.browse_directory(self.data_dir_input)
        )
        paths_layout.addWidget(browse_data_btn, 0, 2)

        # Model directory
        paths_layout.addWidget(QLabel("模型目录:"), 1, 0)
        self.model_dir_input = QLineEdit()
        self.model_dir_input.setText(str(config.MODEL_DIR))
        paths_layout.addWidget(self.model_dir_input, 1, 1)

        browse_model_btn = QPushButton("浏览...")
        browse_model_btn.clicked.connect(
            lambda: self.browse_directory(self.model_dir_input)
        )
        paths_layout.addWidget(browse_model_btn, 1, 2)

        # Logs directory
        paths_layout.addWidget(QLabel("日志目录:"), 2, 0)
        self.logs_dir_input = QLineEdit()
        self.logs_dir_input.setText(str(config.LOGS_DIR))
        paths_layout.addWidget(self.logs_dir_input, 2, 1)

        browse_logs_btn = QPushButton("浏览...")
        browse_logs_btn.clicked.connect(
            lambda: self.browse_directory(self.logs_dir_input)
        )
        paths_layout.addWidget(browse_logs_btn, 2, 2)

        paths_group.setLayout(paths_layout)
        layout.addWidget(paths_group)

        # Warning label
        warning = QLabel("⚠️ 修改路径后需要重启应用才能生效")
        layout.addWidget(warning)

        layout.addStretch()

        # Add to tabs
        self.settings_tabs.addTab(page, "路径配置")

    def refresh_model_list(self):
        """Refresh model repository list."""
        try:
            models = self.model_manager.list_models()

            self.model_table.setRowCount(len(models))

            for i, model in enumerate(models):
                # Model name
                name_item = QTableWidgetItem(model.model_name)
                self.model_table.setItem(i, 0, name_item)

                # Size
                size_item = QTableWidgetItem(f"{model.size_mb:.1f}")
                self.model_table.setItem(i, 1, size_item)

                # Download date
                date_str = model.download_date or "未知"
                if model.download_date:
                    from datetime import datetime
                    try:
                        dt = datetime.fromisoformat(model.download_date)
                        date_str = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass

                date_item = QTableWidgetItem(date_str)
                self.model_table.setItem(i, 2, date_item)

                # Delete button
                delete_btn = QPushButton("删除")
                delete_btn.clicked.connect(
                    lambda checked, name=model.model_name: self.delete_model(name)
                )
                self.model_table.setCellWidget(i, 3, delete_btn)

            self.logger.info(f"Refreshed model list: {len(models)} models")

        except Exception as e:
            self.logger.error(f"Failed to refresh model list: {e}")
            QMessageBox.critical(self, "错误", f"无法刷新模型列表:\n{str(e)}")

    def delete_model(self, model_name: str):
        """Delete a cached model."""
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除模型 '{model_name}' 吗？\n此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                success = self.model_manager.delete_model(model_name)

                if success:
                    QMessageBox.information(self, "删除成功", f"模型 '{model_name}' 已删除")
                    self.refresh_model_list()
                else:
                    QMessageBox.warning(self, "删除失败", f"无法删除模型 '{model_name}'")

            except Exception as e:
                self.logger.error(f"Failed to delete model: {e}")
                QMessageBox.critical(self, "删除失败", f"删除模型时出错:\n{str(e)}")

    def clear_model_cache(self):
        """Clear all cached models."""
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有缓存的模型吗？\n此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                success = self.model_manager.clear_cache()

                if success:
                    QMessageBox.information(self, "清空成功", "所有缓存的模型已删除")
                    self.refresh_model_list()
                else:
                    QMessageBox.warning(self, "清空失败", "无法清空模型缓存")

            except Exception as e:
                self.logger.error(f"Failed to clear cache: {e}")
                QMessageBox.critical(self, "清空失败", f"清空缓存时出错:\n{str(e)}")

    def toggle_password_visibility(self, line_edit: QLineEdit):
        """Toggle password visibility."""
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)

    def test_ollama_connection(self):
        """Test Ollama connection."""
        base_url = self.ollama_base_url_input.text().strip()

        if not base_url:
            QMessageBox.warning(self, "错误", "请输入 Ollama Base URL")
            return

        try:
            import requests
            response = requests.get(f"{base_url}/api/tags", timeout=5)

            if response.status_code == 200:
                QMessageBox.information(
                    self,
                    "连接成功",
                    f"成功连接到 Ollama 服务器\n{base_url}"
                )
            else:
                QMessageBox.warning(
                    self,
                    "连接失败",
                    f"无法连接到 Ollama 服务器\n状态码: {response.status_code}"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "连接失败",
                f"无法连接到 Ollama 服务器:\n{str(e)}\n\n请确保 Ollama 正在运行。"
            )

    def update_device_info(self):
        """Update device information display."""
        device_info = self.model_manager.get_device_info()

        info_text = f"当前设备: {device_info['device'].upper()}\n"
        info_text += f"CUDA 可用: {'是' if device_info['cuda_available'] else '否'}"

        if device_info['cuda_available']:
            info_text += f"\nGPU: {device_info.get('cuda_device_name', 'Unknown')}"
            info_text += f"\n显存: {device_info.get('cuda_memory_total', 0):.1f} GB"

        self.device_info_label.setText(info_text)

    def browse_directory(self, line_edit: QLineEdit):
        """Browse for directory."""
        current_path = line_edit.text()
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择目录",
            current_path,
        )

        if directory:
            line_edit.setText(directory)

    def load_settings(self):
        """Load current settings from config."""
        try:
            # Load LLM settings
            openai_key = self.config_manager.get("openai_api_key", "")
            if openai_key:
                self.openai_api_key_input.setText(openai_key)

            openai_model = self.config_manager.get("openai_model", config.OPENAI_DEFAULT_MODEL)
            index = self.openai_model_combo.findText(openai_model)
            if index >= 0:
                self.openai_model_combo.setCurrentIndex(index)

            ollama_url = self.config_manager.get("ollama_base_url", config.OLLAMA_BASE_URL)
            self.ollama_base_url_input.setText(ollama_url)

            ollama_model = self.config_manager.get("ollama_model", config.OLLAMA_DEFAULT_MODEL)
            self.ollama_model_input.setText(ollama_model)

            zhipu_key = self.config_manager.get("zhipu_api_key", "")
            if zhipu_key:
                self.zhipu_api_key_input.setText(zhipu_key)

            zhipu_model = self.config_manager.get("zhipu_model", config.ZHIPU_DEFAULT_MODEL)
            index = self.zhipu_model_combo.findText(zhipu_model)
            if index >= 0:
                self.zhipu_model_combo.setCurrentIndex(index)

            llm_provider = self.config_manager.get("llm_provider", "无")
            index = self.llm_provider_combo.findText(llm_provider)
            if index >= 0:
                self.llm_provider_combo.setCurrentIndex(index)

            # Load hardware settings
            device = self.config_manager.get("device", "自动检测")
            index = self.device_combo.findText(device)
            if index >= 0:
                self.device_combo.setCurrentIndex(index)

            # Refresh model list
            self.refresh_model_list()

            self.logger.info("Settings loaded successfully")

        except Exception as e:
            self.logger.error(f"Failed to load settings: {e}")

    def save_settings(self):
        """Save current settings to config."""
        try:
            # Save LLM settings
            self.config_manager.set("openai_api_key", self.openai_api_key_input.text())
            self.config_manager.set("openai_model", self.openai_model_combo.currentText())

            self.config_manager.set("ollama_base_url", self.ollama_base_url_input.text())
            self.config_manager.set("ollama_model", self.ollama_model_input.text())

            self.config_manager.set("zhipu_api_key", self.zhipu_api_key_input.text())
            self.config_manager.set("zhipu_model", self.zhipu_model_combo.currentText())

            self.config_manager.set("llm_provider", self.llm_provider_combo.currentText())

            # Save hardware settings
            self.config_manager.set("device", self.device_combo.currentText())

            # Save paths (note: requires restart)
            self.config_manager.set("data_dir", self.data_dir_input.text())
            self.config_manager.set("model_dir", self.model_dir_input.text())
            self.config_manager.set("logs_dir", self.logs_dir_input.text())

            # Commit changes
            self.config_manager.save()

            QMessageBox.information(self, "保存成功", "设置已保存")
            self.logger.info("Settings saved successfully")

        except Exception as e:
            self.logger.error(f"Failed to save settings: {e}")
            QMessageBox.critical(self, "保存失败", f"无法保存设置:\n{str(e)}")

    def reset_settings(self):
        """Reset settings to defaults."""
        reply = QMessageBox.question(
            self,
            "确认重置",
            "确定要重置所有设置为默认值吗？",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                # Clear all settings
                self.openai_api_key_input.clear()
                self.openai_model_combo.setCurrentText(config.OPENAI_DEFAULT_MODEL)

                self.ollama_base_url_input.setText(config.OLLAMA_BASE_URL)
                self.ollama_model_input.setText(config.OLLAMA_DEFAULT_MODEL)

                self.zhipu_api_key_input.clear()
                self.zhipu_model_combo.setCurrentText(config.ZHIPU_DEFAULT_MODEL)

                self.llm_provider_combo.setCurrentText("无")

                self.device_combo.setCurrentText("自动检测")

                self.data_dir_input.setText(str(config.DATA_DIR))
                self.model_dir_input.setText(str(config.MODEL_DIR))
                self.logs_dir_input.setText(str(config.LOGS_DIR))

                QMessageBox.information(self, "重置成功", "设置已重置为默认值")
                self.logger.info("Settings reset to defaults")

            except Exception as e:
                self.logger.error(f"Failed to reset settings: {e}")
                QMessageBox.critical(self, "重置失败", f"无法重置设置:\n{str(e)}")
