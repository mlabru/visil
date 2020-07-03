# -*- coding: utf-8 -*-
"""
airspace_basic

basic model manager
load from one configuration file all configured tables

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
inclusão do event manager e config manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os

# model
import model.items.aer_data as aerdata
import model.items.fix_data as fixdata

# < class CAirspaceBasic >-------------------------------------------------------------------------

class CAirspaceBasic(object):
    """
    basic airspace model manager
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model):
        """
        @param f_model: model manager
        """
        # check input
        assert f_model

        # init super class
        super(CAirspaceBasic, self).__init__()

        # model manager
        self._model = f_model

        # event manager
        self._event = f_model.event

        # registra-se como recebedor de eventos
        self._event.register_listener(self)

        # config manager
        self._config = f_model.config

        # inicia dicionários
        self._dct_aer = {}
        self._lst_arr_dep = []
        self._dct_fix = {}

        # carrega as tabelas de dados nos dicionários
        self._load_dicts()
        
    # ---------------------------------------------------------------------------------------------
    def _load_dicts(self):
        """
        carrega os dicionários
        """
        # monta o nome da tabela de fixos
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.fix"])

        # carrega a tabela de fixos em um dicionário
        self.dct_fix = fixdata.CFixData(self.model, ls_path)
        assert self.dct_fix is not None

        # monta o nome da tabela de waypoints
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.wpt"])

        # carrega a tabela de waypoints em um dicionário
        ldct_wpt = fixdata.CFixData(self.model, ls_path)
        assert ldct_wpt is not None

        # coloca os waypoints no dicionário de fixos
        self.dct_fix.update(ldct_wpt) 

        # salva referência da tabela de fixos no sistema de coordenadas
        self.model.coords.dct_fix = self.dct_fix

        # monta o nome da tabela de aeródromos
        ls_path = os.path.join(self.dct_config["dir.tab"], self.dct_config["tab.aer"])

        # carrega a tabela de aeródromos em um dicionário
        self.dct_aer = aerdata.CAerData(self.model, ls_path)

        # monta a lista de pousos/decolagens

        # para todos os aeródromos...
        for l_aer, l_aer_data in self.dct_aer.items():
            # para todas as pistas...
            for l_pst in l_aer_data.dct_aer_pistas:                
                # salva a tupla (aeródromo, pista)
                self._lst_arr_dep.append("{}/{}".format(l_aer, l_pst))

    # ---------------------------------------------------------------------------------------------
    def get_aer_pst(self, fs_aer, fs_pst):
        """
        obtém o pointer para o aeródromo e pista

        @param fs_aer: indicativo do aeródromo
        @param fs_pst: indicativo da pista

        @return pointer para o aeródromo e pista
        """
        # obtém o aeródromo
        l_aer = self._dct_aer.get(fs_aer, None)

        if l_aer is None:
            # logger
            l_log = logging.getLogger("CAirspaceBasic::get_aer_pst")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E01: não existe aeródromo [{}].".format(fs_aer))

            # retorna pointers
            return None, None

        # obtém a pista
        l_pst = l_aer.dct_aer_pistas.get(fs_pst, None)

        if l_pst is None:
            # logger
            l_log = logging.getLogger("CAirspaceBasic::get_aer_pst")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E02: não existe pista [{}] no aeródromo [{}].".format(fs_pst, fs_aer))

            # retorna pointers
            return l_aer, None

        # retorna pointers
        return l_aer, l_pst

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
    def dct_aer(self):
        return self._dct_aer

    @dct_aer.setter
    def dct_aer(self, f_val):
        self._dct_aer = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_arr_dep(self):
        return self._lst_arr_dep

    @lst_arr_dep.setter
    def lst_arr_dep(self, f_val):
        self._lst_arr_dep = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def config(self):
        return self._config

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_config(self):
        return self._config.dct_config if self._config is not None else {}

    # ---------------------------------------------------------------------------------------------
    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, f_val):
        self._event = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_fix(self):
        return self._dct_fix

    @dct_fix.setter
    def dct_fix(self, f_val):
        self._dct_fix = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def model(self):
        return self._model

# < the end >--------------------------------------------------------------------------------------
