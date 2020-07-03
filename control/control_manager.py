# -*- coding: utf-8 -*-
"""
control_manager
coordinates communications between the model, views and controllers through the use of events

revision 0.5  2017/abr  mlabru
pequenas correções e otimizações

revision 0.4  2016/ago  mlabru
pequenas correções e otimizações

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e alteração do config manager

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import os
import sys
import threading
import time

# model 
import model.common.glb_data as gdata

# control
import control.events.events_manager as evtmgr
import control.events.events_basic as events

# < class CControlManager >------------------------------------------------------------------------

class CControlManager(threading.Thread):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # inicia a super classe
        super(CControlManager, self).__init__()

        # instancia o event manager
        self._event = evtmgr.CEventsManager()
        assert self._event

        # registra a sí próprio como recebedor de eventos
        self._event.register_listener(self)

        # opções de configuração
        self._config = None

        # model
        self._model = None

        # view
        self._view = None

        # voip library
        self._voip = None

    # ---------------------------------------------------------------------------------------------
    def cbk_termina(self):
        """
        termina a aplicação
        """
        # clear to go
        assert self._event

        # cria um evento de quit
        l_evt = events.CQuit()
        assert l_evt

        # dissemina o evento
        self._event.post(l_evt)

    # ---------------------------------------------------------------------------------------------
    @staticmethod
    def notify(f_evt):
        """
        callback de tratamento de eventos recebidos

        @param f_evt: event
        """
        # check input
        assert f_evt

        # recebeu um aviso de término da aplicação ?
        if isinstance(f_evt, events.CQuit):
            # para todos os processos
            gdata.G_KEEP_RUN = False

            # aguarda o término das tasks
            time.sleep(1)

            # termina a aplicação
            sys.exit()

    # ---------------------------------------------------------------------------------------------
    def run(self):
        """
        executa a aplicação
        """
        # return
        return gdata.G_KEEP_RUN

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, f_val):
        self._config = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, f_val):
        self._event = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, f_val):
        self._model = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, f_val):
        self._view = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def voip(self):
        return self._voip

# < the end >--------------------------------------------------------------------------------------
