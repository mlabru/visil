# -*- coding: utf-8 -*-
"""
trj_new

mantém as informações sobre um procedimento de trajetória

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys

# model
import model.items.prc_model as model
import model.items.brk_new as brktrj

# control
import control.events.events_basic as events
import control.control_debug as cdbg

# < class CTrjNEW >--------------------------------------------------------------------------------

class CTrjNEW(model.CPrcModel):
    """
    mantém as informações específicas sobre procedimento de trajetória

    <trajetoria nTrj="1">
        <descricao>DEP SDJD VIA SCB</descricao>
        <star>S</star>
        <proa>123</proa>

        <breakpoint nBrk="1"> ... </breakpoint>
    </trajetoria>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None, fs_ver="0001"):
        """
        @param f_model: model manager
        @param f_data: dados do procedimento de trajetória
        @param fs_ver: versão do formato
        """
        # init super class
        super(CTrjNEW, self).__init__()

        # salva o model manager localmente
        self._model = f_model
        assert self._model

        # salva o event manager localmente
        self._event = f_model.event
        assert self._event

        # herdado de CPrcModel
        # self.v_prc_ok      # (bool)
        # self.i_prc_id      # identificação do procedimento de trajetória
        # self.s_prc_desc    # descrição do procedimento de trajetória

        # star
        self._v_trj_star = False

        # proa a seguir após a trajetória
        self._f_trj_proa = 0.

        # lista de break-points da trajetória
        self._lst_trj_brk = []

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, dict):
                # cria uma procedimento de trajetória com os dados da lista
                self.load_trj(f_data, fs_ver)

            # recebeu uma procedimento de trajetória ?
            elif isinstance(f_data, CTrjNEW):
                # copia a procedimento de trajetória
                self.copy_trj(f_data)

    # ---------------------------------------------------------------------------------------------
    def copy_trj(self, f_trj):
        """
        copy constructor.
        cria uma nova procedimento de trajetória a partir de uma outra procedimento de trajetória

        @param f_trj: procedimento de trajetória a ser copiada
        """
        # check input
        assert f_trj

        # copy super class attributes
        super(CTrjNEW, self).copy_prc(f_trj)

        # flag star
        self._v_trj_star = f_trj.v_trj_star

        # lista de break-points
        self._lst_trj_brk = list(f_trj.lst_trj_brk)

    # ---------------------------------------------------------------------------------------------
    def load_trj(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de procedimento de trajetória a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do procedimento de trajetória
        @param fs_ver: versão do formato dos dados
        """
        # formato versão 0.01 ?
        if "0001" == fs_ver:
            # cria a procedimento de trajetória
            self.make_trj(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CTrjNEW::load_trj")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E01: formato desconhecido.")

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # cai fora...
            sys.exit(1)

    # ---------------------------------------------------------------------------------------------
    def make_trj(self, fdct_data):
        """
        carrega os dados de procedimento de trajetória a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados do procedimento de trajetória
        """
        # identificação da trajetória
        if "nTrj" in fdct_data:
            self.i_prc_id = int(fdct_data["nTrj"])
            self.s_prc_desc = "Trajetória {:04d}".format(fdct_data["nTrj"])            

        # descrição
        if "descricao" in fdct_data:
            self.s_prc_desc = fdct_data["descricao"]

        # star
        if "star" in fdct_data:
            self._v_trj_star = ('S' == fdct_data["star"].strip().upper())

        # proa
        if "proa" in fdct_data:
            self._f_trj_proa = float(fdct_data["proa"].strip().upper())

        # breakpoints da trajetória
        if "breakpoints" in fdct_data:
            # para todos breakpoints da trajetória...
            for l_brk in sorted(fdct_data["breakpoints"], key=lambda l_k: l_k["nBrk"]):
                # cria o breakpoint
                lo_brk = brktrj.CBrkNEW(self._model, self, l_brk)
                assert lo_brk

                # coloca o breakpoint na lista
                self._lst_trj_brk.append(lo_brk)

        # (bool)
        self.v_prc_ok = True

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_trj_brk(self):
        return self._lst_trj_brk

    @lst_trj_brk.setter
    def lst_trj_brk(self, f_val):
        self._lst_trj_brk = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_trj_proa(self):
        return self._f_trj_proa

    @f_trj_proa.setter
    def f_trj_proa(self, f_val):
        # check input
        assert 0. <= f_val <= 360.

        # salva proa
        self._f_trj_proa = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_trj_star(self):
        return False  # self._v_trj_star

    @v_trj_star.setter
    def v_trj_star(self, f_val):
        self._v_trj_star = f_val

# < the end >--------------------------------------------------------------------------------------
