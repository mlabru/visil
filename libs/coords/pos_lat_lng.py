# -*- coding: utf-8 -*-
"""
pos_lat_lng

revision 1.1  2015/dez  mlabru
pep8 style conventions

revision 1.0  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import copy
import logging

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < CPosLatLng >-----------------------------------------------------------------------------------

class CPosLatLng(object):
    """
    CPosLatLng
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ff_pos_lat=0., ff_pos_lng=0.):
        """
        constructor
        """
        # logger
        # M_LOG.info(">> constructor")

        # inicia a super classe
        super(CPosLatLng, self).__init__()

        # recebeu uma coordenada ?
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

    # ---------------------------------------------------------------------------------------------
    def __str__(self):
        """
        str magic method
        """
        # return
        return "{}/{}".format(self.__f_lat, self.__f_lng)

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lat(self):
        """latitude"""
        return self.__f_lat
                                            
    @f_lat.setter
    def f_lat(self, f_val):
        """latitude"""
        # check input
        assert -90. <= f_val <= 90.
        
        # save latitude
        self.__f_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lng(self):
        """longitude"""
        return self.__f_lng
                                            
    @f_lng.setter
    def f_lng(self, f_val):
        """longitude"""
        # check input
        assert -180. <= f_val <= 180.
        
        # save longitude
        self.__f_lng = f_val

# < CPosLatLngRef >--------------------------------------------------------------------------------

class CPosLatLngRef(CPosLatLng):
    """
    CPosLatLngRef
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_ref, ff_variation, ff_track, ff_dcl_mag):
        """
        constructor
        """
        # logger
        # M_LOG.info(">> constructor")

        # convert difference to radians 
        lf_dif = math.radians(ff_track - ff_variation)

        # calculate lat & lng
        lf_lat = f_ref.f_lat + ff_dcl_mag / 60. * math.cos(lf_dif)
        lf_lng = f_ref.f_lng + ff_dcl_mag / 60. * math.sin(lf_dif) / math.cos(math.radians(lf_lat))

        # inicia a super classe
        super(CPosLatLngRef, self).__init__(lf_lat, lf_lng)

# < the end >--------------------------------------------------------------------------------------
