# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './wnd_main_visil.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wndMainVisil(object):
    def setupUi(self, wndMainVisil):
        wndMainVisil.setObjectName("wndMainVisil")
        wndMainVisil.resize(1169, 889)
        wndMainVisil.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.centralwidget = QtWidgets.QWidget(wndMainVisil)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget.setObjectName("centralwidget")
        wndMainVisil.setCentralWidget(self.centralwidget)
        self.status_bar = QtWidgets.QStatusBar(wndMainVisil)
        self.status_bar.setObjectName("status_bar")
        wndMainVisil.setStatusBar(self.status_bar)
        self.dck_lista_voos = QtWidgets.QDockWidget(wndMainVisil)
        self.dck_lista_voos.setStyleSheet("")
        self.dck_lista_voos.setFloating(False)
        self.dck_lista_voos.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dck_lista_voos.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dck_lista_voos.setObjectName("dck_lista_voos")
        self.dwc_lista = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dwc_lista.sizePolicy().hasHeightForWidth())
        self.dwc_lista.setSizePolicy(sizePolicy)
        self.dwc_lista.setObjectName("dwc_lista")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dwc_lista)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_hora = QtWidgets.QLabel(self.dwc_lista)
        self.lbl_hora.setStyleSheet("font: 65 italic 26pt \"Courier New\";\n"
"color:rgb(0, 170, 0);")
        self.lbl_hora.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_hora.setObjectName("lbl_hora")
        self.verticalLayout_2.addWidget(self.lbl_hora)
        self.wid_lv = QtWidgets.QWidget(self.dwc_lista)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wid_lv.sizePolicy().hasHeightForWidth())
        self.wid_lv.setSizePolicy(sizePolicy)
        self.wid_lv.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: #729fcf;")
        self.wid_lv.setObjectName("wid_lv")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.wid_lv)
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_icon = QtWidgets.QLabel(self.wid_lv)
        self.lbl_icon.setText("")
        self.lbl_icon.setPixmap(QtGui.QPixmap(":/images/compile16.png"))
        self.lbl_icon.setObjectName("lbl_icon")
        self.horizontalLayout_3.addWidget(self.lbl_icon)
        self.lbl_title = QtWidgets.QLabel(self.wid_lv)
        self.lbl_title.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 14pt \"Arial\";")
        self.lbl_title.setObjectName("lbl_title")
        self.horizontalLayout_3.addWidget(self.lbl_title)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.wid_lv)
        self.qtv_stp = QtWidgets.QTableView(self.dwc_lista)
        self.qtv_stp.setObjectName("qtv_stp")
        self.verticalLayout_2.addWidget(self.qtv_stp)
        self.dck_lista_voos.setWidget(self.dwc_lista)
        wndMainVisil.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dck_lista_voos)
        self.action_exit = QtWidgets.QAction(wndMainVisil)
        self.action_exit.setObjectName("action_exit")

        self.retranslateUi(wndMainVisil)
        QtCore.QMetaObject.connectSlotsByName(wndMainVisil)

    def retranslateUi(self, wndMainVisil):
        _translate = QtCore.QCoreApplication.translate
        wndMainVisil.setWindowTitle(_translate("wndMainVisil", "ViSIL 0.1 [Visualização]"))
        self.lbl_hora.setText(_translate("wndMainVisil", "12:00:00"))
        self.lbl_title.setText(_translate("wndMainVisil", "Lista de Vôos"))
        self.action_exit.setText(_translate("wndMainVisil", "Sair"))
        self.action_exit.setShortcut(_translate("wndMainVisil", "Ctrl+X"))

import resources_rc
