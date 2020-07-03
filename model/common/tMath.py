# -*- coding: utf-8 -*-
"""
tMath

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# Python library
import logging
import math
import sys

# -------------------------------------------------------------------------------------------------
def dasin(f_sin):
    """
    DOCUMENT ME!
    """
    # return
    return math.degrees(math.asin(f_sin))

# -------------------------------------------------------------------------------------------------
def datan(f_tan):
    """
    DOCUMENT ME!
    """
    # return
    return math.degrees(math.atan(f_tan))

# -------------------------------------------------------------------------------------------------
def dcos(f_degrees):
    """
    DOCUMENT ME!
    """
    # return
    return math.cos(math.radians(f_degrees))

# -------------------------------------------------------------------------------------------------
def dsin(f_degrees):
    """
    DOCUMENT ME!
    """
    # return
    return math.sin(math.radians(f_degrees))

# -------------------------------------------------------------------------------------------------
def dtan(f_degrees):
    """
    DOCUMENT ME!
    """
    # return
    return math.tan(math.radians(f_degrees))

# -------------------------------------------------------------------------------------------------
def dist(f_val1, f_val2):
    """
    DOCUMENT ME!
    """
    if isinstance(f_val1, float) and isinstance(f_val2, float):
        return distXY(f_val1, f_val2)

    elif isinstance(f_val1, posLatLng) and isinstance(f_val2, posLatLng):
        return distLL(f_val1, f_val2)

    else:
        # logger
        l_log = logging.getLogger("tMath::dist")
        l_log.setLevel(logging.CRITICAL)
        l_log.critical("E01: tipo inválido.")

    # quit app
    sys.exit(-1)

# -------------------------------------------------------------------------------------------------
def distLL(f_pos1, f_pos2):
    """
    DOCUMENT ME!
    """
    # calc lat dist
    lf_lat = (f_pos2.f_lat - f_pos1.f_lat) * 60.

    # calc lng dist
    lf_lng = (f_pos2.f_lng - f_pos1.f_lng) * dcos(f_pos1.f_lat) * 60.

    # return
    return distXY(lf_lat, lf_lng)

# -------------------------------------------------------------------------------------------------
def distXY(f_dx, f_dy):
    """
    DOCUMENT ME!
    """
    # return
    return math.sqrt(pow(f_dx, 2) + pow(f_dy, 2))

# -------------------------------------------------------------------------------------------------
def round(f_d, f_n):
    """
    DOCUMENT ME!
    """
    f_d *= pow(10, f_n)
    f_d += .5
    f_d = int(f_d)
    f_d /= pow(10, f_n)

    # return
    return f_d

# -------------------------------------------------------------------------------------------------
def sign(l_a):
    """
    DOCUMENT ME!
    """
    # return
    return 1 if l_a > 0 else -1

# -------------------------------------------------------------------------------------------------
def track(f_pos1, f_pos2):
    """
    DOCUMENT ME!
    """
    lf_lat = f_pos2.f_lat - f_pos1.f_lat
    lf_lng = (f_pos2.f_lng - f_pos1.f_lng) * dcos(f_pos1.f_lat)

    if lf_lng != 0.:
        l_tr = 90. + datan(-lf_lat / lf_lng)

    else:
        l_tr = 90. + datan(-lf_lat)

    if lf_lng < 0.:
        l_tr += 180.

    while l_tr > 360.:
        l_tr -= 360.

    # return
    return l_tr

# -------------------------------------------------------------------------------------------------
def trackDelta(f_from, f_to):
    """
    DOCUMENT ME!
    """
    l_d = f_to - f_from

    while l_d <= -180.:
        l_d += 360.

    while l_d > 180.:
        l_d -= 360.

    # return
    return l_d

# -------------------------------------------------------------------------------------------------
def trackLeftAbeam(f_tr):
    """
    DOCUMENT ME!
    """
    l_d = f_tr - 90.

    while l_d < 0.:
        l_d += 360.

    # return
    return l_d

# -------------------------------------------------------------------------------------------------
def trackOpposite(f_tr):
    """
    DOCUMENT ME!
    """
    l_d = f_tr + 180.

    while l_d >= 360.:
        l_d -= 360.

    # return
    return l_d

# -------------------------------------------------------------------------------------------------
def trackRightAbeam(f_tr):
    """
    DOCUMENT ME!
    """
    l_d = f_tr + 90.

    while l_d >= 360.:
        l_d -= 360.

    # return
    return l_d

# < the end >--------------------------------------------------------------------------------------
