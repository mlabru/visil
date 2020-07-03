# -*- coding: utf-8 -*-
"""
statusbar_basic

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# pyQt library
from PyQt5 import Qt, QtWidgets
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui, QtWidgets

# < class CStatusBarBasic >------------------------------------------------------------------------

class CStatusBarBasic(QtWidgets.QStatusBar):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        constructor
        """
        # verifica parâmetros de entrada
        assert f_parent

        # init super class
        super(CStatusBarBasic, self).__init__(f_parent)

        # QMainWindow
        self._parent = f_parent

        # local variables
        self._lbl_coord = None
        self._lbl_exe = None
        self._lbl_hora = None
        self._lbl_msg = None
        self._lbl_range = None

        # config status bar
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        # self.setBackgroundMode(QtCore.Qt.NoBackground)
        # self.setStyleSheet("color: black;\nbackground-color: transparent;")

        # create permanent widgets
        self._create_statusbar_labels()

        # add widgets in status bar
        self.addWidget(self._lbl_msg)

        # add permanent widgets in status bar
        self.addPermanentWidget(self._lbl_coord)
        self.addPermanentWidget(self._lbl_range)
        self.addPermanentWidget(self._lbl_exe)
        self.addPermanentWidget(self._lbl_hora)

        # exibe a status bar
        self.show()

        # show temporary message (5s)
        self.showMessage(QtCore.QCoreApplication.translate("CStatusBarBasic", "Ready", None), 5000)

    # ---------------------------------------------------------------------------------------------
    def _create_statusbar_labels(self):
        """
        DOCUMENT ME!
        """
        # mensagem
        self._lbl_msg = QtWidgets.QLabel(self)
        assert self._lbl_msg

        self._lbl_msg.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._lbl_msg.setMinimumSize(self._lbl_msg.sizeHint())

        # coordinates label
        self._lbl_coord = QtWidgets.QLabel(self)
        assert self._lbl_coord

        self._lbl_coord.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._lbl_coord.setMinimumSize(self._lbl_coord.sizeHint())

        # range label
        self._lbl_range = QtWidgets.QLabel(self)
        assert self._lbl_range

        self._lbl_range.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self._lbl_range.setMinimumSize(self._lbl_range.sizeHint())
        self._lbl_range.setAutoFillBackground(True)

        l_pal = self._lbl_range.palette()
        l_col = QtGui.QColor(255, 255, 150)
        assert l_col

        l_pal.setColor(QtGui.QPalette.Window, l_col)
        self._lbl_range.setPalette(l_pal)

        # exercício
        self._lbl_exe = QtWidgets.QLabel(self)
        assert self._lbl_exe

        self._lbl_exe.setAlignment(QtCore.Qt.AlignHCenter)
        self._lbl_exe.setMinimumSize(self._lbl_exe.sizeHint())
        self._lbl_exe.setAutoFillBackground(True)

        l_pal = self._lbl_exe.palette()
        l_pal.setColor(QtGui.QPalette.Window, QtGui.QColor(150, 255, 255))

        self._lbl_exe.setPalette(l_pal)

        # horário
        self._lbl_hora = QtWidgets.QLabel(self)
        assert self._lbl_hora

        self._lbl_hora.setAlignment(QtCore.Qt.AlignHCenter)
        self._lbl_hora.setMinimumSize(self._lbl_hora.sizeHint())
        self._lbl_hora.setAutoFillBackground(True)

        l_pal = self._lbl_hora.palette()
        l_pal.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 150))

        self._lbl_hora.setPalette(l_pal)

    # ---------------------------------------------------------------------------------------------
    def update_coordinates(self, fs_coordinates, fv_update=True):
        """
        updates the latitude and longitude on the status bar of radar screen
        """
        # flag update ?
        if fv_update:
            # set latitude/longitude coordinates label
            self._lbl_coord.setText(fs_coordinates)

            # update status bar
            self.update()

    # ---------------------------------------------------------------------------------------------
    def update_exe(self, fs_exe, fv_update=True):
        """
        DOCUMENT ME!
        """
        # flag update ?
        if fv_update:
            # independant mode ?
            self._lbl_exe.setText(fs_exe)

            # update status bar
            self.update()

    # ---------------------------------------------------------------------------------------------
    def update_hora(self, fs_hora, fv_update=True):
        """
        DOCUMENT ME!
        """
        # set hora label
        self._lbl_hora.setText(fs_hora)

        # flag update ?
        if fv_update:
            # update status bar
            self.update()

    # ---------------------------------------------------------------------------------------------
    def update_msg(self, fs_msg, fv_update=True):
        """
        DOCUMENT ME!
        """
        # flag update ?
        if fv_update:
            # set message label
            self._lbl_msg.setText(fs_msg)

            # update status bar
            self.update()

    # ---------------------------------------------------------------------------------------------
    def update_range(self, fi_range, fv_update=True):
        """
        updates the range on the status bar of radar windows
        """
        # flag update ?
        if fv_update:
            # set range label
            self._lbl_range.setText("R%d" % fi_range)

            # update status bar
            self.update()

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_coord(self):
        """
        get coordenadas
        """
        return self._lbl_coord

    @lbl_coord.setter
    def lbl_coord(self, f_val):
        """
        set coordenadas
        """
        self._lbl_coord = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_exe(self):
        """
        get exercício
        """
        return self._lbl_exe

    @lbl_exe.setter
    def lbl_exe(self, f_val):
        """
        set exercício
        """
        self._lbl_exe = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_hora(self):
        """
        get hora
        """
        return self._lbl_hora

    @lbl_hora.setter
    def lbl_hora(self, f_val):
        """
        set hora
        """
        self._lbl_hora = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_msg(self):
        """
        get message
        """
        return self._lbl_msg

    @lbl_msg.setter
    def lbl_msg(self, f_val):
        """
        set message
        """
        self._lbl_msg = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def parent(self):
        """
        get parent
        """
        return self._parent

    @parent.setter
    def parent(self, f_val):
        """
        set parent
        """
        self._parent = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lbl_range(self):
        """ 
        get range
        """
        return self._lbl_range

    @lbl_range.setter
    def lbl_range(self, f_val):
        """ 
        set range
        """
        self._lbl_range = f_val

# < the end >--------------------------------------------------------------------------------------
