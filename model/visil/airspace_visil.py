# -*- coding: utf-8 -*-
"""
airspace_visil

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import os
import sys

# PyQt4 library
from PyQt5 import QtCore
# FIXME QtXml is no longer supported.
from PyQt5 import QtXml

# libs
import libs.coords.pos_lat_lng as pll

# model
import model.newton.airspace_newton as airs
import model.common.fix as cfix
import model.common.flight_plan_item as cfpi
import model.common.holding as cesp
import model.common.runway as crun
import model.common.standard_route as stdrt

import model.items.apx_data as apxdata
import model.items.esp_data as espdata
import model.items.sub_data as subdata
import model.items.trj_data as trjdata

# < class CAirspaceVisil >------------------------------------------------------------------------------

try:
    QString = unicode
except NameError:
    # Python 3
    QString = str

try:
    QChar = unichr
except NameError:
    # Python 3
    QChar = chr

class CAirspaceVisil(airs.CAirspaceNewton):
    """
    represent an airspace
    """
    # ---------------------------------------------------------------------------------------------

    C_ARRIVAL = 0
    C_DEPARTURE = 1

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model):
        """
        read datafile for specified location (airport)
        """
        # check input
        assert f_model

        # init super class
        super(CAirspaceVisil, self).__init__(f_model)

        # herdado de CAirspaceBasic
        # self.model          # model manager 
        # self.event          # event manager
        # self.config         # config manager
        # self.dct_aer        # dicionário de aeródromos
        # self.dct_fix        # dicionário de fixos
        # self.lst_arr_dep    # lista de pousos/decolagens
                                                       
        # herdado de CAirspaceNewton
        # self.dct_apx    # procedimentos de aproximação
        # self.dct_esp    # procedimentos de espera
        # self.dct_sub    # procedimentos de subida   
        # self.dct_trj    # procedimentos de trajetória

        # dicionários locais
        self._dct_dme = {}
        self._dct_ndb = {}
        self._dct_vor = {}
        self._dct_wpt = {}

        self._dct_dep = {}
        self._dct_pso = {}

        self._dct_rwy = {}
        self._dct_arr_runways = {}
        self._dct_dep_runways = {}

        self._dct_transitions = {}

    # ---------------------------------------------------------------------------------------------
    def activateRunway(self, fs_indc, fi_mode):
        """
        add a runway for arrivals or departures
        """
        # check input
        # assert f_model

        if self.C_DEPARTURE == fi_mode:
            if fs_indc in self._dct_dep_runways:
                # return
                return

            self._dct_dep_runways.append(fs_indc)

        elif self.C_ARRIVAL == fi_mode:
            if fs_indc in self._dct_arr_runways:
                # return
                return

            self._dct_arr_runways.append(fs_indc)

    # ---------------------------------------------------------------------------------------------
    def arrival(self, fi_ndx):
        """
        return a pointer to the arrival route with specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_pso):
            # return
            return None

        # return
        return self._dct_pso[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def arrivalRunway(self, fi_ndx):
        """
        return a pointer to a string naming the arrival runway of specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_arr_runways):
            # return
            return None

        # return
        return self._dct_arr_runways[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def deactivateRunway(self, fs_indc, fi_mode):
        """
        remove a runway from available departure or arrival runways
        """
        # check input
        # assert f_model

        if self.C_DEPARTURE == fi_mode:
            if fs_indc in self._dct_dep_runways:
                self._dct_dep_runways.remove(fs_indc)

        elif self.C_ARRIVAL == fi_mode:
            if fs_indc in self._dct_arr_runways:
                self._dct_arr_runways.remove(fs_indc)

    # ---------------------------------------------------------------------------------------------
    def departure(self, fi_ndx):
        """
        return a pointer to the departure route with specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_dep):
            # return
            return None

        # return
        return self._dct_dep[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def departureRunway(self, fi_ndx):
        """
        return a pointer to a string naming the departure runway of specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_dep_runways):
            # return
            return None

        # return
        return self._dct_dep_runways[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def dme(self, fi_ndx):
        """
        return a pointer to the DME with specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_dme):
            # return
            return None

        # return
        return self._dct_dme[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def get_position(self, fs_indc):
        """
        get position of a waypoint/vor/ndb/... named as specified
        """
        # check input
        # assert f_model

        # pesquisa aeródromos/fixos
        l_pos = super(CAirspaceVisil, self).get_position(fs_indc)

        if l_pos is not None:
            # return
            return l_pos

        # pesquisa runway's
        for l_item in self._dct_rwy:
            if l_item.s_indc == fs_indc:
                # return
                return l_item.position

        # return
        return None

    # ---------------------------------------------------------------------------------------------
    def holding(self, f_val):
        """
        return a pointer to the holding with specified index
        """
        # check input
        # assert f_model

        if isinstance(f_val, int):
            # return
            return self.dct_esp.get(f_val, None)

        elif isinstance(f_val, str):
            # return
            return self.dct_esp_indc.get(f_val, None)

        # return
        return None

    # ---------------------------------------------------------------------------------------------
    def load_xml(self, fs_filename):
        """
        load xml airspace file
        """
        # check input
        # assert f_model

        # read coordinates
        ls_filename = ":/data/" + fs_filename + ".xml"

        l_data_file = QtCore.QFile(ls_filename)
        assert l_data_file is not None

        l_data_file.open(QtCore.QIODevice.ReadOnly)

        if not l_data_file.isOpen():
            # logger
            l_log = logging.getLogger("airspace::load_xml")
            l_log.setLevel(logging.NOTSET)
            l_log.fatal("<E01: failed to open {}".format(ls_filename))

            # abend
            sys.exit(1)

        # FIXME QtXml is no longer supported.
        l_xml_doc = QtXml.QDomDocument("airspace")
        assert l_xml_doc is not None

        if not l_xml_doc.setContent(l_data_file):

            l_data_file.close()

            # logger
            l_log = logging.getLogger("airspace::load_xml")
            l_log.setLevel(logging.NOTSET)
            l_log.fatal("<E02: failed to parse {}".format(ls_filename))

            # abend
            sys.exit(1)

        l_data_file.close()

        l_doc_elem = l_xml_doc.documentElement()
        assert l_doc_elem is not None

        self._f_variation, lv_ok = l_doc_elem.attribute(QString("variation"), QString("0")).toDouble()
        self._f_elevation, lv_ok = l_doc_elem.attribute(QString("elevation"), QString("0")).toDouble()

        l_node = l_doc_elem.firstChild()
        assert l_node is not None

        while not l_node.isNull():
            l_element = l_node.toElement()
            assert l_element is not None

            if not l_element.isNull():
                self._parse_dom_element(l_element)

            l_node = l_node.nextSibling()
            assert l_node is not None

    # ---------------------------------------------------------------------------------------------
    def ndb(self, fi_ndx):
        """
        return a pointer to the NDB with specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_ndb):
            # return
            return None

        # return
        return self._dct_ndb[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def _parse_dom_element(self, f_element):
        """
        helper function to the constructor, parses xml entries
        """
        # check input
        # assert f_model

        lv_ok = False

        lf_lat = 0
        lf_lng = 0

        ls_indc = f_element.text().toLocal8Bit().data()  # constData ()

        # read coordinates if available
        if f_element.hasAttribute(QString("longitude")) and \
           f_element.hasAttribute(QString("latitude")):
            lf_lat, lv_ok = f_element.attribute(QString("latitude"), QString("0")).toDouble()
            lf_lng, lv_ok = f_element.attribute(QString("longitude"), QString("0")).toDouble()

        # handle case of ARP
        if f_element.tagName() == QString("ARP"):
            self._arp = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert self._arp

        # handle case of VOR
        elif f_element.tagName() == QString("VOR"):
            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self._dct_vor.append(l_fix)

        # handle case of DME
        elif f_element.tagName() == QString("DME"):
            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self._dct_dme.append(l_fix)

        # handle case of NDB
        elif f_element.tagName() == QString("NDB"):
            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self._dct_ndb.append(l_fix)

        # handle case of WPT
        elif f_element.tagName() == QString("WPT"):
            l_fix = cfix.CFix(ls_indc, lf_lat, lf_lng)
            assert l_fix

            self._dct_wpt.append(l_fix)

        # handle case of RWY
        elif f_element.tagName() == QString("RWY"):
            l_track, lv_ok = f_element.attribute(QString("track"), QString("0")).toDouble()
            l_gp, lv_ok = f_element.attribute(QString("glidepath"), QString("0")).toDouble()

            l_rwy = crun.CRunway(ls_indc, lf_lat, lf_lng, l_track, l_gp)
            assert l_rwy is not None

            self._dct_rwy.append(l_rwy)

        # handle case of holding
        elif f_element.tagName() == QString("holding"):
            l_inb, lv_ok = f_element.attribute(QString("inbound"), QString("0")).toDouble()

            l_dir = 'l' if f_element.attribute(QString("direction"),
                           QString("0")).startsWith(QString("l")) else 'r'

            l_hold = cesp.CHolding(f_element.attribute(QString("waypoint"),
                                                       QString("")).toLocal8Bit().data(), l_inb, l_dir)
            assert l_hold is not None

            self.dct_esp.append(l_hold)

        # handle case of standard route
        elif (f_element.tagName() == QString("departure")) or \
             (f_element.tagName() == QString("arrival")) or \
             (f_element.tagName() == QString("transition")):
            ls_rt = stdrt.CStandardRoute()
            assert ls_rt is not None

            ls_rt.s_indc = f_element.attribute(QString("name"), QString("")).toLocal8Bit().data()

            l_nodeList = f_element.elementsByTagName(QString("runway"))

            for l_iI in range(l_nodeList.length()):
                l_e = l_nodeList.at(l_iI).toElement()

                if l_e.isNull():
                    continue

                ls_rt.addRunway(l_e.text().toLocal8Bit().data())

            l_nodeList = f_element.elementsByTagName(QString("waypoint"))

            for l_iI in range(l_nodeList.length()):
                l_e = l_nodeList.at(l_iI).toElement()

                if l_e.isNull():
                    continue

                l_fpItem = cfpi.CFlightPlanItem()
                assert l_fpItem is not None

                l_fpItem.s_indc = l_e.text().toLocal8Bit().data()

                l_fpItem._iSpeedConstraint, lv_ok = l_e.attribute(
                    QString("speed"), QString("0")).toInt()

                # parse the altitude constraint
                altc = l_e.attribute(QString("altitude"), QString("0"))

                if altc.endsWith(QChar('B')):
                    altc = altc.mid(0, altc.length() - 1)

                    l_fpItem._iAltConstraint, lv_ok = altc.toInt()
                    l_fpItem._iAltConstraintType = cfpi.CFlightPlanItem._OR_BELOW

                elif altc.endsWith(QChar('A')):
                    altc = altc.mid(0, altc.length() - 1)

                    l_fpItem._iAltConstraint, lv_ok = altc.toInt()
                    l_fpItem._iAltConstraintType = cfpi.CFlightPlanItem._OR_ABOVE

                else:
                    l_fpItem._iAltConstraint, lv_ok = altc.toInt()
                    l_fpItem._iAltConstraintType = cfpi.CFlightPlanItem._EXACTLY

                l_fpItem._vFlyOver = l_e.hasAttribute("flyover")

                ls_rt.addItem(l_fpItem)

            if f_element.tagName() == QString("departure"):
                self._dct_dep.append(ls_rt)

            if f_element.tagName() == QString("arrival"):
                self._dct_pso.append(ls_rt)

            if f_element.tagName() == QString("transition"):
                self._dct_transitions.append(ls_rt)

    # ---------------------------------------------------------------------------------------------
    def route(self, fs_indc):
        """
        return a pointer to the standard route with specified name
        """
        # check input
        # assert f_model

        for l_iI in range(len(self._dct_pso)):
            if self.arrival(l_iI).s_indc == fs_indc:
                # return
                return self.arrival(l_iI)

        for l_iI in range(len(self._dct_dep)):
            if self.departure(l_iI).s_indc == fs_indc:
                # return
                return self.departure(l_iI)

        for l_iI in range(len(self._dct_transitions)):
            if self.transition(l_iI).s_indc == fs_indc:
                # return
                return self.transition(l_iI)

        # return
        return None

    # ---------------------------------------------------------------------------------------------
    def runway(self, f_val):
        """
        return a pointer to the runway with specified index
        """
        # check input
        # assert f_model

        if isinstance(f_val, int):
            # return
            return self._runway_by_no(f_val)

        elif isinstance(f_val, str):
            # return
            return self._runway_by_indc(f_val)

        # return
        return None

    # ---------------------------------------------------------------------------------------------
    def _runway_by_no(self, fi_ndx):
        """
        return a pointer to the runway with specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_rwy):
            # return
            return None

        # return
        return self._dct_rwy[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def _runway_by_indc(self, fs_indc):
        """
        return a pointer to the runway with specified indc
        """
        # check input
        # assert f_model

        li_ndx = 0

        while self._runway_by_no(li_ndx):
            if self._runway_by_no(li_ndx).s_indc == fs_indc:
                # return
                return self._runway_by_no(li_ndx)

            li_ndx += 1

        # return
        return None

    # ---------------------------------------------------------------------------------------------
    def transition(self, fi_ndx):
        """
        return a pointer to the transition with specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_transitions):
            # return
            return None

        # return
        return self._dct_transitions[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def vor(self, fi_ndx):
        """
        return a pointer to the VOR with specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_vor):
            # return
            return None

        # return
        return self._dct_vor[fi_ndx]

    # ---------------------------------------------------------------------------------------------
    def waypoint(self, fi_ndx):
        """
        return a pointer to the waypoint with specified index
        """
        # check input
        # assert f_model

        if fi_ndx >= len(self._dct_wpt):
            # return
            return None

        # return
        return self._dct_wpt[fi_ndx]

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def airport(self):
        """
        pointer to the aerodrome reference point
        """
        return self._arp

    # ---------------------------------------------------------------------------------------------
    @property
    def f_elevation(self):
        """
        get aerodrome elevation
        """
        return self._f_elevation
                                            
    # @f_elevation.setter
    # def f_elevation(self, f_val):
        # """
        # set aerodrome elevation
        # """
        # self._f_elevation = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_variation(self):
        """
        get magnetic variation
        """
        return self._f_variation
                                            
    # @f_variation.setter
    # def f_variation(self, f_val):
        # """
        # set magnetic variation
        # """
        # self._f_variation = f_val

# < the end >--------------------------------------------------------------------------------------
