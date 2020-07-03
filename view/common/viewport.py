# -*- coding: utf-8 -*-
"""
viewport

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import math

# model
import libs.coords.coord_defs as cdefs
import libs.coords.pos_lat_lng as pll
import libs.coords.pos_xy as pxy

# < class CViewport >------------------------------------------------------------------------------

class CViewport(object):
    """
    viewport
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, fi_w, fi_h):
        """
        constructor
        """
        # inicia a super classe
        super(CViewport, self).__init__()

        # largura e altura da viewport
        self._f_width = float(fi_w)
        self._f_height = float(fi_h)

        # coordenada do centro da viewport
        self._center = pll.CPosLatLng()
        assert self._center is not None

        self._f_blip_size = fi_w / 220.
        self._f_zoom = 160.

    # ---------------------------------------------------------------------------------------------
    def translate_pos(self, f_pos):
        """
        translate pos
        """
        # check input
        assert f_pos

        # create answer
        l_xy = pxy.CPosXY()
        assert l_xy is not None

        # lat/lng
        lf_delta_lat = (f_pos.f_lat - self._center.f_lat) * cdefs.D_CNV_GR2NM
        lf_delta_lng = (f_pos.f_lng - self._center.f_lng) * cdefs.D_CNV_GR2NM

        # escala
        lf_esc = self._f_width / self._f_zoom

        # convert to x/y
        l_xy.f_y = self._f_height / 2. - lf_delta_lat * lf_esc
        l_xy.f_x = self._f_width / 2. + lf_delta_lng * math.cos(math.radians(self._center.f_lat)) * lf_esc

        # return
        return l_xy

    # ---------------------------------------------------------------------------------------------
    def translate_xy(self, f_xy):
        """
        translate xy
        """
        # check input
        assert f_xy

        # create answer
        l_pos = pll.CPosLatLng()
        assert l_pos is not None

        # get x/y
        lf_delta_x = (f_xy.f_x - self._f_width / 2.) / cdefs.D_CNV_GR2NM
        lf_delta_y = (f_xy.f_y - self._f_height / 2.) / cdefs.D_CNV_GR2NM

        # escala
        lf_esc = float(self._f_zoom / self._f_width)

        # calculate lat/lng
        l_pos.f_lat = self._center.f_lat - lf_delta_y * lf_esc
        l_pos.f_lng = self._center.f_lng + lf_delta_x / math.cos(math.radians(self._center.f_lat)) * lf_esc

        # return
        return l_pos

    # ---------------------------------------------------------------------------------------------
    def update_size(self, fi_w, fi_h):
        """
        update size
        """
        # set size
        self._f_width = float(fi_w)
        self._f_height = float(fi_h)

        # set blip size
        self._f_blip_size = fi_h / 140.

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_blip_size(self):
        return self._f_blip_size

    @f_blip_size.setter
    def f_blip_size(self, f_val):
        self._f_blip_size = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, f_val):
        self._center = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def ppnm(self):
        return float(self._f_width) / float(self._f_zoom)

    # ---------------------------------------------------------------------------------------------
    @property
    def f_zoom(self):
        return self._f_zoom

    @f_zoom.setter
    def f_zoom(self, f_val):

        # check input
        if f_val < 20:
            f_val = 20

        elif f_val > 420:
            f_val = 420

        self._f_zoom = float(f_val)

# < the end >--------------------------------------------------------------------------------------
