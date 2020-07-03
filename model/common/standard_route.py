# -*- coding: utf-8 -*-
"""
standard_route

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < class CStandardRoute >-------------------------------------------------------------------------

class CStandardRoute(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        DOCUMENT ME!
        """
        # inicia a super classe
        super(CStandardRoute, self).__init__()

        # route name
        self._s_name = None

        self._lst_items = []
        self._lst_runways = []

    # ---------------------------------------------------------------------------------------------
    def addItem(self, f_item):
        """
        DOCUMENT ME!
        """
        self._lst_items.append(f_item)

    # ---------------------------------------------------------------------------------------------
    def addRunway(self, fs_rwy):
        """
        DOCUMENT ME!
        """
        self._lst_runways.append(fs_rwy)

    # ---------------------------------------------------------------------------------------------
    def belongsToRunway(self, fs_rwy):
        """
        DOCUMENT ME!
        """
        # return
        return fs_rwy in self._lst_runways

    # ---------------------------------------------------------------------------------------------
    def getItem(self, fi_ndx):
        """
        DOCUMENT ME!
        """
        # check input
        if fi_ndx >= len(self._lst_items):
            return None

        # verifica condições de execuçao
        if not self._lst_items:
            return None

        # return
        return self._lst_items[fi_ndx]

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def lst_items(self):
        """
        get list items
        """
        return self._lst_items
                                            
    @lst_items.setter
    def lst_items(self, f_val):
        """
        set list items
        """
        self._lst_items = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_name(self):
        """
        get name
        """
        return self._s_name
                                            
    @s_name.setter
    def s_name(self, f_val):
        """
        set name
        """
        self._s_name = f_val

# < the end >--------------------------------------------------------------------------------------
