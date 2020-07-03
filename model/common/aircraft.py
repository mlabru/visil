# -*- coding: utf-8 -*-
"""
aircraft
mantém os detalhes de uma aeronave

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import copy

# libs
import libs.coords.pos_lat_lng as pll

# model
import model.common.adiru as cadi

# < class CAircraft >------------------------------------------------------------------------------

class CAircraft(object):
    """
    mantém as informações específicas sobre uma aeronave
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_id="NOADDR"):
        """
        @param  fs_id: identificação da aeronave
        """
        # check input
        assert fs_id

        # air data inertial reference unit
        self._adiru = cadi.CADIRU()
        assert self._adiru

        # callsign
        self._s_callsign = "NONAME"

        # icao address
        self._s_icao_addr = fs_id

        # posição lat/lng
        self._pos = pll.CPosLatLng()
        assert self._pos is not None

        # status
        self._s_status = "N/A"

    # ---------------------------------------------------------------------------------------------
    def copy(self):
        """
        copy constructor
        """
        # return a copy
        return copy.deepcopy(self)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def adiru(self):
        """
        get air data inertial reference unit
        """
        return self._adiru

    @adiru.setter
    def adiru(self, f_val):
        """
        set air data inertial reference unit
        """
        self._adiru = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_alt(self):
        """
        get altitude
        """
        return self._adiru.f_alt

    @f_alt.setter
    def f_alt(self, f_val):
        """
        set altitude
        """
        self._adiru.f_alt = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_callsign(self):
        """
        get callsign
        """
        return self._s_callsign  # .decode ( "utf-8" )

    @s_callsign.setter
    def s_callsign(self, f_val):
        """
        set callsign
        """
        self._s_callsign = f_val.strip()  # .encode ( "utf-8" )

    # ---------------------------------------------------------------------------------------------
    @property
    def f_ias(self):
        """
        get ias (instrument air speed)
        """
        return self._adiru.f_ias

    @f_ias.setter
    def f_ias(self, f_val):
        """
        set ias (instrument air speed)
        """
        self._adiru.f_ias = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_icao_addr(self):
        """
        get ICAO address
        """
        return self._s_icao_addr

    @s_icao_addr.setter
    def s_icao_addr(self, f_val):
        """
        set ICAO address
        """
        self._s_icao_addr = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lat(self):
        """
        get latitude
        """
        return self._pos.f_lat

    @f_lat.setter
    def f_lat(self, f_val):
        """
        set latitude
        """
        self._pos.f_lat = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lng(self):
        """
        get longitude
        """
        return self._pos.f_lng

    @f_lng.setter
    def f_lng(self, f_val):
        """
        set longitude
        """
        self._pos.f_lng = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def pos(self):
        """
        get position
        """
        return self._pos

    @pos.setter
    def pos(self, f_val):
        """
        set position
        """
        self._pos = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_status(self):
        """
        get status
        """
        return self._s_status

    @s_status.setter
    def s_status(self, f_val):
        """
        set status
        """
        self._s_status = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_true_heading(self):
        """
        get true heading
        """
        return self._adiru.f_true_heading

    @f_true_heading.setter
    def f_true_heading(self, f_val):
        """
        set true heading
        """
        self._adiru.f_true_heading = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_vel(self):
        """
        get velocidade
        """
        return self._adiru.f_vel

    @f_vel.setter
    def f_vel(self, f_val):
        """
        set velocidade
        """
        self._adiru.f_vel = f_val

# < the end >--------------------------------------------------------------------------------------
