# -*- coding: utf-8 -*-
"""
model_visil

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# PyQt library
from PyQt5 import QtCore

# libs
import libs.coords.coord_sys as coords
import libs.geomag.geomag.geomag.geomag as gm

# model
import model.model_manager as model

import model.visil.emula_visil as emula
import model.visil.airspace_visil as airs

# control
import control.common.glb_defs as gdefs
import control.events.events_basic as event

# < class CModelVisil >----------------------------------------------------------------------------

class CModelVisil(model.CModelManager):
    """
    visir model object
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control):
        """
        constructor
        
        @param f_control: control manager
        """
        # init super class
        super(CModelVisil, self).__init__(f_control)

        # herdados de CModelManager
        # self.app           # the application
        # self.config        # config manager
        # self.dct_config    # dicionário de configuração
        # self.control       # control manager
        # self.event         # event manager

        # show message
        self.control.splash.showMessage("creating coordinate system...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        
        # obtém as coordenadas de referência
        lf_ref_lat = float(self.dct_config["map.lat"])
        lf_ref_lng = float(self.dct_config["map.lng"])
        lf_dcl_mag = float(self.dct_config["map.dcl"])

        # coordinate system
        self._coords = coords.CCoordSys(lf_ref_lat, lf_ref_lng, lf_dcl_mag)
        assert self._coords

        # create magnectic converter
        self._geomag = gm.GeoMag("data/tabs/WMM.COF")
        assert self._geomag

        self.control.splash.showMessage("loading cenary...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

        # variáveis de instância
        self._airspace = None

        # carrega as tabelas do sistema
        self._load_cenario()

        self.control.splash.showMessage("creating emulation model...", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.white)

        # create emula model
        self._emula = emula.CEmulaVisil(self, f_control)
        assert self._emula

    # ---------------------------------------------------------------------------------------------
    def _load_air(self):
        """
        faz a carga do airspace

        @return flag e mensagem
        """
        # obtém o diretório padrão de airspaces
        ls_dir = self.dct_config["dir.air"]

        # nome do diretório vazio ?
        if ls_dir is None:
            # diretório padrão de airspaces
            self.dct_config["dir.air"] = gdefs.D_DIR_AIR

            # diretório padrão de airspaces
            ls_dir = gdefs.D_DIR_AIR

        # expand user (~)
        ls_dir = os.path.expanduser(ls_dir)

        # create airspace (aeródomos, fixos, pistas, pousos e decolagens)
        self._airspace = airs.CAirspaceVisil(self)
        assert self._airspace

        # carrega os dicionários (aproximações, esperas, subidas e trajetórias)
        self._airspace.load_dicts()

        # retorna ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def _load_cenario(self):
        """
        carrega as tabelas do sistema

        @return flag e mensagem
        """
        # carrega o landscape
        # lv_ok, ls_msg = self._load_land()

        # tudo Ok ?
        # if lv_ok:
        
        # carrega o airspace
        lv_ok, ls_msg = self._load_air()

        # houve erro em alguma fase ?
        if not lv_ok:
            # logger
            l_log = logging.getLogger("CModelVisil::_load_cenario")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E01: erro na carga da base de dados: {}.".format(ls_msg))

            # cria um evento de quit
            l_evt = event.CQuit()
            assert l_evt

            # dissemina o evento
            self.event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_evt):
        """
        callback de tratamento de eventos recebidos

        @param f_evt: evento recebido
        """
        # return
        return
        
    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def airspace(self):
        """
        get airspace
        """
        return self._airspace

    # ---------------------------------------------------------------------------------------------
    @property
    def coords(self):
        """
        get coordinate system
        """
        return self._coords

    @coords.setter
    def coords(self, f_val):
        """
        set coordinate system
        """
        self._coords = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def emula(self):
        """
        get emula model
        """
        return self._emula

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_esp(self):
        """
        get esperas
        """
        return self._airspace.dct_esp

    # ---------------------------------------------------------------------------------------------
    @property
    def geomag(self):
        """
        get geomag
        """
        return self._geomag

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sub(self):
        """
        get subidas
        """
        return self._airspace.dct_sub

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trj(self):
        """
        get trajetórias
        """
        return self._airspace.dct_trj

# < the end >--------------------------------------------------------------------------------------
