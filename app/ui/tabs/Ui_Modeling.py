# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Tab2.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Modeling(object):
    def setupUi(self, Modeling):
        if not Modeling.objectName():
            Modeling.setObjectName(u"Modeling")
        Modeling.resize(675, 379)
        self.verticalLayout_6 = QVBoxLayout(Modeling)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(Modeling)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.model_combo = QComboBox(self.groupBox)
        self.model_combo.setObjectName(u"model_combo")

        self.horizontalLayout_4.addWidget(self.model_combo)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 8)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(self.groupBox)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_5.addWidget(self.comboBox_2)

        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(1, 8)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_5 = QGroupBox(Modeling)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout = QVBoxLayout(self.groupBox_5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.train_btn = QPushButton(self.groupBox_5)
        self.train_btn.setObjectName(u"train_btn")

        self.verticalLayout.addWidget(self.train_btn)

        self.save_model_btn = QPushButton(self.groupBox_5)
        self.save_model_btn.setObjectName(u"save_model_btn")

        self.verticalLayout.addWidget(self.save_model_btn)

        self.load_model_btn = QPushButton(self.groupBox_5)
        self.load_model_btn.setObjectName(u"load_model_btn")

        self.verticalLayout.addWidget(self.load_model_btn)


        self.horizontalLayout.addWidget(self.groupBox_5)

        self.horizontalLayout.setStretch(0, 6)
        self.horizontalLayout.setStretch(1, 4)

        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_3 = QGroupBox(Modeling)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.umap_n_neighbors_spin = QSpinBox(self.groupBox_3)
        self.umap_n_neighbors_spin.setObjectName(u"umap_n_neighbors_spin")

        self.gridLayout.addWidget(self.umap_n_neighbors_spin, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.umap_n_components_spin = QSpinBox(self.groupBox_3)
        self.umap_n_components_spin.setObjectName(u"umap_n_components_spin")

        self.gridLayout.addWidget(self.umap_n_components_spin, 1, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.umap_min_dist_spin = QSpinBox(self.groupBox_3)
        self.umap_min_dist_spin.setObjectName(u"umap_min_dist_spin")

        self.gridLayout.addWidget(self.umap_min_dist_spin, 2, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.umap_metric_combo = QComboBox(self.groupBox_3)
        self.umap_metric_combo.setObjectName(u"umap_metric_combo")

        self.gridLayout.addWidget(self.umap_metric_combo, 3, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)


        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(Modeling)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)

        self.hdbscan_min_cluster_spin = QSpinBox(self.groupBox_4)
        self.hdbscan_min_cluster_spin.setObjectName(u"hdbscan_min_cluster_spin")

        self.gridLayout_2.addWidget(self.hdbscan_min_cluster_spin, 0, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.hdbscan_min_samples_spin = QSpinBox(self.groupBox_4)
        self.hdbscan_min_samples_spin.setObjectName(u"hdbscan_min_samples_spin")

        self.gridLayout_2.addWidget(self.hdbscan_min_samples_spin, 1, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)

        self.hdbscan_metric_combo = QComboBox(self.groupBox_4)
        self.hdbscan_metric_combo.setObjectName(u"hdbscan_metric_combo")

        self.gridLayout_2.addWidget(self.hdbscan_metric_combo, 2, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)


        self.horizontalLayout_2.addWidget(self.groupBox_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.groupBox_2 = QGroupBox(Modeling)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_3.addWidget(self.label_10)

        self.top_n_words_spin = QSpinBox(self.groupBox_2)
        self.top_n_words_spin.setObjectName(u"top_n_words_spin")

        self.horizontalLayout_3.addWidget(self.top_n_words_spin)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_3.addWidget(self.label_11)

        self.min_topic_size_spin = QSpinBox(self.groupBox_2)
        self.min_topic_size_spin.setObjectName(u"min_topic_size_spin")

        self.horizontalLayout_3.addWidget(self.min_topic_size_spin)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_3.addWidget(self.label_12)

        self.nr_topics_spin = QSpinBox(self.groupBox_2)
        self.nr_topics_spin.setObjectName(u"nr_topics_spin")

        self.horizontalLayout_3.addWidget(self.nr_topics_spin)

        self.calc_probs_cb = QCheckBox(self.groupBox_2)
        self.calc_probs_cb.setObjectName(u"calc_probs_cb")

        self.horizontalLayout_3.addWidget(self.calc_probs_cb)


        self.verticalLayout_6.addWidget(self.groupBox_2)


        self.retranslateUi(Modeling)

        QMetaObject.connectSlotsByName(Modeling)
    # setupUi

    def retranslateUi(self, Modeling):
        Modeling.setWindowTitle(QCoreApplication.translate("Modeling", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Modeling", u"\u5d4c\u5165\u6a21\u578b", None))
        self.label.setText(QCoreApplication.translate("Modeling", u"\u9009\u62e9\u6a21\u578b", None))
        self.label_2.setText(QCoreApplication.translate("Modeling", u"\u9009\u62e9\u8bed\u8a00", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Modeling", u"\u64cd\u4f5c", None))
        self.train_btn.setText(QCoreApplication.translate("Modeling", u"\u5f00\u59cb\u8bad\u7ec3", None))
        self.save_model_btn.setText(QCoreApplication.translate("Modeling", u"\u4fdd\u5b58\u6a21\u578b", None))
        self.load_model_btn.setText(QCoreApplication.translate("Modeling", u"\u52a0\u8f7d\u6a21\u578b", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Modeling", u"UMAP\u53c2\u6570", None))
        self.label_3.setText(QCoreApplication.translate("Modeling", u"n_neighbors", None))
#if QT_CONFIG(tooltip)
        self.umap_n_neighbors_spin.setToolTip(QCoreApplication.translate("Modeling", u"\u8f83\u5927\u503c\u4fdd\u7559\u5168\u5c40\u7ed3\u6784\uff0c\u8f83\u5c0f\u503c\u4fdd\u7559\u5c40\u90e8\u7ed3\u6784", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Modeling", u"n_components", None))
#if QT_CONFIG(tooltip)
        self.umap_n_components_spin.setToolTip(QCoreApplication.translate("Modeling", u"\u964d\u7ef4\u540e\u7684\u7ef4\u5ea6\u6570", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Modeling", u"min_dist", None))
#if QT_CONFIG(tooltip)
        self.umap_min_dist_spin.setToolTip(QCoreApplication.translate("Modeling", u"\u63a7\u5236\u70b9\u4e4b\u95f4\u7684\u6700\u5c0f\u8ddd\u79bb", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("Modeling", u"metric", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Modeling", u"HDBSCAN\u53c2\u6570", None))
        self.label_7.setText(QCoreApplication.translate("Modeling", u"min_cluster_size", None))
#if QT_CONFIG(tooltip)
        self.hdbscan_min_cluster_spin.setToolTip(QCoreApplication.translate("Modeling", u"\u6700\u5c0f\u7c07\u5927\u5c0f", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("Modeling", u"min_samples", None))
#if QT_CONFIG(tooltip)
        self.hdbscan_min_samples_spin.setToolTip(QCoreApplication.translate("Modeling", u"\u6838\u5fc3\u70b9\u7684\u6700\u5c0f\u90bb\u5c45\u6570", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("Modeling", u"metric", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Modeling", u"\u9ad8\u7ea7\u8bbe\u7f6e", None))
        self.label_10.setText(QCoreApplication.translate("Modeling", u"\u6bcf\u4e3b\u9898\u8bcd\u6570:", None))
        self.label_11.setText(QCoreApplication.translate("Modeling", u"\u6bcf\u4e3b\u9898\u5927\u5c0f:", None))
        self.label_12.setText(QCoreApplication.translate("Modeling", u"\u76ee\u6807\u4e3b\u9898\u6570 (\u53ef\u9009):", None))
#if QT_CONFIG(tooltip)
        self.nr_topics_spin.setToolTip(QCoreApplication.translate("Modeling", u"\u8bbe\u4e3a 0 \u8868\u793a\u81ea\u52a8\u786e\u5b9a\u4e3b\u9898\u6570", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.calc_probs_cb.setToolTip(QCoreApplication.translate("Modeling", u"\u8ba1\u7b97\u6587\u6863\u7684\u4e3b\u9898\u6982\u7387\u5206\u5e03\uff08\u8f83\u6162\uff09", None))
#endif // QT_CONFIG(tooltip)
        self.calc_probs_cb.setText(QCoreApplication.translate("Modeling", u"\u8ba1\u7b97\u4e3b\u9898\u6982\u7387", None))
    # retranslateUi

