# -*- coding: utf-8 -*-
"""
model manager

revision 0.4  2016/ago  mlabru
pequenas correções e otimização

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e config manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# control
import control.events.events_manager as event
import control.config.config_manager as config

# < class CModelManager >--------------------------------------------------------------------------

class CModelManager(object):
    """
    main model object. Views and controllers interact with this
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        initializes the model manager

        @param f_control: control manager
        """
        # check input
        assert f_control

        # control manager
        self._control = f_control

        # config manager
        self._config = f_control.config if f_control.config is not None else config.CConfigManager()
        assert self._config

        # event manager
        self._event = f_control.event if f_control.event is not None else event.CEventsManager()
        assert self._event

        # registra como recebedor de eventos
        self._event.register_listener(self)

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        # return
        return

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def app(self):
        """
        get the application
        """
        return self._control.app

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        """
        get config manager
        """
        return self._config

    # ---------------------------------------------------------------------------------------------
    @property
    def control(self):
        """
        get control manager
        """
        return self._control

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        """
        get configuration dictionary
        """
        return self._config.dct_config if self._config is not None else {}

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        """
        get event manager
        """
        return self._event

    @event.setter
    def event(self, f_val):
        """
        get event manager
        """
        self._event = f_val

# < the end >--------------------------------------------------------------------------------------
