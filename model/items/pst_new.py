# -*- coding: utf-8 -*-
"""
pst_new

mantém as informações sobre uma pista

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
import model.items.pst_model as model

# control
import control.events.events_basic as events

# < class CPstNEW >--------------------------------------------------------------------------------

class CPstNEW(model.CPstModel):
    """
    mantém as informações específicas sobre pista
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_aer, f_data=None, fs_ver="0001"):
        """
        @param f_model: model manager
        @param f_aer: aeródromo
        @param f_data: dados da pista
        @param fs_ver: versão do formato
        """
        # check input
        assert f_aer

        # init super class
        super(CPstNEW, self).__init__()

        # salva o model manager localmente
        self._model = f_model
        assert self._model

        # salva o event manager localmente
        self._event = f_model.event
        assert self._event

        # herdado de CPstModel
        # self.v_pst_ok      # (bool)
        # self.s_pst_indc    # identificação da pista (indicativo)
        # self.f_pst_rumo    # rumo magnético da pista
        # self.f_pst_true    # rumo verdadeiro da pista
        # self.f_pst_x       # X (m)
        # self.f_pst_y       # Y (m)
        # self.f_pst_z       # Y (m)/elevação

        # salva o aeródromo localmente
        self._ptr_pst_aer = f_aer

        # latitude (gr)
        self._f_pst_lat = f_aer.f_aer_lat
        # longitude (gr)
        self._f_pst_lng = f_aer.f_aer_lng
        # elevação (m)
        self._f_pst_elev = f_aer.f_aer_elev

        # cabeceira oposta
        self._f_pst_cab_opos_x = 0.
        self._f_pst_cab_opos_y = 0.

        self._f_pst_cab_opos_lat = f_aer.f_aer_lat
        self._f_pst_cab_opos_lng = f_aer.f_aer_lng

        # indicativo de pista em uso
        self._v_pst_em_uso = False

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, dict):
                # cria uma pista com os dados da lista
                self.load_pst(f_data, fs_ver)

            # recebeu uma pista ?
            elif isinstance(f_data, CPstNEW):
                # copia a pista
                self.copy_pst(f_data)

    # ---------------------------------------------------------------------------------------------
    def copy_pst(self, f_pst):
        """
        copy constructor
        cria uma nova pista a partir de uma outra pista

        @param f_pst: pista a ser copiada
        """
        # check input
        assert f_pst

        # copy super class attributes
        super(CPstNEW, self).copy_pst(f_pst)

        # salva o aeródromo localmente
        self._ptr_pst_aer = f_pst.ptr_pst_aer

        # latitude
        self._f_pst_lat = f_pst.f_pst_lat
        # longitude
        self._f_pst_lng = f_pst.f_pst_lng
        # elevação
        self._f_pst_elev = f_pst.f_pst_elev

        # cabeceira oposta
        self._f_pst_cab_opos_x = f_pst.f_pst_cab_opos_x
        self._f_pst_cab_opos_y = f_pst.f_pst_cab_opos_y

        self._f_pst_cab_opos_lat = f_pst.f_pst_cab_opos_lat
        self._f_pst_cab_opos_lng = f_pst.f_pst_cab_opos_lng

        # indicativo de pista em uso
        self._v_pst_em_uso = f_pst.v_pst_em_uso

    # ---------------------------------------------------------------------------------------------
    def load_pst(self, fdct_data, fs_ver="0001"):
        """
        carrega os dados de pista a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados da pista
        @param fs_ver: versão do formato dos dados
        """
        # formato versão 0.01 ?
        if "0001" == fs_ver:
            # cria a pista
            self.make_pst(fdct_data)

        # senão, formato desconhecido
        else:
            # logger
            l_log = logging.getLogger("CPstNEW::load_pst")
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
    def make_pst(self, fdct_data):
        """
        carrega os dados de pista a partir de um dicionário (formato 0001)

        @param fdct_data: dicionário com os dados da pista
        """
        # identificação da pista
        if "nPst" in fdct_data:
            self.s_pst_indc = fdct_data["nPst"]

        # coord (posição) (lat, lng)
        if "coord" in fdct_data:
            # latitude e longitude
            self._f_pst_lat, self._f_pst_lng = self._model.coords.from_dict(fdct_data["coord"])

            # cabeceira oposta
            self._f_pst_cab_opos_lat = self._f_pst_lat
            self._f_pst_cab_opos_lng = self._f_pst_lng

            # converte para xyz
            self.f_pst_x, self.f_pst_y, self.f_pst_z = self._model.coords.geo2xyz(self._f_pst_lat, self._f_pst_lng, 0.)

            # cabeceira oposta
            self._f_pst_cab_opos_x = self.f_pst_x
            self._f_pst_cab_opos_y = self.f_pst_y

            # elevação
            self._f_pst_elev = self._ptr_pst_aer.f_aer_elev

        # rumo magnético (gr)
        if "rumo" in fdct_data:
            # rumo magnético (gr)
            self.f_pst_rumo = float(fdct_data["rumo"])

        # (bool)
        self.v_pst_ok = True

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_cab_opos_lat(self):
        """
        get latitude da cabeceira oposta
        """
        return self._f_pst_cab_opos_lat

    @f_pst_cab_opos_lat.setter
    def f_pst_cab_opos_lat(self, f_val):
        """
        set latitude da cabeceira oposta
        """
        self._f_pst_cab_opos_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_cab_opos_lng(self):
        """
        get longitude da cabeceira oposta
        """
        return self._f_pst_cab_opos_lng

    @f_pst_cab_opos_lng.setter
    def f_pst_cab_opos_lng(self, f_val):
        """
        set longitude da cabeceira oposta
        """
        self._f_pst_cab_opos_lng = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_cab_opos_x(self):
        """
        get cabeceira oposta X
        """
        return self._f_pst_cab_opos_x

    @f_pst_cab_opos_x.setter
    def f_pst_cab_opos_x(self, f_val):
        """
        set cabeceira oposta X
        """
        self._f_pst_cab_opos_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_cab_opos_y(self):
        """
        get cabeceira oposta Y
        """
        return self._f_pst_cab_opos_y

    @f_pst_cab_opos_y.setter
    def f_pst_cab_opos_y(self, f_val):
        """
        set cabeceira oposta Y
        """
        self._f_pst_cab_opos_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_elev(self):
        """
        get elevação
        """
        return self._f_pst_elev

    @f_pst_elev.setter
    def f_pst_elev(self, f_val):
        """
        set elevação
        """
        self._f_pst_elev = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_pst_em_uso(self):
        """
        get indicativo de pista em uso
        """
        return self._v_pst_em_uso

    @v_pst_em_uso.setter
    def v_pst_em_uso(self, f_val):
        """
        set indicativo de pista em uso
        """
        self._v_pst_em_uso = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_lat(self):
        """
        get latitude
        """
        return self._f_pst_lat

    @f_pst_lat.setter
    def f_pst_lat(self, f_val):
        """
        set latitude
        """
        self._f_pst_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_lng(self):
        """
        get longitude
        """
        return self._f_pst_lng

    @f_pst_lng.setter
    def f_pst_lng(self, f_val):
        """
        set longitude
        """
        self._f_pst_lng = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ptr_pst_aer(self):
        """
        get aeródromo
        """
        return self._ptr_pst_aer

    @ptr_pst_aer.setter
    def ptr_pst_aer(self, f_val):
        """
        set aeródromo
        """
        self._ptr_pst_aer = f_val

# < the end >--------------------------------------------------------------------------------------
