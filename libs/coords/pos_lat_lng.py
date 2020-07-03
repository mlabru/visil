#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
pos_lat_lng

DOCUMENT ME!

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

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import copy

# < class CPosLatLng >-----------------------------------------------------------------------------

class CPosLatLng(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ff_pos_lat=0., ff_pos_lng=0.):
        """
        DOCUMENT ME!
        """
        # inicia a super classe
        super(CPosLatLng, self).__init__()

        # recebeu um coordenada ?
        if isinstance(ff_pos_lat, CPosLatLng):
            ff_pos_lng = ff_pos_lat.f_lng
            ff_pos_lat = ff_pos_lat.f_lat

        # check input
        assert -90. <= ff_pos_lat <= 90.
        assert -180. <= ff_pos_lng <= 180.

        self.__f_lat = ff_pos_lat
        self.__f_lng = ff_pos_lng

    # ---------------------------------------------------------------------------------------------
    def copy(self):
        """
        copy constructor
        """
        # return a copy
        return copy.deepcopy(self)

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lat(self):
        """
        get latitude
        """
        return self.__f_lat
                                            
    @f_lat.setter
    def f_lat(self, f_val):
        """
        set latitude
        """
        # check input
        assert -90. <= f_val <= 90.
        
        # save latitude
        self.__f_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lng(self):
        """
        get longitude
        """
        return self.__f_lng
                                            
    @f_lng.setter
    def f_lng(self, f_val):
        """
        set longitude
        """
        # check input
        assert -180. <= f_val <= 180.
        
        # save longitude
        self.__f_lng = f_val

# < class CPosLatLngRef >--------------------------------------------------------------------------

class CPosLatLngRef(CPosLatLng):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_ref, ff_variation, ff_track, ff_dcl_mag):
        """
        DOCUMENT ME!
        """
        # convert difference to radians 
        lf_dif = math.radians(ff_track - ff_variation)

        # calculate lat & lng
        lf_lat = f_ref.f_lat + ff_dcl_mag / 60. * math.cos(lf_dif)
        lf_lng = f_ref.f_lng + ff_dcl_mag / 60. * math.sin(lf_dif) / math.cos(math.radians(lf_lat))

        # inicia a super classe
        super(CPosLatLngRef, self).__init__(lf_lat, lf_lng)

# < the end >--------------------------------------------------------------------------------------
