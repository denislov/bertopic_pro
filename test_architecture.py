#!/usr/bin/env python
"""
BERTopic Pro - 架构验证测试
在无头环境中测试应用架构，无需实际显示 GUI
"""

import sys
import os

# 设置 Qt 使用 offscreen 平台插件
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

print("=" * 60)
print("BERTopic Pro 架构验证测试")
print("=" * 60)

# 1. 测试配置加载
print("\n[1/7] 测试配置系统...")
try:
    import config
    assert config.APP_NAME == "BERTopic Pro"
    assert config.APP_VERSION == "0.1.0"
    print(f"  ✓ 配置加载成功")
    print(f"    - APP_NAME: {config.APP_NAME}")
    print(f"    - VERSION: {config.APP_VERSION}")
    print(f"    - DEVICE: {config.DEFAULT_DEVICE}")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    sys.exit(1)

# 2. 测试日志系统
print("\n[2/7] 测试日志系统...")
try:
    from app.utils.logger import get_logger, setup_logging
    logger = get_logger("test")
    logger.info("日志系统测试")
    print(f"  ✓ 日志系统初始化成功")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    sys.exit(1)

# 3. 测试配置管理器
print("\n[3/7] 测试配置管理器...")
try:
    from app.utils.config_manager import get_config_manager
    cm = get_config_manager()
    cm.set("test_key", "test_value")
    value = cm.get("test_key")
    assert value == "test_value"
    print(f"  ✓ 配置管理器工作正常")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    sys.exit(1)

# 4. 测试基础类
print("\n[4/7] 测试基础抽象类...")
try:
    from app.ui.tabs.base_tab import BaseTab
    from app.core.workers.base_worker import BaseWorker
    print(f"  ✓ BaseTab 加载成功")
    print(f"  ✓ BaseWorker 加载成功")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    sys.exit(1)

# 5. 测试所有 Tab 模块
print("\n[5/7] 测试 Tab 模块...")
try:
    from app.ui.tabs.preprocess_tab import PreprocessTab
    from app.ui.tabs.modeling_tab import ModelingTab
    from app.ui.tabs.visualization_tab import VisualizationTab
    from app.ui.tabs.settings_tab import SettingsTab
    print(f"  ✓ PreprocessTab 加载成功")
    print(f"  ✓ ModelingTab 加载成功")
    print(f"  ✓ VisualizationTab 加载成功")
    print(f"  ✓ SettingsTab 加载成功")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    sys.exit(1)

# 6. 测试主窗口类（不实例化）
print("\n[6/7] 测试主窗口类...")
try:
    from app.ui.main_window import MainWindow
    print(f"  ✓ MainWindow 类加载成功")
except Exception as e:
    print(f"  ✗ 失败: {e}")
    sys.exit(1)

# 7. 测试 Qt 应用创建（offscreen 模式）
print("\n[7/7] 测试 Qt 应用初始化...")
try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt

    # 创建 offscreen 应用实例
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    print(f"  ✓ QApplication 创建成功")
    print(f"  ✓ 平台插件: {os.environ.get('QT_QPA_PLATFORM', 'default')}")

    # 不显示窗口，只测试创建
    # window = MainWindow()
    # print(f"  ✓ 主窗口实例化成功（offscreen 模式）")

except Exception as e:
    print(f"  ✗ 失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ 所有架构测试通过！")
print("=" * 60)
print("\n📝 说明:")
print("  - 所有核心模块导入成功")
print("  - 配置系统运行正常")
print("  - 日志系统工作正常")
print("  - Qt 框架初始化成功")
print("\n⚠️  注意:")
print("  当前在 offscreen 模式下测试")
print("  要显示 GUI，需要:")
print("  1. 本地开发环境（有显示器）")
print("  2. 或安装 Xvfb (虚拟显示)")
print("  3. 或通过 VNC/远程桌面连接")
print("\n🚀 架构验证完成，可以开始第二阶段开发！")
