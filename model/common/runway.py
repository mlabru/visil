# -*- coding: utf-8 -*-
"""
runway

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# model
import model.common.fix as CFix

# < class CRunway >--------------------------------------------------------------------------------

class CRunway(CFix.CFix):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_rwy_name, ff_rwy_lat, ff_rwy_lng, ff_rwy_track, ff_rwy_gp):
        """
        define uma aerovia

        @param fs_rwy_name: nome
        @param ff_rwy_lat: latitude
        @param ff_rwy_lng: longitude
        @param ff_rwy_track: path
        @param ff_rwy_gp: glide path
        """
        # inicia a super classe
        super(CRunway, self).__init__(fs_rwy_name, ff_rwy_lat, ff_rwy_lng)

        # herdados de CFix
        # self.s_name      # nome
        # self.position    # posição

        self._f_track = ff_rwy_track
        self._f_app_angle = ff_rwy_gp

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_app_angle(self):
        """
        get glide path
        """
        return self._f_app_angle
                                            
    @f_app_angle.setter
    def f_app_angle(self, f_val):
        """
        set glide path
        """
        self._f_app_angle = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_track(self):
        """
        get track
        """
        return self._f_track
                                            
    @f_track.setter
    def f_track(self, f_val):
        """
        set track
        """
        self._f_track = f_val

# < the end >--------------------------------------------------------------------------------------
