# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Home.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QSizePolicy, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_Home(object):
    def setupUi(self, Home):
        if not Home.objectName():
            Home.setObjectName(u"Home")
        Home.resize(800, 600)
        self.actionShow_Console = QAction(Home)
        self.actionShow_Console.setObjectName(u"actionShow_Console")
        self.actionShow_Console.setCheckable(True)
        self.actionShow_Console.setChecked(True)
        self.actionOpen = QAction(Home)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionQuit = QAction(Home)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionClear_Console = QAction(Home)
        self.actionClear_Console.setObjectName(u"actionClear_Console")
        self.actionAbout = QAction(Home)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionNone = QAction(Home)
        self.actionNone.setObjectName(u"actionNone")
        self.centralwidget = QWidget(Home)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")

        self.verticalLayout.addWidget(self.tabWidget)

        self.logConsole = QPlainTextEdit(self.centralwidget)
        self.logConsole.setObjectName(u"logConsole")
        self.logConsole.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.verticalLayout.addWidget(self.logConsole)

        self.verticalLayout.setStretch(0, 7)
        self.verticalLayout.setStretch(1, 3)
        Home.setCentralWidget(self.centralwidget)
        self.logConsole.raise_()
        self.tabWidget.raise_()
        self.menubar = QMenuBar(Home)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menuRecent = QMenu(self.menu)
        self.menuRecent.setObjectName(u"menuRecent")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        Home.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Home)
        self.statusbar.setObjectName(u"statusbar")
        Home.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.menuRecent.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.actionQuit)
        self.menuRecent.addAction(self.actionNone)
        self.menu_2.addAction(self.actionShow_Console)
        self.menu_2.addAction(self.actionClear_Console)
        self.menu_3.addAction(self.actionAbout)

        self.retranslateUi(Home)
        self.actionShow_Console.triggered["bool"].connect(self.logConsole.setVisible)
        self.actionClear_Console.triggered.connect(self.logConsole.clear)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Home)
    # setupUi

    def retranslateUi(self, Home):
        Home.setWindowTitle(QCoreApplication.translate("Home", u"MainWindow", None))
        self.actionShow_Console.setText(QCoreApplication.translate("Home", u"Show Console", None))
        self.actionOpen.setText(QCoreApplication.translate("Home", u"\u6253\u5f00\u6570\u636e\u6587\u4ef6...", None))
        self.actionQuit.setText(QCoreApplication.translate("Home", u"\u9000\u51fa", None))
        self.actionClear_Console.setText(QCoreApplication.translate("Home", u"Clear Console", None))
        self.actionAbout.setText(QCoreApplication.translate("Home", u"\u5173\u4e8e", None))
        self.actionNone.setText(QCoreApplication.translate("Home", u"None", None))
        self.menu.setTitle(QCoreApplication.translate("Home", u"\u6587\u4ef6", None))
        self.menuRecent.setTitle(QCoreApplication.translate("Home", u"\u6700\u8fd1\u6253\u5f00", None))
        self.menu_2.setTitle(QCoreApplication.translate("Home", u"\u89c6\u56fe", None))
        self.menu_3.setTitle(QCoreApplication.translate("Home", u"\u5e2e\u52a9", None))
    # retranslateUi

