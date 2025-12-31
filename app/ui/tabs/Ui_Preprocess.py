# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Tab1.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Preprocess(object):
    def setupUi(self, Preprocess):
        if not Preprocess.objectName():
            Preprocess.setObjectName(u"Preprocess")
        Preprocess.resize(626, 362)
        self.verticalLayout = QVBoxLayout(Preprocess)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(Preprocess)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.file_path_input = QLineEdit(self.groupBox)
        self.file_path_input.setObjectName(u"file_path_input")

        self.verticalLayout_2.addWidget(self.file_path_input)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)

        self.browse_btn = QPushButton(self.groupBox)
        self.browse_btn.setObjectName(u"browse_btn")

        self.horizontalLayout_8.addWidget(self.browse_btn)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.load_btn = QPushButton(self.groupBox)
        self.load_btn.setObjectName(u"load_btn")

        self.horizontalLayout_8.addWidget(self.load_btn)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.btnPreview = QPushButton(self.groupBox)
        self.btnPreview.setObjectName(u"btnPreview")

        self.horizontalLayout_8.addWidget(self.btnPreview)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.file_info_label = QLabel(self.groupBox)
        self.file_info_label.setObjectName(u"file_info_label")

        self.verticalLayout_2.addWidget(self.file_info_label)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Preprocess)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.text_column_combo = QComboBox(self.groupBox_2)
        self.text_column_combo.setObjectName(u"text_column_combo")

        self.horizontalLayout_3.addWidget(self.text_column_combo)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.timestamp_column_combo = QComboBox(self.groupBox_2)
        self.timestamp_column_combo.setObjectName(u"timestamp_column_combo")

        self.horizontalLayout_4.addWidget(self.timestamp_column_combo)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox_4 = QGroupBox(Preprocess)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.segment_cb = QCheckBox(self.groupBox_4)
        self.segment_cb.setObjectName(u"segment_cb")
        self.segment_cb.setChecked(True)

        self.horizontalLayout_6.addWidget(self.segment_cb)

        self.remove_punct_cb = QCheckBox(self.groupBox_4)
        self.remove_punct_cb.setObjectName(u"remove_punct_cb")

        self.horizontalLayout_6.addWidget(self.remove_punct_cb)

        self.remove_urls_cb = QCheckBox(self.groupBox_4)
        self.remove_urls_cb.setObjectName(u"remove_urls_cb")

        self.horizontalLayout_6.addWidget(self.remove_urls_cb)

        self.lowercase_cb = QCheckBox(self.groupBox_4)
        self.lowercase_cb.setObjectName(u"lowercase_cb")

        self.horizontalLayout_6.addWidget(self.lowercase_cb)

        self.remove_stopwords_cb = QCheckBox(self.groupBox_4)
        self.remove_stopwords_cb.setObjectName(u"remove_stopwords_cb")
        self.remove_stopwords_cb.setChecked(True)

        self.horizontalLayout_6.addWidget(self.remove_stopwords_cb)

        self.remove_emails_cb = QCheckBox(self.groupBox_4)
        self.remove_emails_cb.setObjectName(u"remove_emails_cb")

        self.horizontalLayout_6.addWidget(self.remove_emails_cb)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_5 = QGroupBox(Preprocess)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.groupBox_5)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.stopwords_input = QLineEdit(self.groupBox_5)
        self.stopwords_input.setObjectName(u"stopwords_input")

        self.horizontalLayout_5.addWidget(self.stopwords_input)

        self.browse_stop_btn = QPushButton(self.groupBox_5)
        self.browse_stop_btn.setObjectName(u"browse_stop_btn")
        self.browse_stop_btn.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.browse_stop_btn)

        self.label_4 = QLabel(self.groupBox_5)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.custom_dict_input = QLineEdit(self.groupBox_5)
        self.custom_dict_input.setObjectName(u"custom_dict_input")

        self.horizontalLayout_5.addWidget(self.custom_dict_input)

        self.browse_dict_btn = QPushButton(self.groupBox_5)
        self.browse_dict_btn.setObjectName(u"browse_dict_btn")
        self.browse_dict_btn.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_5.addWidget(self.browse_dict_btn)


        self.horizontalLayout_2.addWidget(self.groupBox_5)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.groupBox_3 = QGroupBox(Preprocess)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.btnSaveResults = QPushButton(self.groupBox_3)
        self.btnSaveResults.setObjectName(u"btnSaveResults")

        self.horizontalLayout_7.addWidget(self.btnSaveResults)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.btnStartProcess = QPushButton(self.groupBox_3)
        self.btnStartProcess.setObjectName(u"btnStartProcess")

        self.horizontalLayout_7.addWidget(self.btnStartProcess)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.verticalLayout.setStretch(0, 3)
        self.verticalLayout.setStretch(2, 3)

        self.retranslateUi(Preprocess)

        QMetaObject.connectSlotsByName(Preprocess)
    # setupUi

    def retranslateUi(self, Preprocess):
        Preprocess.setWindowTitle(QCoreApplication.translate("Preprocess", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Preprocess", u"\u6587\u4ef6\u5bfc\u5165", None))
        self.label.setText(QCoreApplication.translate("Preprocess", u"\u6587\u4ef6\u8def\u5f84\uff1a", None))
        self.file_path_input.setPlaceholderText(QCoreApplication.translate("Preprocess", u"\u9009\u62e9 CSV\u3001Excel \u6216 TXT \u6587\u4ef6...", None))
        self.browse_btn.setText(QCoreApplication.translate("Preprocess", u"\u5bfc\u5165", None))
        self.load_btn.setText(QCoreApplication.translate("Preprocess", u"\u52a0\u8f7d", None))
        self.btnPreview.setText(QCoreApplication.translate("Preprocess", u"\u9884\u89c8", None))
        self.file_info_label.setText(QCoreApplication.translate("Preprocess", u"\u672a\u52a0\u8f7d\u6570\u636e", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Preprocess", u"\u5217\u6620\u5c04", None))
        self.label_2.setText(QCoreApplication.translate("Preprocess", u"\u6587\u672c\u5217", None))
        self.text_column_combo.setCurrentText("")
        self.text_column_combo.setPlaceholderText(QCoreApplication.translate("Preprocess", u"\u9009\u62e9\u5217...", None))
        self.label_3.setText(QCoreApplication.translate("Preprocess", u"\u65f6\u95f4\u5217", None))
        self.timestamp_column_combo.setPlaceholderText(QCoreApplication.translate("Preprocess", u"(\u53ef\u9009)", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Preprocess", u"\u6587\u672c\u6e05\u6d17\u9009\u9879", None))
#if QT_CONFIG(tooltip)
        self.segment_cb.setToolTip(QCoreApplication.translate("Preprocess", u"\u4f7f\u7528 Jieba \u8fdb\u884c\u4e2d\u6587\u5206\u8bcd", None))
#endif // QT_CONFIG(tooltip)
        self.segment_cb.setText(QCoreApplication.translate("Preprocess", u"Jieba\u5206\u8bcd", None))
#if QT_CONFIG(tooltip)
        self.remove_punct_cb.setToolTip(QCoreApplication.translate("Preprocess", u"\u79fb\u9664\u6240\u6709\u6807\u70b9\u7b26\u53f7", None))
#endif // QT_CONFIG(tooltip)
        self.remove_punct_cb.setText(QCoreApplication.translate("Preprocess", u"\u53bb\u9664\u6807\u70b9\u7b26\u53f7", None))
#if QT_CONFIG(tooltip)
        self.remove_urls_cb.setToolTip(QCoreApplication.translate("Preprocess", u"\u79fb\u9664\u6587\u672c\u4e2d\u7684\u7f51\u5740\u94fe\u63a5", None))
#endif // QT_CONFIG(tooltip)
        self.remove_urls_cb.setText(QCoreApplication.translate("Preprocess", u"\u53bb\u9664URL", None))
#if QT_CONFIG(tooltip)
        self.lowercase_cb.setToolTip(QCoreApplication.translate("Preprocess", u"\u5c06\u6240\u6709\u6587\u672c\u8f6c\u6362\u4e3a\u5c0f\u5199\uff08\u9002\u7528\u4e8e\u82f1\u6587\uff09", None))
#endif // QT_CONFIG(tooltip)
        self.lowercase_cb.setText(QCoreApplication.translate("Preprocess", u"\u8f6c\u6362\u5927\u5c0f\u5199", None))
#if QT_CONFIG(tooltip)
        self.remove_stopwords_cb.setToolTip(QCoreApplication.translate("Preprocess", u"\u79fb\u9664\u5e38\u89c1\u505c\u7528\u8bcd", None))
#endif // QT_CONFIG(tooltip)
        self.remove_stopwords_cb.setText(QCoreApplication.translate("Preprocess", u"\u53bb\u9664\u505c\u7528\u8bcd", None))
#if QT_CONFIG(tooltip)
        self.remove_emails_cb.setToolTip(QCoreApplication.translate("Preprocess", u"\u79fb\u9664\u6587\u672c\u4e2d\u7684\u7535\u5b50\u90ae\u4ef6\u5730\u5740", None))
#endif // QT_CONFIG(tooltip)
        self.remove_emails_cb.setText(QCoreApplication.translate("Preprocess", u"\u53bb\u9664\u90ae\u7bb1\u5730\u5740", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Preprocess", u"Jieba\u8bbe\u7f6e", None))
        self.label_5.setText(QCoreApplication.translate("Preprocess", u"\u505c\u7528\u8bcd\u8868", None))
        self.browse_stop_btn.setText(QCoreApplication.translate("Preprocess", u"...", None))
        self.label_4.setText(QCoreApplication.translate("Preprocess", u"\u81ea\u5b9a\u4e49\u8bcd\u5178", None))
        self.browse_dict_btn.setText(QCoreApplication.translate("Preprocess", u"...", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Preprocess", u"\u64cd\u4f5c", None))
        self.btnSaveResults.setText(QCoreApplication.translate("Preprocess", u"\u4fdd\u5b58\u7ed3\u679c", None))
        self.btnStartProcess.setText(QCoreApplication.translate("Preprocess", u"\u5f00\u59cb\u5904\u7406", None))
    # retranslateUi

