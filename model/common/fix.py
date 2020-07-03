# -*- coding: utf-8 -*-
"""
fix

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# libs
import libs.coords.pos_lat_lng as pll

# < class CFix >-----------------------------------------------------------------------------------

class CFix(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_fix_indc="NONAME", ff_fix_lat=0., ff_fix_lng=0.):
        """
        define um navaid
                
        @param fs_fix_indc: nome
        @param ff_fix_lat: latitude
        @param ff_fix_lng: longitude
        """
        # inicia a super classe
        super(CFix, self).__init__()

        self._s_indc = fs_fix_indc

        self._position = pll.CPosLatLng(ff_fix_lat, ff_fix_lng)
        assert self._position

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_indc(self):
        """
        get indicativo
        """
        return self._s_indc
                                            
    @s_indc.setter
    def s_indc(self, f_val):
        """
        set indicativo
        """
        self._s_indc = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def position(self):
        """
        get posição
        """
        return self._position
                                            
    @position.setter
    def position(self, f_val):
        """
        set posição
        """
        self._position = f_val

# < the end >--------------------------------------------------------------------------------------
