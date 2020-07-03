# -*- coding: utf-8 -*-
"""
adiru

revision 0.2  2015/dez  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import copy

# < class CADIRU >---------------------------------------------------------------------------------

class CADIRU(object):
    """
    represents air data inertial reference unit
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # inicia a super classe
        super(CADIRU, self).__init__()

        # altitude
        self._f_alt = 0.

        # instrument air speed
        self._f_ias = 0.

        # proa em relação ao norte verdadeiro
        self._f_true_heading = 0.

        # velocidade
        self._f_vel = 0.

    # ---------------------------------------------------------------------------------------------
    def copy(self):
        """
        copy constructor
        """
        # return a copy
        return copy.deepcopy(self)

    # =============================================================================================
    # dados
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_alt(self):
        """
        get altitude
        """
        return self._f_alt

    @f_alt.setter
    def f_alt(self, f_val):
        """
        set altitude
        """
        self._f_alt = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_ias(self):
        """
        get ias (instrument air speed)
        """
        return self._f_ias

    @f_ias.setter
    def f_ias(self, f_val):
        """
        set ias (instrument air speed)
        """
        self._f_ias = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_true_heading(self):
        """
        get true heading
        """
        return self._f_true_heading

    @f_true_heading.setter
    def f_true_heading(self, f_val):
        """
        set true heading
        """
        # check input
        assert 0. <= f_val <= 360.

        # true heading
        self._f_true_heading = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_vel(self):
        """
        get velocidade
        """
        return self._f_vel

    @f_vel.setter
    def f_vel(self, f_val):
        """
        set velocidade
        """
        self._f_vel = f_val

# < the end >--------------------------------------------------------------------------------------
