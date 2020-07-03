# -*- coding: utf-8 -*-
"""
slate_radar

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import math

# PyQt library
from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui, QtWidgets

# libs
import libs.coords.pos_lat_lng as pll
import libs.coords.pos_xy as pxy

# model
import model.common.glb_data as gdata
import model.common.tMath as tMath

import model.newton.defs_newton as ldefs

# view
import view.common.paint_engine as peng
import view.common.viewport as vwp

# < class CSlateRadar >----------------------------------------------------------------------------

class CSlateRadar(QtWidgets.QWidget):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------

    C_LMODE_APP = 0
    C_LMODE_DCT = 1
    C_LMODE_HDG = 2
    C_LMODE_RTE = 3

    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_control, f_parent=None):
        """
        constructor
        
        @param f_control: control manager
        @param f_parent: parent widget
        """
        # check input
        assert f_control
        assert f_parent

        # init super classe
        super(CSlateRadar, self).__init__(f_parent)

        # save control manager 
        self._control = f_control

        # save QMainWindow
        self._parent = f_parent

        # save model manager 
        l_model = f_control.model

        # save event manager
        self._event = f_control.event

        # register as event listener
        self._event.register_listener(self)

        # save flight model
        # self._emula = l_model.emula

        self._f_radar_vector = 0.
        self._i_lateral_mode = self.C_LMODE_APP

        self._s_direct = ""
        self._s_route = ""
        self._s_approach = ""

        # flight dictionary
        self._dct_flight = l_model.emula.dct_flight
                        
        # save airspace
        self._airspace = l_model.airspace

        # save weather
        # self._weather = l_model.getWeather()

        # create a viewport
        self._viewport = vwp.CViewport(self.width() - 1, self.height() - 1)
        assert self._viewport

        # get reference center
        self._viewport.center = self._airspace.get_position("SBBR") #16

        # create paint engine
        self._paint_engine = peng.CPaintEngine()
        assert self._paint_engine

        self._paint_engine.setColors(False)

        # get color background area
        l_clr = None  # colorMngr.getColor("WND_MAIN_AREA_BKGRND")

        # QBrush
        self._brush = QtGui.QBrush(gdata.G_DCT_COLORS["radar_background"])
        assert self._brush

        # QPen
        self._pen = QtGui.QPen()
        assert self._pen

        # QRect
        self._rect_invalid = QtCore.QRect()
        assert self._rect_invalid is not None

        # fast track simulation speed
        self._f_simulation_speed = 1.

        # radar timer (4s cycle)
        self._f_radar_interval = 4000. / self._f_simulation_speed
        self._i_radar_timer = self.startTimer(round(self._f_radar_interval, 0))

        # update timer (0.4s cycle)
        self._f_update_interval = 400. / self._f_simulation_speed
        self._i_aircraft_timer = self.startTimer(round(self._f_update_interval, 0))

        self._i_active_ac = -1
        self._v_paused = False

        # setup UI
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setCursor(QtCore.Qt.CrossCursor)

        self.setMouseTracking(True)
        self.setStyleSheet("background-color: rgb(0, 0, 0);")

        # monta a lista de aeronaves ativas
        #self._build_aircraft_list()

    # ---------------------------------------------------------------------------------------------
    def hideLateral(self):
        """
        DOCUMENT ME!
        """
        self._i_active_ac = -1
        self.setMouseTracking(False)

    # ---------------------------------------------------------------------------------------------
    def makeApproach(self):
        """
        DOCUMENT ME!
        """
        # check input
        # assert f_control

        l_oXY = pxy.CPosXY(self._iMouseX, self._iMouseY)
        assert l_oXY is not None

        pos = self._viewport.translate_xy(l_oXY)

        l_fClosest_r = 1000000
        l_sClosest = ""

        i = 0

        while (self._airspace.arrivalRunway(i)):
            pos1 = self._airspace.getPosition(self._airspace.arrivalRunway(i))

            d = tMath.distLL(pos, pos1)
            a = tMath.trackDelta(self._airspace.runway(self._airspace.arrivalRunway(i)).track(),
                tMath.track(pos,pos1))

            r = d * tMath.dsin(abs(a))

            if ((r < l_fClosest_r) and (abs(a) < 90)):
                l_sClosest = self._airspace.arrivalRunway(i)
                l_fClosest_r = r

            i += 1

        self._s_approach = l_sClosest
        self._i_lateral_mode = self.C_LMODE_APP

    # ---------------------------------------------------------------------------------------------
    def makeDirect(self):
        """
        DOCUMENT ME!
        """
        # check input
        # assert f_control

        # get mouse position
        l_oXY = pxy.CPosXY(self._iMouseX, self._iMouseY)
        assert l_oXY is not None

        # converte as coordenadas de tela para mapa
        pos = self._viewport.translate_xy(l_oXY)

        # inicia variáveis
        l_sClosest = ""
        l_fClosest_r = 1000000

        # primeiro waypoint
        i = 0
        wpt = self._airspace.waypoint(0)

        # scan all waypoints
        while wpt is not None:
            # calcula a distância do mouse ao waypoint
            r = tMath.distLL(pos, wpt.position())

            # distância menor que a anterior ?
            if r < l_fClosest_r:
                # this is the new closest waypoint
                l_sClosest = wpt._sName()
                l_fClosest_r = r

            # next waypoint
            i += 1
            wpt = self._airspace.waypoint(i)

        # primeiro vor
        i = 0
        wpt = self._airspace.vor(0)

        # scan all vor's
        while wpt is not None:
            # calcula a distância do mouse ao vor
            r = tMath.distLL(pos, wpt.position())

            # distância menor que a anterior ?
            if r < l_fClosest_r:
                # this is the new closest element
                l_sClosest = wpt._sName()
                l_fClosest_r = r

            # next vor
            i += 1
            wpt = self._airspace.vor(i)

        # primeiro ndb
        i = 0
        wpt = self._airspace.ndb(0)

        # scan all ndb's
        while wpt is not None:
            # calcula a distância do mouse ao ndb
            r = tMath.distLL(pos, wpt.position())

            # distância menor que a anterior ?
            if r < l_fClosest_r:
                # this is the new closest element
                l_sClosest = wpt._sName()
                l_fClosest_r = r

            # next ndb
            i += 1
            wpt = self._airspace.ndb(i)

        # salva nome do elemento mais próximo do mouse
        self._s_direct = l_sClosest
        self._i_lateral_mode = self.C_LMODE_DCT

    # ---------------------------------------------------------------------------------------------
    def makeRoute(self):
        """
        DOCUMENT ME!
        """
        # check input
        # assert f_control

        # get mouse position
        l_oXY = pxy.CPosXY(self._iMouseX, self._iMouseY)
        assert l_oXY is not None

        # converte as coordenadas de tela para mapa
        pos = self._viewport.translate_xy(l_oXY)

        # inicia variáveis
        l_sClosest = ""
        l_fClosest_r = 1000000

        # first arrival
        i = 0
        srt = self._airspace.arrival(0)

        # scan all arrival's
        while srt is not None:
            # init flag
            apply = False

            # first runway
            rw = 0

            # scan all runway's
            while self._airspace.arrivalRunway(rw):
                # arrival belongs to runway ?
                if srt.belongsToRunway(self._airspace.arrivalRunway(rw)):
                    # ok, found
                    apply = True

                # next runway
                rw += 1

            # no found any runway ?
            if not apply:
                # next arrival
                i += 1
                srt = self._airspace.arrival(i)

                # next loop
                continue

            n = 0
            while srt.item(n) is not None:
                pos1 = self._airspace.getPosition(srt.item(n)._sName)
                r = tMath.distLL(pos, pos1)

                if srt.item(n + 1):
                    pos2 = self._airspace.getPosition(srt.item(n + 1)._sName)
                    rttrk = tMath.track(pos1, pos2)
                    rtdist = tMath.distLL(pos1, pos2)
                    mstrk = tMath.track(pos1, pos)
                    tdelta = tMath.trackDelta(rttrk, mstrk)
                    prog = tMath.distLL(pos, pos1) * tMath.dcos(tdelta)

                    if ((prog > 0) and (prog < rtdist)):
                        r = tMath.distLL(pos, pos1) * tMath.dsin(abs(tdelta))

                # distância menor que a anterior ?
                if r < l_fClosest_r:
                    # this is the new closest element
                    l_sClosest = srt.getName()
                    l_fClosest_r = r

                n += 1

            # next arrival
            i += 1
            srt = self._airspace.arrival(i)

        # first transition
        i = 0
        srt = self._airspace.transition(0)

        # scan all transitions
        while srt is not None:
            # init flag
            apply = False

            # first runway
            rw = 0

            # scan all runway's
            while self._airspace.arrivalRunway(rw):
                # transition belongs to runway ?
                if srt.belongsToRunway(self._airspace.arrivalRunway(rw)):
                    # ok, found
                    apply = True

                # next runway
                rw += 1

            # no found any transition ?
            if not apply:
                # next transition
                i += 1
                srt = self._airspace.transition(i)

                # next loop
                continue

            n = 0
            while srt.item(n):
                pos1 = self._airspace.getPosition(srt.item(n)._sName)
                r = tMath.distLL(pos, pos1)

                if srt.item(n + 1):
                    pos2 = self._airspace.getPosition(srt.item(n + 1)._sName)
                    rttrk = tMath.track(pos1, pos2)
                    rtdist = tMath.distLL(pos1, pos2)
                    mstrk = tMath.track(pos1, pos)
                    tdelta = tMath.trackDelta(rttrk, mstrk)
                    prog = tMath.distLL(pos, pos1) * tMath.dcos(tdelta)

                    if ((prog > 0) and (prog < rtdist)):
                        r = tMath.distLL(pos, pos1) * tMath.dsin(abs(tdelta))

                if r < l_fClosest_r:
                    l_sClosest = srt._sName()
                    l_fClosest_r = r

                n += 1

            # next transition
            i += 1
            srt = self._airspace.transition(i)

        self._s_route = l_sClosest
        self._i_lateral_mode = self.C_LMODE_RTE

    # ---------------------------------------------------------------------------------------------
    def makeVector(self, f_iVal):
        """
        DOCUMENT ME!
        """
        # check input
        # assert f_control

        # M_LOG.debug("f_iVal....: " + str(f_iVal))
        # M_LOG.debug("aoAircraft: " + str(len(self._dct_flight)))

        # verifica se o índice é válido
        if (f_iVal < 0) or (f_iVal >= len(self._dct_flight)):
            # cai fora...
            return

        # get mouse position
        l_XY = pxy.CPosXY(self._iMouseX, self._iMouseY)
        assert l_XY is not None

        # converte as coordenadas de tela para mapa
        l_pos = self._viewport.translate_xy(l_XY)

        self._f_radar_vector = tMath.track(self._dct_flight[f_iVal].radarPosition(), l_pos) + self._airspace.variation()

        l_iRem = int(self._f_radar_vector * 10.) % 50

        self._f_radar_vector = int(self._f_radar_vector) - (int(self._f_radar_vector) % 5)

        if l_iRem >= 25:
            self._f_radar_vector += 5.

        if self._f_radar_vector > 360.:
            self._f_radar_vector -= 360.

        if 0. == self._f_radar_vector:
            self._f_radar_vector = 360.

        self._i_lateral_mode = self.C_LMODE_HDG

    # ---------------------------------------------------------------------------------------------
    def notify(self, f_evt):
        """
        DOCUMENT ME!
        """
        # return
        return

    # ---------------------------------------------------------------------------------------------
    def _on_draw(self, fo_painter):
        """
        called to draw the radar window content. calls the _on_draw function for every graphical
        element to be displayed in the view. Those elements are listed in the _lstDisplayElement
        table. The elements are displayed from the lower layer to the upper and within a layer
        from the lowest priority order to the upper, so that elements with the highest priority
        are displayed over any other graphical elements

        @param fo_painter: painting device
        """
        # check input
        assert fo_painter

        # pTrkMngr = CSlateRadar.cls_app.GetTrackMngr ()

        # set background mode
        # fo_painter.setBackgroundMode(QtCore.Qt.TransparentMode)

        # draw background
        self._paint_engine.draw_background(self, fo_painter)

        # for all priorities...
        #for l_iPrio in xrange(displayElement.PRIO_MAP_MAX, -1, -1):
            # M_LOG.debug("l_iPrio: " + str(l_iPrio))

            # for all mapas da lista...
            #for l_oVMap in self._lst_view_maps:
                # desenha o elemento
                #l_oVMap._on_draw(self, fo_painter, l_iPrio)

        # desenha o ARP
        self._paint_engine.draw_arp(self)

        # for all aerodromes...
        for l_aer in list(self._airspace.dct_aer.values()):
            # desenha o aeródromo
            self._paint_engine.draw_aerodromo(self, l_aer)
        '''
        # init index
        l_iI = 0
        l_iJ = 0

        # draw standard routes
        while self._airspace.arrivalRunway(l_iI):
            while self._airspace.arrival(l_iJ):
                if self._airspace.arrival(l_iJ).belongsToRunway(self._airspace.arrivalRunway(l_iI)):
                    self._paint_engine.drawArrival(self, self._airspace.arrival(l_iJ))

                l_iJ += 1
            l_iJ = 0

            while self._airspace.transition(l_iJ):
                if self._airspace.transition(l_iJ).belongsToRunway(self._airspace.arrivalRunway(l_iI)):
                    self._paint_engine.drawTransition(self, self._airspace.transition(l_iJ))

                l_iJ += 1
            l_iI += 1
        l_iI = 0

        # draw standard routes
        while self._airspace.departureRunway(l_iI):

            l_iJ = 0

            while self._airspace.departure(l_iJ):
                if self._airspace.departure(l_iJ).belongsToRunway(self._airspace.departureRunway(l_iI)):
                    self._paint_engine.drawDeparture(self, self._airspace.departure(l_iJ))

                l_iJ += 1
            l_iI += 1
        '''
        # draw DMEs navaids
        for l_dme in [fix for fix in list(self._airspace.dct_fix.values()) if ldefs.E_DME == fix.en_fix_tipo]:
            # show DME ?
            if self._parent.dct_visual.get(ldefs.D_FMT_FIX.format(l_dme.s_fix_indc), False):
                # draw DME
                self._paint_engine.draw_navaid(self, l_dme)

        # draw NDBs navaids
        for l_ndb in [fix for fix in list(self._airspace.dct_fix.values()) if ldefs.E_NDB == fix.en_fix_tipo]:
            # show NDB ?
            if self._parent.dct_visual.get(ldefs.D_FMT_FIX.format(l_ndb.s_fix_indc), False):
                # desenha o NDB
                self._paint_engine.draw_navaid(self, l_ndb)

        # draw VORs navaids
        for l_vor in [fix for fix in list(self._airspace.dct_fix.values()) if ldefs.E_VOR == fix.en_fix_tipo]:
            # show VOR ?
            if self._parent.dct_visual.get(ldefs.D_FMT_FIX.format(l_vor.s_fix_indc), False):
                # desenha o VOR
                self._paint_engine.draw_navaid(self, l_vor)

        # draw waypoints
        for l_wpt in [fix for (key, fix) in list(self._airspace.dct_fix.items()) if ldefs.E_BRANCO == fix.en_fix_tipo]:
            # show waypoint ?
            if self._parent.dct_visual.get(ldefs.D_FMT_FIX.format(l_wpt.s_fix_indc), False):
                # draw waypoint
                self._paint_engine.draw_navaid(self, l_wpt)

        # draw runways
        # for l_oRWY in self._airspace.aoRWY:
            # self._paint_engine.drawRunway(self, l_oRWY)

        # for all aproximações...
        for l_apx in list(self._airspace.dct_apx.values()):
            # show approach ?
            if self._parent.dct_visual.get(ldefs.D_FMT_APX.format(l_apx.i_prc_id), False):
                # draw aproximação
                self._paint_engine.draw_aproximacao(self, l_apx)

        # for all subidas...
        for l_sub in list(self._airspace.dct_sub.values()):
            # show climb ?
            if self._parent.dct_visual.get(ldefs.D_FMT_SUB.format(l_sub.i_prc_id), False):
                # draw subida
                self._paint_engine.draw_subida(self, l_sub)

        # for all trajectories...
        for l_trj in list(self._airspace.dct_trj.values()):
            # show trajectory ?
            if self._parent.dct_visual.get(ldefs.D_FMT_TRJ.format(l_trj.i_prc_id), False):
                # draw trajectory
                self._paint_engine.draw_trajetoria(self, l_trj)

        # draw aircraft targets
        for l_anv in list(self._dct_flight.values()):
            # desenha a aeronave
            self._paint_engine.draw_blip(self, l_anv)
        '''
        if self._i_active_ac >= 0:
            if self.C_LMODE_HDG == self._i_lateral_mode:
                self._paint_engine.drawVector(self, self._dct_flight[self._i_active_ac], self._f_radar_vector)

            elif self.C_LMODE_DCT == self._i_lateral_mode:
                if self._s_direct != "":
                    self._paint_engine.drawDirect(self, self._dct_flight[self._i_active_ac], self._s_direct)

            elif self.C_LMODE_RTE == self._i_lateral_mode:
                if self._s_route != "":
                    self._paint_engine.drawRoute(self, self._dct_flight[self._i_active_ac], self._s_route)

            elif self.C_LMODE_APP == self._i_lateral_mode:
                if self._s_approach != "":
                    self._paint_engine.drawApproach(self, self._dct_flight[self._i_active_ac], self._s_approach)
        '''
        '''
        # if the currently selected radar service is not available the message
        # "display frozen" is displayed in the top of the underlay layer
        if True: #not pTrkMngr.m_pTrkSrc:

            FrozenTime = QtCore.QTime ().currentTime () # pTrkMngr.GetFrozenTime ()
            rect = self.rect ()

            fo_painter.setFont(FontMngr.GetFontByName("FROZEN"))
            fo_painter.setPen(ColorMngr.GetColor(ColorMngr.GetColorNb("FROZEN_MSG")))

            txt = "FROZEN AT " + FrozenTime.toString("hh:mm:ss")
            size = fo_painter.boundingRect(0, 0, 0, 0, QtCore.Qt.AlignLeft, txt).size ()

            fo_painter.drawText(rect.center ().x () - size.width () / 2, rect.center ().y (), txt)
        '''
        '''
        # and with a higher priority the element with implicit focus
        if self.m_pCurElem is not None:
            # M_LOG.debug("self.m_pCurElem: ", + str(self.m_pCurElem))
            self.m_pCurElem._on_draw(fo_painter, 1)

        if self.m_pModifElem is not None:
            # M_LOG.debug("self.m_pModifElem: ", + str(self.m_pModifElem))
            self.m_pModifElem._on_draw(fo_painter, 0)
        '''
    # ---------------------------------------------------------------------------------------------
    def showLateral(self, f_iVal):
        """
        DOCUMENT ME!
        """
        self._i_active_ac = f_iVal

        self.setMouseTracking(True)

    # =============================================================================================
    # Qt Slots
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def invert(self, f_vInverted):
        """
        DOCUMENT ME!
        """
        # inverte as cores dos elementos
        self._paint_engine.setColors(f_vInverted)

        # redraw everything
        self.repaint()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot(bool)
    def pause(self, f_vVal):
        """
        DOCUMENT ME!
        """
        self._v_paused = f_vVal

        if self._v_paused:
            self.killTimer(self._i_radar_timer)
            self.killTimer(self._i_aircraft_timer)

        else:
            self._i_radar_timer = self.startTimer(tMath.round(self._f_radar_interval, 0))
            self._i_aircraft_timer = self.startTimer(tMath.round(self._f_update_interval, 0))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def showRange(self):
        """
        DOCUMENT ME!
        """
        self._parent.status_bar.lbl_range.setText("R%d" % int(self._viewport.f_zoom))

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def zoom_in(self):
        """
        DOCUMENT ME!
        """
        # change zoom  
        self._viewport.f_zoom = round(self._viewport.f_zoom / math.sqrt(2.), 0)
                
        # update scope
        self.repaint()

    # ---------------------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def zoom_out(self):
        """
        DOCUMENT ME!
        """
        # change zoom
        self._viewport.f_zoom = round(self._viewport.f_zoom * math.sqrt(2.), 0)
                
        # update scope
        self.repaint()

    # =============================================================================================
    # Qt Events
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    # void (QKeyReleaseEvent)
    def keyReleaseEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # check input
        assert f_evt
        
        if self._i_active_ac < 0:
            # return
            return

        if QtCore.Qt.Key_D == f_evt.key():
            self.makeDirect()
            self.repaint()

        elif QtCore.Qt.Key_R == f_evt.key():
            self.makeRoute()
            self.repaint()

        elif QtCore.Qt.Key_H == f_evt.key():
            self.makeVector(self._i_active_ac)
            self.repaint()

        elif QtCore.Qt.Key_A == f_evt.key():
            self.makeApproach()
            self.repaint()

        elif QtCore.Qt.Key_Escape == f_evt.key():
            if self._i_active_ac >= 0:
                self.hideLateral()
                self.repaint()

        else:
            f_evt.ignore()

    # ---------------------------------------------------------------------------------------------
    # void (QMouseMoveEvent)
    def mouseMoveEvent(self, f_evt):
        """
        called when the mouse pointer is moved over the radar window

        @param  f_evt: QMouseEvent*, not used in this function
        """
        # check input
        assert f_evt
        
        # checks
        Normal = 0
        Panning = 1
        Zoom = 2

        m_Mode = 0
        '''
        QRect radarwndrect ;
        QPoint globalpnt ;
        QRect statusbarrect ;
        '''
        # M_LOG.debug("_iActiveAC...: " + str(self._i_active_ac))
        # M_LOG.debug("_iLateralMode: " + str(self._i_lateral_mode))

        self._iMouseX = f_evt.x()
        self._iMouseY = f_evt.y()

        if self._i_active_ac >= 0:
            if self.C_LMODE_HDG == self._i_lateral_mode:
                self.makeVector(self._i_active_ac)

            elif self.C_LMODE_DCT == self._i_lateral_mode:
                self.makeDirect()

            elif self.C_LMODE_RTE == self._i_lateral_mode:
                self.makeRoute()

            elif self.C_LMODE_APP == self._i_lateral_mode:
                self.makeApproach()

            self.repaint()

        else:
            # pnt = QtGui.QCursor.pos () ;
            # point = mapFromGlobal(pnt) ;

            # CheckFocus () ;

            # check the radar window mode
            if Normal == m_Mode:
                '''
                # No mode is activated for the radar window having the focus
                # No process is to be performed if the radar window is over
                # another radar window for which the panning mode is activated
                if m_psMainWnd
                    if(m_psMainWnd->m_Mode == Panning)
                        break ;

                if m_psSecWnd1
                    if(m_psSecWnd1->m_Mode == Panning)
                        break ;

                if m_psSecWnd2
                    if(m_psSecWnd2->m_Mode == Panning)
                        break ;
                '''
                # the status bar must show the current lat long of the mouse pointer
                # if it presents the focus and the mouse pointer is over the view
                # QPoint pnt ;

                if (1):  # m_bsForcedMove or (( point != m_LastCursorPos) and(hasMouse ()))):
                    '''
                    killTimer(m_TimerId) ;
                    m_TimerId = startTimer(100) ;

                    pnt = point ;
                    DPtoLP(&pnt) ;

                    radarwndrect = this->geometry () ;
                    statusbarrect = GetStatusBar ()->rect () ;
                    '''
                    # the mouse pointer must not be over the status bar
                    if (1):  # globalpnt.y () <= radarwndrect.y () + radarwndrect.height () - statusbarrect.height ()):

                        # converte a posição do mouse para coordenadas XY
                        l_oXY = pxy.CPosXY(f_evt.x(), f_evt.y())
                        assert l_oXY

                        # converte coordenadas XY para geográfica
                        l_oGeo = self._viewport.translate_xy(l_oXY)
                        assert l_oGeo

                        # atualiza a statusBar
                        self._parent.status_bar.update_coordinates(str(l_oGeo) + " (%d, %d)" % (f_evt.x(), f_evt.y()))

                        # libera a área alocada
                        del l_oGeo

                pass
                '''
                m_LastCursorPos = point ;

                # the event is then transmitted to the graphical element that are
                # under modification or that has the implicit focus
                if(hasMouse ())

                    if(m_pModifElem)
                        m_pModifElem->onMouseMove(0, point) ;

                    if(m_pCurElem)

                        curprio = m_pCurElem->GetPriority(point, true) ;

                        if(curprio == 0)

                            m_pCurElem->SelectElement(false) ;
                            m_pCurElem = NULL ;
                else:
                    # if the element being modified is not within the view the event is transmitted
                    # anyway in order to cancel the tool creation mode
                    if(m_pModifElem)
                        m_pModifElem->onMouseMove(0, point) ;
                '''
                pass

            elif (Panning == m_Mode):
                '''
                # panning mode
                if(m_ReducePanning >= 10)
                {
                    m_ReducePanning = 0 ;
                    QRect rect = QWidget::rect () ;
                    QSize size ;
                    QPoint pnt ;
                    size = QSize(rect.center ().x () - point.x (), rect.center ().y () - point.y ()) ;
                    DPtoLP(&size) ;
                    size.setHeight(-size.height ()) ;

                    # Because of the range limitation, the center must remains within predefined limits
                    # if (( size.width ()) ||(size.height ()))
                    {
                        # Following the first move of the mouse pointer this check is not performed and over all the presentation of the view is not updated as the first move is the positionning of the mouse pointer at the center of the view
                        if(!m_FirstPanningMove)
                        {
                            pnt = GetCentre () ;
                            pnt = QPoint(pnt.x () + size.width (), pnt.y () + size.height ()) ;

                            /*if(pnt.x () >5000)
                                pnt.setX(5000) ;

                            if(pnt.x () <-5000)
                                pnt.setX(-5000) ;

                            if(pnt.y () >5000)
                                pnt.setY(5000) ;

                            if(pnt.y () <-5000)
                                pnt.setY(-5000) ;*/

                            SetCentre(pnt) ;
                            onUpdate(NULL, 0, NULL) ;

                        } # end if

                        m_FirstPanningMove = false ;
                        rect = geometry () ;
                        QCursor::setPos(rect.center () .x (), rect.center () .y ()) ;
                        CTOORArrow::UpdateFromView(this) ;

                    } # end if
                }
                else
                    m_ReducePanning ++ ;
                '''
                pass

            elif Zoom == m_Mode:
                '''
                # zoom mode
                radarwndrect = this->geometry () ;
                globalpnt = QCursor::pos () ;
                statusbarrect = GetStatusBar ()->rect () ;

                # the mouse pointer must be over the radar window to perform the change
                if (( globalpnt.x () >= radarwndrect.x () + radarwndrect.width ()) ||
                   (globalpnt.x () <= radarwndrect.x ()) ||
                   (globalpnt.y () <= radarwndrect.y ()) ||
                   (globalpnt.y () >= radarwndrect.y () + radarwndrect.height () - statusbarrect.height ()))
                {
                    m_Mode = Normal ;
                    setCursor(*CAsdApp::GetApp ()->GetCursor(MPNormalSelect)) ;

                } # end if
                '''
                pass

    # ---------------------------------------------------------------------------------------------
    # void (QMouseReleaseEvent)
    def mouseReleaseEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # check input
        assert f_evt

        if f_evt.button() & QtCore.Qt.LeftButton:
            # none aircraft active ?
            if self._i_active_ac < 0:
                # update mouse
                self._iMouseX = f_evt.x()
                self._iMouseY = f_evt.y()

                # find closest aircraft
                l_XY = pxy.CPosXY(self._iMouseX, self._iMouseY)
                assert l_XY is not None

                l_pos = self._viewport.translate_xy(l_XY)

                l_fClosest_r = 1000000
                # l_iClosest = -1

                # for key in xrange(len(self._dct_flight)):
                    # r = tMath.distLL(l_pos, self._dct_flight[key].radarPosition())

                    # if r < l_fClosest_r:
                        # l_iClosest = key
                        # l_fClosest_r = r

                # activate Vector
                # self.showLateral(l_iClosest)
                self.makeVector(self._i_active_ac)
                self.repaint()

            else:  # Yes, order HDG
                if self.C_LMODE_HDG == self._i_lateral_mode:
                    self._dct_flight[self._i_active_ac].instructHeading(int(self._f_radar_vector))

                elif self.C_LMODE_DCT == self._i_lateral_mode:
                    self._dct_flight[self._i_active_ac].instructDirect(self._s_direct)

                elif self.C_LMODE_RTE == self._i_lateral_mode:
                    self._dct_flight[self._i_active_ac].instructRoute(self._s_route)

                elif self.C_LMODE_APP == self._i_lateral_mode:
                    self._dct_flight[self._i_active_ac].instructApproach(self._s_approach)

                self.hideLateral()
                self.repaint()

        elif f_evt.button() & QtCore.Qt.MidButton:
            l_XY = pxy.CPosXY(f_evt.x(), f_evt.y())
            assert l_XY is not None

            l_pos = self._viewport.translate_xy(l_XY)
            self._viewport.center = l_pos

            self.repaint()

        elif f_evt.button() & QtCore.Qt.RightButton:
            # cancel vectoring
            if self._i_active_ac >= 0:
                self.hideLateral()
                self.repaint()

    # ---------------------------------------------------------------------------------------------
    # void (QPaintEvent)
    def paintEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # check input
        assert f_evt
        
        # checks
        assert self._pen
        assert self._brush
        assert self._rect_invalid is not None

        # cria um painter para o pixmap
        lo_painter = QtGui.QPainter(self)
        assert lo_painter

        # set pen
        lo_painter.setPen(self._pen)

        # set brush
        lo_painter.setBrush(self._brush)

        if 1:  # not self._rect_invalid.isEmpty():
            # save painter
            lo_painter.save()

            # fill background
            lo_painter.fillRect(self._rect_invalid, self._brush)

            # draw graphics elements
            self._on_draw(lo_painter)

            # invalidate rect
            self._rect_invalid.setRect(0, 0, -1, -1)

            # restore painter
            lo_painter.restore()

    # ---------------------------------------------------------------------------------------------
    # void (QResizeEvent)
    def resizeEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # check input
        assert f_evt
        
        # update size
        self._viewport.update_size(self.width() - 1, self.height() - 1)

    # ---------------------------------------------------------------------------------------------
    # void (QTimerEvent)
    def timerEvent(self, f_evt):
        """
        DOCUMENT ME!
        """
        # check input
        assert f_evt
        
        # radar timer ?
        if f_evt.timerId() == self._i_radar_timer:
            # M_LOG.debug("RadarTimer...")

            # reconstroi a lista de vôos ativos
            # self._build_aircraft_list()

            # for all aeronaves na lista...
            for l_atv in list(self._dct_flight.values()):
                # faz a atualização da posição das aeronaves
                l_atv.update_radar_position(self._f_simulation_speed * self._f_radar_interval)

                # atualiza a posição da aeronave
                # self.updateAnv(l_atv, l_iI)

            # atualiza a tela
            self.repaint()

        # flight timer ?
        elif f_evt.timerId() == self._i_aircraft_timer:
            # for all flights in list...
            for l_atv in list(self._dct_flight.values()):
                # faz a cinemática da aeronave
                l_atv.fly(self._f_simulation_speed * self._f_update_interval)

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def fRadarInterval(self):
        return self._f_radar_interval

    @fRadarInterval.setter
    def fRadarInterval(self, f_val):
        self._f_radar_interval = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def fUpdateInterval(self):
        return self._f_update_interval

    @fUpdateInterval.setter
    def fUpdateInterval(self, f_val):
        self._f_update_interval = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, f_val):
        self._viewport = f_val

# < the end >--------------------------------------------------------------------------------------
