# -*- coding: utf-8 -*-
"""
coord_model
mantém os detalhes de um sistema de coordenadas

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# libs
from . import coord_defs as cdefs
from . import coord_conv as conv
from . import coord_geod as geod

# < CCoordModel >----------------------------------------------------------------------------------

class CCoordModel(object):
    """
    mantém os detalhes de um sistema de coordenadas
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ff_ref_lat=cdefs.M_REF_LAT, ff_ref_lng=cdefs.M_REF_LNG, ff_dcl_mag=cdefs.M_DCL_MAG):
        """
        cria um sistema de coordenadas
        """
        # inicia super classe
        super(CCoordModel, self).__init__()

        # coordenadas geográficas de referênica
        self.__f_ref_lat = ff_ref_lat
        self.__f_ref_lng = ff_ref_lng

        # declinação magnética
        self.__f_dcl_mag = ff_dcl_mag

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_ref_lat(self):
        """
        get latitude de referênica
        """
        return self.__f_ref_lat

    @f_ref_lat.setter
    def f_ref_lat(self, f_val):
        """
        set latitude de referênica
        """
        self.__f_ref_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_ref_lng(self):
        """
        get longitude de referênica
        """
        return self.__f_ref_lng

    @f_ref_lng.setter
    def f_ref_lng(self, f_val):
        """
        set longitude de referênica
        """
        self.__f_ref_lng = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_dcl_mag(self):
        """
        get declinação magnética
        """
        return self.__f_dcl_mag

    @f_dcl_mag.setter
    def f_dcl_mag(self, f_val):
        """
        set declinação magnética
        """
        self.__f_dcl_mag = f_val

# < the end >--------------------------------------------------------------------------------------
