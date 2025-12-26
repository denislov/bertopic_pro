# 这一行导入了 QApplication、QWidget 和 QLabel 类，它们是 PySide6 中用于创建应用程序和窗口组件的类。
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QGroupBox,
    QListWidget, QListWidgetItem, QMessageBox,
    QSplitter, QWidget, QComboBox,
)
from PySide6.QtCore import Qt, QUrl
import sys
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings

from PySide6 import QtCore, QtGui, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("空白测试模板")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self) -> None:
        """设置界面"""
        # 在此处编写设置UI的代码
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("这是一个空白测试模板")
        layout.addWidget(label)
        web_view = QWebEngineView()
        settings = web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        web_view.setUrl(QUrl.fromLocalFile(r"C:\Users\adrian\AppData\Local\Temp\tmpaggm21tg.html"))
        layout.addWidget(web_view)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())