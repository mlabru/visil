#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
coord_model

mantém os detalhes de um sistema de coordenadas

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# libs
import libs.coords.coord_defs as cdefs
import libs.coords.coord_conv as conv
import libs.coords.coord_geod as geod

# < class CCoordModel >----------------------------------------------------------------------------

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
