# -*- coding: utf-8 -*-
"""
statusbar_visil

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# view
import view.common.statusbar_basic as sbb

# < class CStatusBarVisil >------------------------------------------------------------------------

class CStatusBarVisil(sbb.CStatusBarBasic):
    """
    used to display the Current Working Position, the Independant/Dependant mode, radar and weather
    services used, filters and coordinates of the mouse pointer on the status bar of a radar window
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_parent=None):
        """
        constructor
        """
        # check input
        assert f_parent

        # init super class
        super(CStatusBarVisil, self).__init__(f_parent)

    # =============================================================================================
    # dados
    # =============================================================================================

# < the end >--------------------------------------------------------------------------------------
