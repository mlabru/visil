# -*- coding: utf-8 -*-
"""
holding

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < class CHolding >----------------------------------------------------------------------------

class CHolding(object):

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_fixo=None, ff_entrada=None, fc_dir=None):
        """
        constructor
        """
        # check input
        assert fc_dir in ['l', 'r']

        self._sWaypoint = fs_fixo

        self._fInbound = ff_entrada

        # sentido da espera 
        self._cDirection = fc_dir

# < the end >--------------------------------------------------------------------------------------
