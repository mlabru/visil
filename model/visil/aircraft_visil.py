# -*- coding: utf-8 -*-
"""
aircraft_visil

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# Python library
import logging
import random
import sys
import time

# libs
import libs.coords.pos_lat_lng as pll

# model
import model.common.tMath as tmath
import model.common.aircraft_basic as sanv
import model.common.strip_model as mstp

# control
import control.control_debug as cdbg

# < class CAircraftVisil >-------------------------------------------------------------------------

class CAircraftVisil(sanv.CAircraftBasic):
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
        super(CAircraftVisil, self).__init__(f_emula, f_data)

        # herdado de CAircraft
        # self.adiru          # air data inertial reference unit
        # self.s_callsign     # callsign
        # self.s_icao_addr    # icao address
        # self.pos            # posição lat/lng
        # self.s_status       # situação

        # herdado de CAircraftBasic
        # self.airspace            # airspace
        # self.lst_trail           # trail list
        # self.lst_instructions    # instructions list
        # self.v_uninitialized     # flag uninitialized
        
        # self._weather = f_emula.model.weather
        # assert self._weather

        # create aircraft components

        #self._mcp = CMCP.CMCP(self._airspace.f_variation)
        #assert self._mcp is not None

        #self._fms = CFMS.CFMS(self, self._airspace, self._weather, self.adiru, self._mcp)
        #assert self._fms is not None

        #self._auto_pilot = CAutoPilot.CAutoPilot(self.adiru, self._fms, self._mcp)
        #assert self._auto_pilot is not None

        #self._fms.setAutoPilot(self._auto_pilot)

        #self._pilot = CPilot.CPilot(self, self._airspace, self._weather, self._fms, self._mcp)
        #assert self._pilot is not None

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, list):
                # cria uma aeronave com os dados da lista
                self._make_aircraft(f_data, True)

            # recebeu uma aeronave ?
            elif isinstance(f_data, CAircraftVisil):
                # copia a aeronave
                # self.copy_aircraft(f_data)
                pass

            # senão, inicia os dados locais
            else:
                # set initial values
                self.adiru.f_alt = 1000.
                self.adiru.f_ias = 230.
                self.adiru.f_true_heading = 0.

    # ---------------------------------------------------------------------------------------------
    def fly(self, t):
        """
        do periodic updates (position, altitude, speed,...) variable t specifies time in microseconds
        """
        # check input
        # assert f_control
        '''
        tas = self._fms.TAS()

        # any instructions ?
        for l_inst in self.lst_instructions:
            if l_inst._oReactTime <= time.time():
                self._pilot.accept(l_inst)
                self.lst_instructions.remove(l_inst)

        # make FMS decisions
        self._fms.decide()

        # update Position in two halves
        self._auto_pilot.move(self.adiru.f_true_heading, tas, t / 2000.)
        # self._auto_pilot.move(tmath.trackOpposite(self._weather.get_wind_dir(self.adiru.f_alt)),
        #                                           self._weather.get_wind_spd(self.adiru.f_alt), t / 2000.)
        self._auto_pilot.move(tmath.trackOpposite(0.), 0., t / 2000.)

        target_hdg = self._mcp.targetHeading()

        if self._mcp.lateralMode() != CMCP.CMCP._C_LMODE_HDG:
            target_hdg = self._fms.targetHeading()

        # change HDG
        if self.adiru.f_true_heading != target_hdg:
            self._auto_pilot.turn(target_hdg, t)

        # update Position in two halves
        self._auto_pilot.move(self.adiru.f_true_heading, tas, t / 2000.)
        # self._auto_pilot.move(tmath.trackOpposite(self._weather.get_wind_dir(self.adiru.f_alt)),
        #                                           self._weather.get_wind_spd(self.adiru.f_alt), t / 2000.)
        self._auto_pilot.move(tmath.trackOpposite(0.), 0., t / 2000.)
        '''
    # ---------------------------------------------------------------------------------------------
    def get_strip(self):
        """
        return flight strip
        """
        # return
        return mstp.CStripModel()

    # ---------------------------------------------------------------------------------------------
    def _make_aircraft(self, f_data, fv_initial=False):
        """
        create an aircraft from list
        """
        # check input
        assert f_data is not None

        # inicia o indice de dados
        li_ndx = 0

        # identificação da aeronave
        li_id = int(f_data[li_ndx])
        li_ndx += 1

        # código transponder (ssr)
        li_ssr = int(f_data[li_ndx])
        li_ndx += 1

        # spi
        li_spi = int(f_data[li_ndx])
        li_ndx += 1

        # altitude
        lf_alt = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_alt = lf_alt
        # cdbg.M_DBG.debug("_make_aircraft: self.adiru.f_alt: {}".format(self.adiru.f_alt))

        # latitude
        lf_lat = float(f_data[li_ndx])
        li_ndx += 1

        # longitude
        lf_lng = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.pos = pll.CPosLatLng(lf_lat, lf_lng)
        assert self.adiru.pos

        if fv_initial:
            self.pos = pll.CPosLatLng(lf_lat, lf_lng)
            assert self.pos

        # velocidade
        lf_vel = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_ias = lf_vel
        # cdbg.M_DBG.debug("_make_aircraft: self.adiru.f_ias: {}".format(self.adiru.f_ias))

        # razão de subida
        lf_raz = float(f_data[li_ndx])
        li_ndx += 1

        # proa
        lf_pro = float(f_data[li_ndx])
        li_ndx += 1

        self.adiru.f_true_heading = lf_pro
        # cdbg.M_DBG.debug("_make_aircraft: self.adiru.f_true_heading: {}".format(self.adiru.f_true_heading))

        # callsign
        ls_ind = str(f_data[li_ndx])
        li_ndx += 1

        self.s_callsign = ls_ind

        # performance
        ls_prf = str(f_data[li_ndx])
        li_ndx += 1

        # hora
        lf_tim = float(f_data[li_ndx])
        li_ndx += 1

    # ---------------------------------------------------------------------------------------------
    def update_data(self, f_data):
        """
        update data
        """
        # update aircraft data
        self._make_aircraft(f_data)

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_alt(self):
        """
        get altitude
        """
        return self.adiru.f_alt

    # ---------------------------------------------------------------------------------------------
    @property
    def f_ias(self):
        """
        get instrument air speed
        """
        return self.adiru.f_ias

    # ---------------------------------------------------------------------------------------------
    @property
    def position(self):
        """
        get last position
        """
        return self.pos

    # ---------------------------------------------------------------------------------------------
    @property
    def f_true_heading(self):
        """
        get instrument air speed
        """
        return self.adiru.f_true_heading

# < the end >--------------------------------------------------------------------------------------
