# -*- coding: utf-8 -*-
"""
aircraft_basic

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# Python library
import random
import sys
import time

# libs
import libs.coords.pos_lat_lng as pll

# model
import model.common.tMath as tmath
import model.common.aircraft as sanv

# control
import control.control_debug as cdbg

# < class CAircraftBasic >-------------------------------------------------------------------------

class CAircraftBasic(sanv.CAircraft):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_emula, f_data=None):
        """
        constructor
        """
        # check input
        assert f_emula

        # inicia a super classe
        super(CAircraftBasic, self).__init__()

        # herdado de CAircraft
        # self.adiru          # air data inertial reference unit
        # self.s_callsign     # callsign
        # self.s_icao_addr    # icao address
        # self.pos            # posição lat/lng
        # self.s_status       # situação

        # herdado de CADIRU
        # self.adiru.f_alt             # altitude
        # self.adiru.f_ias             # instrument air speed
        # self.adiru.f_true_heading    # proa em relação ao norte verdadeiro
        # self.adiru.f_vel             # velocidade

        # emulation model
        self._emula = f_emula

        # import foreign objects
        self._airspace = f_emula.model.airspace

        # create vectors
        self._lst_trail = []
        self._lst_instructions = []

        self._v_uninitialized = True

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, list):
                # cria uma aeronave com os dados da lista
                self.make_aircraft(f_data, True)

            # recebeu uma aeronave ?
            elif isinstance(f_data, CAircraftBasic):
                # copia a aeronave
                # self.copy_aircraft(f_data)
                pass

            # senão, inicia os dados locais
            else:
                # set initial values
                self.adiru.f_alt = 10000.
                self.adiru.f_ias = 230.
                self.adiru.f_vel = 230.
                self.adiru.f_true_heading = 0.

    # ---------------------------------------------------------------------------------------------
    def init_position(self, f_oPos):
        """
        set initial position and radar position
        """
        # check input
        # assert f_control

    # ---------------------------------------------------------------------------------------------
    def isClimbing(self):
        """
        is the aircraft climbing ?
        """
        # TODO
        return False

    # ---------------------------------------------------------------------------------------------
    def isDescending(self):
        """
        is the aircraft descending ?
        """
        # TODO
        return False

    # ---------------------------------------------------------------------------------------------
    def make_aircraft(self, f_data, fv_initial=False):
        """
        create an aircraft from list
        """
        # check input
        assert f_data is not None

        # índice de dados
        li_ndx = 0

        # identificacao da aeronave
        self.s_icao_addr = str(f_data[li_ndx])
        li_ndx += 1

        # código transponder (ssr)
        self._i_ssr = int(f_data[li_ndx])
        li_ndx += 1

        # spi
        li_spi = int(f_data[li_ndx])
        li_ndx += 1

        # altitude (m)
        self.adiru.f_alt = float(f_data[li_ndx])
        li_ndx += 1

        # latitude
        lf_lat = float(f_data[li_ndx])
        li_ndx += 1

        # longitude
        lf_lng = float(f_data[li_ndx])
        li_ndx += 1

        self.pos = pll.CPosLatLng(lf_lat, lf_lng)
        assert self.pos

        # if fv_initial:
            # self.pos = pll.CPosLatLng(lf_lat, lf_lng)
            # assert self.pos

        # velocidade (kt)
        lf_vel = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_ias = lf_vel
        self.adiru.f_vel = lf_vel

        # razão de subida
        self._f_raz = float(f_data[li_ndx])
        li_ndx += 1

        # proa
        lf_pro = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_true_heading = lf_pro

        # callsign
        self.s_callsign = str(f_data[li_ndx])
        li_ndx += 1

        # performance
        self._s_prf = str(f_data[li_ndx])
        li_ndx += 1

        # hora
        self._i_hora = float(f_data[li_ndx])
        li_ndx += 1

    # ---------------------------------------------------------------------------------------------
    def radar_ground_speed(self):
        """
        determine groundspeed from radar history
        """
        # clear to go ?
        if len(self._lst_trail) < 3:
            # return
            return 0

        # calculate ground speed
        l_gs = tmath.distLL(self._lst_trail[-1], self.pos) / (self._f_trail_interval / 1000.) * 3600.

        # return
        return l_gs

    # ---------------------------------------------------------------------------------------------
    def radar_magnetic_track(self):
        """
        determine magnetic track from radar history
        """
        # clear to go ?
        if len(self._lst_trail) < 3:
            # return
            return 0

        # calculate position magnectic declination 
        lf_dcl_mag = self._emula.model.geomag.GeoMag(self.pos.f_lat, self.pos.f_lng)
        assert lf_dcl_mag

        # cdbg.M_DBG.debug("lf_dcl_mag.dec:[{}]".format(lf_dcl_mag.dec))
                        
        # determine magnetic track from radar history
        # li_mag_trk = round(tmath.track(self._lst_trail[-1], self.pos) + self._airspace.f_variation, 0)
 
        # cdbg.M_DBG.debug("self.adiru.f_true_heading:[{}]".format(self.adiru.f_true_heading))

        # determine magnetic track from radar history
        li_mag_trk = (round(tmath.track(self._lst_trail[-1], self.pos) + lf_dcl_mag.dec, 0) + 360) % 360
        # cdbg.M_DBG.debug("li_mag_trk (2):[{}]".format(li_mag_trk))

        # return
        return li_mag_trk

    # ---------------------------------------------------------------------------------------------
    def trail(self, fi_ndx):
        """
        get position of radar history point #n
        """
        # exists trail ?
        if not self._lst_trail:
            # return
            return None

        # index out of range ?
        if fi_ndx >= len(self._lst_trail):
            # return
            return None

        # return
        return self._lst_trail[len(self._lst_trail) - 1 - fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def update_data(self, f_data):
        """
        update data
        """
        # update aircraft data
        self.make_aircraft(f_data)

    # ---------------------------------------------------------------------------------------------
    def update_radar_position(self, ff_tim):
        """
        get new radar position, and push old one into history
        """
        # última posção conhecida
        l_last_pos = pll.CPosLatLng(self.pos)
        assert l_last_pos is not None

        # coloca no rastro
        self._lst_trail.append(l_last_pos)

        # atualiza a posição da aeronave
        self.pos = self.adiru.pos

        # intervalo do rastro
        self._f_trail_interval = ff_tim

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def i_hora(self):
        """
        get hora
        """
        return self._i_hora

    @i_hora.setter
    def i_hora(self, f_val):
        """
        set hora
        """
        self._i_hora = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_prf(self):
        """
        get performance
        """
        return self._s_prf

    @s_prf.setter
    def s_prf(self, f_val):
        """
        set performance
        """
        self._s_prf = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_raz(self):
        """
        get razão de descida/subida
        """
        return self._f_raz

    @f_raz.setter
    def f_raz(self, f_val):
        """
        set razão de descida/subida
        """
        self._f_raz = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_rumo_mag(self):
        """
        get rumo magnético
        """
        # calculate position magnectic declination 
        lf_dcl_mag = self._emula.model.geomag.GeoMag(self.pos.f_lat, self.pos.f_lng)
        assert lf_dcl_mag

        # determine magnetic track
        lf_mag_trk = (self.adiru.f_true_heading + lf_dcl_mag.dec + 360.) % 360.
        # cdbg.M_DBG.debug("li_mag_trk (1):[{}]".format(li_mag_trk))

        # return
        return lf_mag_trk

    # ---------------------------------------------------------------------------------------------
    @property
    def i_ssr(self):
        """
        get transponder code
        """
        return self._i_ssr

    @i_ssr.setter
    def i_ssr(self, f_val):
        """
        set transponder code
        """
        self._i_ssr = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_trail(self):
        """
        get trail list
        """
        return self._lst_trail

    @lst_trail.setter
    def lst_trail(self, f_val):
        """
        set trail list
        """
        self._lst_trail = f_val

# < the end >--------------------------------------------------------------------------------------
