# -*- coding: utf-8 -*-
"""
view_manager

revision 0.3  2016/ago  mlabru
pequenas correções e otimizações

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < class CViewManager >---------------------------------------------------------------------------

class CViewManager(object):
    """
    handles all interaction with user. This class is the interface
    It draws the scope on the screen and handles all mouse input
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        @param f_control: control
        """
        # check input
        assert f_control

        # control
        self._control = f_control

        # register as listener
        f_control.event.register_listener(self)

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # return
        return

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        run
        """
        # return
        return

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        return self._control.app

    @app.setter
    def app(self, f_val):

        # check input
        assert f_val

        # app
        self._control.app = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        return self._control.config

    @config.setter
    def config(self, f_val):

        # check input
        assert f_val

        # config
        self._control.config = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        return self._control.config.dct_config

    @dct_config.setter
    def dct_config(self, f_val):

        # check input
        assert f_val

        # configuration dictionary
        self._control.config.dct_config = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def control(self):
        return self._control

    @control.setter
    def control(self, f_val):

        # check input
        assert f_val

        # control
        self._control = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        return self._control.event

    @event.setter
    def event(self, f_val):

        # check input
        assert f_val

        # event
        self._control.event = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self._control.model

    @model.setter
    def model(self, f_val):

        # check input
        assert f_val

        # model
        self._control.model = f_val

# < the end >--------------------------------------------------------------------------------------
