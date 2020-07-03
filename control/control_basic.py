# -*- coding: utf-8 -*-
"""
control_basic
the control basic interface

revision 0.3  2016/ago  mlabru
pequenas correções e otimizações

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import sys

# PyQt library
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui, QtWidgets

# control
import control.control_manager as control

# < class CControlBasic >--------------------------------------------------------------------------

class CControlBasic(control.CControlManager):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_path=None):
        """
        constructor

        @param fs_path: path do arquivo de configuração
        """
        # init super class
        super(CControlBasic, self).__init__()

        # herdados de CControlManager
        # self.event     # event manager
        # self.config    # opções de configuração
        # self.model     # model manager
        # self.view      # view manager
        # self.voip      # biblioteca de VoIP

        # the application itself
        self._app = None

        # splash screen
        self._splash = None

        # flight control
        self._ctr_flight = None

        # simulation statistics
        self._sim_stat = None

        # simulation timer
        self._sim_time = None

    # ---------------------------------------------------------------------------------------------
    def create_app(self, fs_name):
        """
        DOCUMENT ME!
        """
        # create application
        self._app = QtWidgets.QApplication(sys.argv)
        assert self._app

        # setup application parameters
        self._app.setOrganizationName("sophosoft")
        self._app.setOrganizationDomain("sophosoft.com.br")
        self._app.setApplicationName(fs_name)

        # load logo
        l_pix_logo = QtGui.QPixmap(":/images/logos/logo.png")
        assert l_pix_logo

        # create splash screen
        self._splash = QtWidgets.QSplashScreen(l_pix_logo, QtCore.Qt.WindowStaysOnTopHint)
        assert self._splash

        self._splash.setMask(l_pix_logo.mask())

        # show splash screen
        self._splash.show()

        # process events (before main loop)
        self._app.processEvents()

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        """
        get application
        """
        return self._app

    @app.setter
    def app(self, f_val):
        """
        set application
        """
        self._app = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ctr_flight(self):
        """
        get flight control
        """
        return self._ctr_flight

    @ctr_flight.setter
    def ctr_flight(self, f_val):
        """
        set flight control
        """
        self._ctr_flight = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sim_stat(self):
        """
        get simulation statistics
        """
        return self._sim_stat

    @sim_stat.setter
    def sim_stat(self, f_val):
        """
        set simulation statistics
        """
        self._sim_stat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def sim_time(self):
        """
        get simulation timer
        """
        return self._sim_time

    @sim_time.setter
    def sim_time(self, f_val):
        """
        set simulation timer
        """
        self._sim_time = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def splash(self):
        """
        get splash screen
        """
        return self._splash

    @splash.setter
    def splash(self, f_val):
        """
        set splash screen
        """
        self._splash = f_val

# < the end >--------------------------------------------------------------------------------------
