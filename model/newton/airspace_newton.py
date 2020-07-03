# -*- coding: utf-8 -*-
"""
airspace_newton

basic airspace. Load from one configuration file all configured tables

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

# libs
import libs.coords.pos_lat_lng as pll

# model
import model.common.airspace_basic as airs

# import model.items.ape_data as apedata
import model.items.apx_data as apxdata
import model.items.esp_data as espdata
# import model.items.ils_data as ilsdata
import model.items.sub_data as subdata
import model.items.trj_data as trjdata

import model.newton.defs_newton as ldefs

# < class CAirspaceNewton >-------------------------------------------------------------------------

class CAirspaceNewton(airs.CAirspaceBasic):
    """
    newton airspace
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model):
        """
        @param f_model: model manager
        """
        # init super class
        super(CAirspaceNewton, self).__init__(f_model)

        # herdado de CAirspaceBasic
        # self.model           # model manager 
        # self.event           # event manager
        # self.config          # config manager
        # self.dct_aer         # dicionário de aeródromos
        # self.lst_arr_dep     # lista de pousos/decolagens
        # self.dct_fix         # dicionário de fixos

        # procedimentos de aproximação perdida
        self._dct_ape = {}

        # procedimentos de aproximação
        self._dct_apx = {}

        # procedimentos de espera
        self._dct_esp = {}

        # procedimentos de ILS
        self._dct_ils = {}

        # procedimentos de subida
        self._dct_sub = {}

        # procedimentos de trajetória
        self._dct_trj = {}

    # ---------------------------------------------------------------------------------------------
    def get_brk_prc(self, f_brk):
        """
        DOCUMENT ME!
        """
        # existe procedimento associado ?
        if f_brk.ptr_brk_prc is not None:
            # obtém o procedimento e a função operacional
            f_brk.ptr_brk_prc, f_brk.en_brk_fnc_ope = self.get_ptr_prc(f_brk.ptr_brk_prc)

    # ---------------------------------------------------------------------------------------------
    def get_position(self, fs_indc):
        """
        get position of a aerodome/fix/vor/ndb/... named as specified

        @param fs_indc: indicativo do objeto (str)
        """
        # check input
        # assert f_model

        # pesquisa aeródromos
        l_aer = self.dct_aer.get(fs_indc, None)

        if l_aer is not None:
            # return
            return pll.CPosLatLng(l_aer.f_aer_lat, l_aer.f_aer_lng)

        # pesquisa fixos
        l_key = self.dct_fix.get(fs_indc, None)

        if l_key is not None:
            # return
            return pll.CPosLatLng(l_fix.f_fix_lat, l_fix.f_fix_lng)

        # return
        return None

    # ---------------------------------------------------------------------------------------------
    def get_ptr_prc(self, fs_prc):
        """
        obtém o pointer e a função operacional de um procedimento

        @param fs_prc: procedimento no formato XXX9999

        @return pointer e função operacional
        """
        # não existe procedimento ?
        if fs_prc is None or 4 > len(fs_prc):
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E01: não existe procedimento [%s]." % fs_prc)

            # retorna pointer & função
            return None, ldefs.E_NOPROC

        #cdbg.M_DBG.debug("procedimento : [%s]" % fs_prc)
        # obtém o procedimento
        ls_prc = fs_prc[:3]

        # obtém o número do procedimento
        li_num_prc = int(fs_prc[3:])

        # é uma aproximação ?
        if "APE" == ls_prc:
            # check dicionário de aproximação perdida
            assert self._dct_ape is not None

            # obtém o procedimento de aproximação pelo número
            lptr_prc = self._dct_ape.get(li_num_prc, None)

            # função operacional da aproximação perdida
            le_fnc_ope = ldefs.E_APXPERDIDA if lptr_prc is not None else ldefs.E_NOPROC

        # é uma aproximação ?
        elif "APX" == ls_prc:
            # check dicionário de aproximação
            assert self._dct_apx is not None

            # obtém o procedimento de aproximação pelo número
            lptr_prc = self._dct_apx.get(li_num_prc, None)

            # função operacional da aproximação
            le_fnc_ope = ldefs.E_APROXIMACAO if lptr_prc is not None else ldefs.E_NOPROC

        # é uma espera ?
        elif "ESP" == ls_prc:
            # check dicionário de espera
            assert self._dct_esp is not None

            # obtém o procedimento de espera pelo número
            lptr_prc = self._dct_esp.get(li_num_prc, None)

            # função operacional da espera
            le_fnc_ope = ldefs.E_ESPERA if lptr_prc is not None else ldefs.E_NOPROC

        # é um ILS ?
        elif "ILS" == ls_prc:
            # check dicionário de ILS
            assert self._dct_ils is not None

            # obtém o procedimento de ILS pelo número
            lptr_prc = self._dct_ils.get(li_num_prc, None)

            # função operacional da espera
            le_fnc_ope = ldefs.E_ILS if lptr_prc is not None else ldefs.E_NOPROC

        # é uma subida ?
        elif "SUB" == ls_prc:
            # check dicionário de subidas
            assert self._dct_sub is not None

            # obtém o procedimento de subida pelo número
            lptr_prc = self._dct_sub.get(li_num_prc, None)

            # função operacional da subidas
            le_fnc_ope = ldefs.E_SUBIDA if lptr_prc is not None else ldefs.E_NOPROC

        # é uma trajetória ?
        elif "TRJ" == ls_prc:
            # check dicionário de trajetórias
            assert self._dct_trj is not None

            # obtém o procedimento de trajetória pelo número
            lptr_prc = self._dct_trj.get(li_num_prc, None)

            # função operacional da trajetória
            le_fnc_ope = ldefs.E_TRAJETORIA if lptr_prc is not None else ldefs.E_NOPROC

        # senão, procedimento desconhecido
        else:
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E02: procedimento [{}] desconhecido. fallback to noProc.".format(fs_prc))

            # sem procedimento
            lptr_prc = None
            le_fnc_ope = ldefs.E_NOPROC

        # função operacional sem procedimento ?
        if (lptr_prc is None) and (ldefs.E_NOPROC != le_fnc_ope):
            # logger
            l_log = logging.getLogger("CAirspaceNewton::get_ptr_prc")
            l_log.setLevel(logging.ERROR)
            l_log.error("<E03: função operacional:[{}] sem procedimento:[{}].".format(ls_prc, li_num_prc))

        # retorna pointer & função
        return lptr_prc, le_fnc_ope

    # ---------------------------------------------------------------------------------------------
    def load_dicts(self):
        """
        DOCUMENT ME!
        """
        # monta o nome da tabela de procedimentos de aproximação perdida
        #ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.ape"])

        # carrega a tabela de procedimentos de aproximação perdidas em um dicionário
        #self._dct_ape = apedata.CApeData(self.model, ls_path)
        #assert self._dct_ape is not None

        # monta o nome da tabela de procedimentos de aproximação
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.apx"])

        # carrega a tabela de procedimentos de aproximação em um dicionário
        self._dct_apx = apxdata.CApxData(self.model, ls_path)
        assert self._dct_apx is not None

        # monta o nome da tabela de procedimentos de espera
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.esp"])

        # carrega a tabela de procedimentos de espera em um dicionário
        self._dct_esp = espdata.CEspData(self.model, ls_path)
        assert self._dct_esp is not None

        # monta o nome da tabela de procedimentos de ILS
        #ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.ils"])

        # carrega a tabela de procedimentos de ILS em um dicionário
        #self._dct_ils = ilsdata.CILSData(self.model, ls_path)
        #assert self._dct_ils is not None

        # monta o nome da tabela de procedimentos de subida
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.sub"])

        # carrega a tabela de procedimentos de subida em um dicionário
        self._dct_sub = subdata.CSubData(self.model, ls_path)
        assert self._dct_sub is not None

        # monta o nome da tabela de procedimentos de trajetória
        ls_path = os.path.join(self.dct_config["dir.prc"], self.dct_config["tab.trj"])

        # carrega a tabela de procedimentos de trajetória em um dicionário
        self._dct_trj = trjdata.CTrjData(self.model, ls_path)
        assert self._dct_trj is not None

        # resolve os procedimentos dos breakpoints
        self.resolv_procs()

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_event):
        """
        callback de tratamento de eventos recebidos

        @param f_event: evento recebido
        """
        return
         
    # ---------------------------------------------------------------------------------------------
    def resolv_procs(self):
        """
        resolve os procedimentos dos breakpoints. Os procedimentos, ainda no formato XXX9999 são
        validados e resolvidos
        """
        # para todos os procedimentos de aproximação...
        for l_apx in list(self._dct_apx.values()):
            # aproximação ok ?
            if l_apx is not None:
                # obtém o dicionário de esperas
                ldct_esp = self._dct_esp
                assert ldct_esp

                # tem aproximação perdida ?
                # if 'S' == l_apx.v_apx_ape:
                    # pointer para a aproximação perdida
                    # l_apx.ptr_apx_prc_ape, _ = self.find_ptr_ape(l_apx.ptr_apx_aer, l_apx.ptr_apx_pis)
                    # assert l_apx.ptr_apx_prc_ape

                # obtém o procedimento de espera pelo número
                l_apx.ptr_apx_prc_esp = lptr_prc = self._dct_esp.get(l_apx.ptr_apx_prc_esp, None)

                # espera ok ?
                if l_apx.ptr_apx_prc_esp is None:
                    # logger
                    l_log = logging.getLogger("CAirspaceNewton::resolv_procs")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E02: aproximação [{}] sem espera.".format(l_apx.i_prc_id))
                '''
                # tem ILS ?
                if 'S' == l_apx.vApxILS:
                    # obtém o pointer para o ILS
                    l_apx.pApxPrcILS = self.find_ptr_ils(l_apx.pApxPtrAer.sAerID, l_apx.pApxPtrPis.sPisID)
                    assert l_apx.pApxPrcILS
                '''
                # para todos breakpoints da aproximação...
                for l_brk in l_apx.lst_apx_brk:
                    self.get_brk_prc(l_brk)

        # para todos os procedimentos de aproximação perdida...
        for l_ape in list(self._dct_ape.values()):
            # aproximação ok ?
            if l_ape is not None:
                # obtém o dicionário de esperas
                ldct_esp = self._dct_esp
                assert ldct_esp

                # obtém o procedimento de espera pelo número
                l_ape.ptr_ape_prc_esp = lptr_prc = self._dct_esp.get(l_ape.ptr_ape_prc_esp, None)

                # espera ok ?
                if l_ape.ptr_ape_prc_esp is None:
                    # logger
                    l_log = logging.getLogger("CAirspaceNewton::resolv_procs")
                    l_log.setLevel(logging.WARNING)
                    l_log.warning("<E02: aproximação [{}] sem espera.".format(l_ape.i_prc_id))

                # para todos breakpoints da aproximação perdida...
                for l_brk in l_ape.lst_ape_brk:
                    self.get_brk_prc(l_brk)
        '''
        # para todos os procedimentos de ILS...
        for l_prc_ils in self._dct_ils.values():
            # obtém os dados da ILS
            l_ils = self._dct_ils[l_prc_ils]

            if l_ils is not None:
                # pointer do pouso
                l_ils.pIlsPtrPouso = self.findDepPtr ( l_ils.pILSPtrAer.sAerID, l_ils.pILSPtrPis.sPisID )
                assert l_ils.pIlsPtrPouso

                # obtém o procedimento e a função
                l_ils.pILSPtrPrc, l_ils.eILSPrc = self.get_ptr_prc(l_ils.eILSPrc)
        '''
        # para todos os procedimentos de subida...
        for l_sub in list(self._dct_sub.values()):
            # subida ok ?  
            if l_sub is not None:
                """
                # associa o número da decolagem
                l_sub.pSubPrcDec = self.find_prc_dep ( l_sub.pSubPtrAer.sAerID, l_sub.pSubPtrPis.sPisID )
                assert l_sub.pSubPtrDec
                """
                # para todos breakpoints da subida...
                for l_brk in l_sub.lst_sub_brk:
                    self.get_brk_prc(l_brk)

        # para todos os procedimentos de trajetória...
        for l_trj in list(self._dct_trj.values()):
            # trajetória ok ?
            if l_trj is not None:
                # para todos breakpoints da trajetória...
                for l_brk in l_trj.lst_trj_brk:
                    self.get_brk_prc(l_brk)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_ape(self):
        return self._dct_ape

    @dct_ape.setter
    def dct_ape(self, f_val):
        self._dct_ape = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_apx(self):
        return self._dct_apx

    @dct_apx.setter
    def dct_apx(self, f_val):
        self._dct_apx = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_esp(self):
        return self._dct_esp

    @dct_esp.setter
    def dct_esp(self, f_val):
        self._dct_esp = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_ils(self):
        return self._dct_ils

    @dct_ils.setter
    def dct_ils(self, f_val):
        self._dct_ils = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_sub(self):
        return self._dct_sub

    @dct_sub.setter
    def dct_sub(self, f_val):
        self._dct_sub = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_trj(self):
        return self._dct_trj

    @dct_trj.setter
    def dct_trj(self, f_val):
        self._dct_trj = f_val

# < the end >--------------------------------------------------------------------------------------
