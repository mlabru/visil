# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dock_procedures.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dck_procedures(object):
    def setupUi(self, dck_procedures):
        dck_procedures.setObjectName("dck_procedures")
        dck_procedures.resize(316, 480)
        self.dwc_procedures = QtWidgets.QWidget()
        self.dwc_procedures.setObjectName("dwc_procedures")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dwc_procedures)
        self.verticalLayout.setObjectName("verticalLayout")
        self.wid_tbx_head = QtWidgets.QWidget(self.dwc_procedures)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wid_tbx_head.sizePolicy().hasHeightForWidth())
        self.wid_tbx_head.setSizePolicy(sizePolicy)
        self.wid_tbx_head.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: #729fcf;")
        self.wid_tbx_head.setObjectName("wid_tbx_head")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.wid_tbx_head)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_icon = QtWidgets.QLabel(self.wid_tbx_head)
        self.lbl_icon.setText("")
        self.lbl_icon.setPixmap(QtGui.QPixmap(":/images/compile16.png"))
        self.lbl_icon.setObjectName("lbl_icon")
        self.horizontalLayout.addWidget(self.lbl_icon)
        self.lbl_title = QtWidgets.QLabel(self.wid_tbx_head)
        self.lbl_title.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 14pt \"Arial\";")
        self.lbl_title.setObjectName("lbl_title")
        self.horizontalLayout.addWidget(self.lbl_title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.wid_tbx_head)
        self.tbx_procedures = QtWidgets.QToolBox(self.dwc_procedures)
        self.tbx_procedures.setObjectName("tbx_procedures")
        self.pag_procs = QtWidgets.QWidget()
        self.pag_procs.setGeometry(QtCore.QRect(0, 0, 298, 299))
        self.pag_procs.setObjectName("pag_procs")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.pag_procs)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tree_procs = QtWidgets.QTreeWidget(self.pag_procs)
        self.tree_procs.setObjectName("tree_procs")
        self.tree_procs.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.tree_procs)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/execute.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbx_procedures.addItem(self.pag_procs, icon, "")
        self.pag_navaids = QtWidgets.QWidget()
        self.pag_navaids.setGeometry(QtCore.QRect(0, 0, 298, 299))
        self.pag_navaids.setObjectName("pag_navaids")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.pag_navaids)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tree_navaids = QtWidgets.QTreeWidget(self.pag_navaids)
        self.tree_navaids.setObjectName("tree_navaids")
        self.tree_navaids.headerItem().setText(0, "1")
        self.verticalLayout_3.addWidget(self.tree_navaids)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/navaid.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbx_procedures.addItem(self.pag_navaids, icon1, "")
        self.pag_runways = QtWidgets.QWidget()
        self.pag_runways.setEnabled(False)
        self.pag_runways.setGeometry(QtCore.QRect(0, 0, 298, 299))
        self.pag_runways.setObjectName("pag_runways")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.pag_runways)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tree_runways = QtWidgets.QTreeWidget(self.pag_runways)
        self.tree_runways.setObjectName("tree_runways")
        self.tree_runways.headerItem().setText(0, "1")
        self.verticalLayout_4.addWidget(self.tree_runways)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/linepointer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbx_procedures.addItem(self.pag_runways, icon2, "")
        self.verticalLayout.addWidget(self.tbx_procedures)
        dck_procedures.setWidget(self.dwc_procedures)

        self.retranslateUi(dck_procedures)
        self.tbx_procedures.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(dck_procedures)

    def retranslateUi(self, dck_procedures):
        _translate = QtCore.QCoreApplication.translate
        self.lbl_title.setText(_translate("dck_procedures", "Procedures"))
        self.tbx_procedures.setItemText(self.tbx_procedures.indexOf(self.pag_procs), _translate("dck_procedures", "Procedures"))
        self.tbx_procedures.setItemText(self.tbx_procedures.indexOf(self.pag_navaids), _translate("dck_procedures", "Navaids"))
        self.tbx_procedures.setItemText(self.tbx_procedures.indexOf(self.pag_runways), _translate("dck_procedures", "Runways"))

import resources_rc
