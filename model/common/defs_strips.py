# -*- coding: utf-8 -*-
"""
defs_strips
provide all the interface to store the layer

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/abr  mlabru
initial release (Linux/Python)
"""
# < defines >--------------------------------------------------------------------------------------

# strip attributes
D_STP_0, D_STP_ID, D_STP_IND, D_STP_SSR, D_STP_PRF, \
D_STP_LAT, D_STP_LNG, D_STP_ALT, D_STP_PROA, D_STP_IAS, \
D_STP_RAZ, D_STP_HORA, D_STP_STATUS = range(13)

# strips list (piloto)
D_STRIPS = {"0":".", "1":"o", "2":"x", "3":"+", "4":"#", "5":"@", "6":"*", "7":"^", "8":"'", "9":":"}

# reverse strips dictionary
D_STRIPS_VALS = {val: key for key, val in list(D_STRIPS.items())}

# strip default
D_STRIP_DEFAULT = '*'  # u'\u2744'

# < the end >--------------------------------------------------------------------------------------
