# -*- coding: utf-8 -*-
"""
flight_plan_item

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < class CFlightPlanItem >------------------------------------------------------------------------

class CFlightPlanItem(object):

    # ---------------------------------------------------------------------------------------------
    _EXACTLY = 0
    _OR_BELOW = 1
    _OR_ABOVE = 2

    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        self._s_name = None

        self._fInbound = -1.

        self._iAltConstraint = 0
        self._iAltConstraintType = 0
        self._iSpeedConstraint = 0

        self._vFlyOver = False
        self._vApproach = False

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_name(self):
        """
        get latitude
        """
        return self._s_name
                                            
    @s_name.setter
    def s_name(self, f_val):
        """
        set latitude
        """
        self._s_name = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_lng(self):
        """
        get longitude
        """
        return self._f_lng
                                            
    @f_lng.setter
    def f_lng(self, f_val):
        """
        set longitude
        """
        self._f_lng = f_val

# < the end >--------------------------------------------------------------------------------------
