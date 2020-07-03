# -*- coding: utf-8 -*-
"""
strip_model

used to map attributes of type strip contained in the mds files

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/fev  mlabru
initial release (Linux/Python)
"""
# < class CStripModel >---------------------------------------------------------------------------

class CStripModel(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # init super class
        super(CStripModel, self).__init__()

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_element(self):
        """
        get element
        """
        return "STRIP"

# < the end >--------------------------------------------------------------------------------------
