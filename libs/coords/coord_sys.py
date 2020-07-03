# -*- coding: utf-8 -*-
"""
coord_sys
mantém os detalhes de um sistema de coordenadas

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import collections
import logging
import math
import re

# libs
from . import coord_model as model
from . import coord_conv as conv
from . import coord_defs as cdefs
from . import coord_geod as geod
from . import coord_geog as geog

# < CCoordSys >------------------------------------------------------------------------------------

class CCoordSys(model.CCoordModel):
    """
    mantém os detalhes de um sistema de coordenadas
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ff_ref_lat=cdefs.M_REF_LAT, ff_ref_lng=cdefs.M_REF_LNG, ff_dcl_mag=cdefs.M_DCL_MAG):
        """
        constructor
        """
        # init super class
        super(CCoordSys, self).__init__(ff_ref_lat, ff_ref_lng, ff_dcl_mag)

        # herdados de CCoordModel
        # self.f_ref_lat    # latitude de referência
        # self.f_ref_lng    # longitude de referência
        # self.f_dcl_mag    # declinação magnética de referência

        # coordenadas geográficas de referênica e declinação magnética
        CREF = collections.namedtuple("CREF", "lat lng decl_mag")

        self.__nt_ref = CREF(lat=ff_ref_lat, lng=ff_ref_lng, decl_mag=ff_dcl_mag)
        assert self.__nt_ref

        # coordenadas de referência
        cdefs.M_REF_LAT = ff_ref_lat
        cdefs.M_REF_LNG = ff_ref_lng
        cdefs.M_DCL_MAG = ff_dcl_mag

        # dicionário de fixos
        self.__dct_fix = None

        # dicionário de indicativos
        self.__dct_fix_indc = None

    # ---------------------------------------------------------------------------------------------
    def decl_xyz(self, ff_x, ff_y, ff_z, ff_decl=0.):
        """
        conversão de coordenadas geográficas em (x, y, z)
        """
        # retorna a coordenada declinada x, y z
        return geog.decl_xyz(ff_x, ff_y, ff_z, ff_decl)

    # ---------------------------------------------------------------------------------------------
    def from_dict(self, f_dict):
        """
        conversão de um dicionário em latitude e longitude

        @param f_dict: dicionário

        @return lat, long
        """
        # check input
        assert f_dict

        # get coords fields
        l_cpo_b = f_dict.get("cpoB", None)
        l_cpo_c = f_dict.get("cpoC", None)
        l_cpo_d = f_dict.get("cpoD", None)

        # coordenada
        li_rc, lf_lat, lf_lng = self.new_coord(f_dict["tipo"], f_dict["cpoA"], l_cpo_b, l_cpo_c, l_cpo_d)

        # retorna a coordenada em latitude e longitude
        return lf_lat, lf_lng

    # ---------------------------------------------------------------------------------------------
    def __geo_fixo(self, fs_cpo_a, f_dct_fix=None):
        """
        encontra coordenada geográfica do fixo

        @param fs_cpo_a: fixo
        @param f_dct_fix: dicionário de fixos

        @return 0 se Ok, senão -1 = NOk
        """
        if f_dct_fix is None:
            # dicionário de fixos
            f_dct_fix = self.__dct_fix

        # indicativo do fixo
        ls_fix = str(fs_cpo_a).strip().upper()

        # fixo existe no dicionário ?
        if ls_fix in f_dct_fix:
            # o fixo é válido ?
            if f_dct_fix[ls_fix].v_fix_ok:
                # latitude
                lf_lat = f_dct_fix[ls_fix].f_fix_lat

                # longitude
                lf_lng = f_dct_fix[ls_fix].f_fix_lng

                # return
                return 0, lf_lat, lf_lng

        # return
        return -1, 0., 0.

    # ---------------------------------------------------------------------------------------------
    def geo2xyz(self, f_lat, f_lng, f_alt=0.):
        """
        conversão de coordenadas geográficas em (x, y, z)
        """
        # retorna a coordenada em x, y z
        # return geog.geo2xyz(f_lat, f_lng, self.__nt_ref.lat, self.__nt_ref.lng)
        # return geod.geod2ecef(f_lat, f_lng, f_alt)
        return geog.geo2xyz_3(f_lat, f_lng, f_alt)

    # ---------------------------------------------------------------------------------------------
    def __get_fixo_by_indc(self, fs_cpo_a, f_dct_fix_indc=None):
        """
        encontra o número do fixo pelo indicativo

        @param fs_cpo_a: indicativo do fixo
        @param f_dct_fix_indc: dicionário de indicativos de fixos

        @return número do fixo ou -1
        """
        # check input
        assert fs_cpo_a

        if f_dct_fix_indc is None:
            # dicionário de indicativos
            f_dct_fix_indc = self.__dct_fix_indc

        # verifica condições de execução
        assert f_dct_fix_indc is not None
        
        # indicativo do fixo
        ls_fix = str(fs_cpo_a).strip().upper()

        # return
        return f_dct_fix_indc.get(ls_fix, -1)

    # ---------------------------------------------------------------------------------------------
    def new_coord(self, fc_tipo, fs_cpo_a, fs_cpo_b="", fs_cpo_c="", fs_cpo_d=""):
        """
        cria uma coordenada
        """
        # check input
        if fc_tipo not in cdefs.D_SET_COORD_VALIDAS:
            # logger
            l_log = logging.getLogger("CCoordSys::new_coord")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical(u"<E01: tipo de coordenada({}) inválida.".format(fc_tipo))

            # cai fora
            return -1, -90., -180.

        # inicia os valores de resposta
        lf_lat = None
        lf_lng = None

        # coordenada distância/radial
        if 'D' == fc_tipo:
            #!!TipoD(lp_ref, fp_coord)

            # obtém as coordenadas geográficas do fixo(cpoA)
            li_rc, lf_lat, lf_lng = self.__geo_fixo(fs_cpo_a)

            if 0 != li_rc:
                # logger
                l_log = logging.getLogger("CCoordSys::new_coord")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E02: fixo {} inexistente.".format(fs_cpo_a))

                # cai fora
                return li_rc, lf_lat, lf_lng

            # converte para cartesiana
            lf_x, lf_y, _ = self.geo2xyz(lf_lat, lf_lng)

            # distância(m)
            l_vd = float(fs_cpo_b) * cdefs.D_CNV_NM2M

            # radial(radianos)
            l_vr = math.radians(conv.azm2ang(float(fs_cpo_c)))

            # x, y do ponto
            lf_x += l_vd * math.cos(l_vr)
            lf_y += l_vd * math.sin(l_vr)

            # converte para geográfica
            lf_lat, lf_lng, _ = self.xyz2geo(lf_x, lf_y)

            # ok
            return li_rc, lf_lat, lf_lng

        # coordenada fixo
        elif 'F' == fc_tipo:
            # obtém as coordenadas geográficas do fixo(cpoA)
            li_rc, lf_lat, lf_lng = self.__geo_fixo(fs_cpo_a)

            if 0 != li_rc:
                # logger
                l_log = logging.getLogger("CCoordSys::new_coord")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E03: fixo {} inexistente.".format(fs_cpo_a))

            # cai fora
            return li_rc, lf_lat, lf_lng

        # coordenada geográfica formato ICA ?(formato GGGMM.mmmH)
        elif 'G' == fc_tipo:
            # latitude
            lf_lat = conv.parse_ica(str(fs_cpo_a))

            # longitude
            lf_lng = conv.parse_ica(str(fs_cpo_b))

            # ok
            return 0, lf_lat, lf_lng

        # coordenada indicativo de fixo
        elif 'I' == fc_tipo:
            # obtém o número do fixo pelo indicativo
            li_rc = self.__get_fixo_by_indc(fs_cpo_a)
            
            if li_rc < 0:
                # logger
                l_log = logging.getLogger("CCoordSys::new_coord")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E04: fixo {} inexistente.".format(fs_cpo_a))

                # cai fora
                return -1, -90., -180.

            # obtém as coordenadas geográficas do indicativo do fixo
            li_rc, lf_lat, lf_lng = self.__geo_fixo(li_rc)

            if li_rc < 0:
                # logger
                l_log = logging.getLogger("CCoordSys::new_coord")
                l_log.setLevel(logging.ERROR)
                l_log.error(u"<E05: fixo {} inexistente.".format(fs_cpo_a))

            # cai fora
            return li_rc, lf_lat, lf_lng

        # coordenada geográfica formato AISWEB ?(formato X:999:99:99.99)
        elif 'K' == fc_tipo:
            # latitude
            lf_lat = conv.parse_aisweb(str(fs_cpo_a))

            # longitude
            lf_lng = conv.parse_aisweb(str(fs_cpo_b))

            # ok
            return 0, lf_lat, lf_lng

        # coordenada geográfica formato decimal ?(formato +/-999.9999)
        elif 'L' == fc_tipo:
            # latitude
            lf_lat = float(fs_cpo_a)

            # longitude
            lf_lng = float(fs_cpo_b)

            # ok
            return 0, lf_lat, lf_lng

        # coordenada polar
        elif 'P' == fc_tipo:
            li_rc = -1

            lf_lat = -90.
            lf_lng = -180.

            # cai fora
            return li_rc, lf_lat, lf_lng

        # coordenada desconhecida
        elif 'X' == fc_tipo:
            li_rc = -1

            lf_lat = -90.
            lf_lng = -180.

            # cai fora
            return li_rc, lf_lat, lf_lng

        # senão, coordenada inválida
        else:
            # logger
            l_log = logging.getLogger("CCoordSys::new_coord")
            l_log.setLevel(logging.NOTSET)
            l_log.critical(u"<E06: tipo de coordenada({}) inválida".format(fc_tipo))

            # cai fora
            return -1, -90., -180.

        # return
        return -1, -90., -180.

    # ---------------------------------------------------------------------------------------------
    def xyz2geo(self, ff_x, ff_y, ff_z=0.):
        """
        conversão de coordenadas geográficas em (x, y, z)
        """
        # retorna a coordenada em latitude e longitude
        # return geog.xy2geo(ff_x, ff_y)
        # return geod.ecef2geod(ff_x, ff_y, ff_z)
        return geog.xyz2geo_3(ff_x, ff_y, ff_z)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_fix(self):
        """
        get dicionário de fixos
        """
        return self.__dct_fix

    @dct_fix.setter
    def dct_fix(self, f_val):
        """
        set dicionário de fixos
        """
        self.__dct_fix = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def dct_fix_indc(self):
        """
        get dicionário de indicativos
        """
        return self.__dct_fix_indc

    @dct_fix_indc.setter
    def dct_fix_indc(self, f_val):
        """
        set dicionário de indicativos
        """
        self.__dct_fix_indc = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def nt_ref(self):
        """
        get referência
        """
        return self.__nt_ref

    @nt_ref.setter
    def nt_ref(self, f_val):
        """
        set referência
        """
        self.__nt_ref = f_val

# < the end >--------------------------------------------------------------------------------------
