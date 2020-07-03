# -*- coding: utf-8 -*-
"""
pst_model

mantém os detalhes de um pista

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < class CPstModel >------------------------------------------------------------------------------

class CPstModel(object):
    """
    mantém as informações específicas sobre pista
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # flag ok (bool)
        self._v_pst_ok = False
        # identificação do pista (indicativo)
        self._s_pst_indc = ""

        # proa em relação ao norte magnético
        self._f_pst_rumo = 0.
                
        # proa em relação ao norte verdadeiro
        self._f_pst_true = 0.

        # X (m)
        self._f_pst_x = 0.
        # Y (m)
        self._f_pst_y = 0.
        # Z (m)
        self._f_pst_z = 0.

    # ---------------------------------------------------------------------------------------------
    def copy_pst(self, f_pst):
        """
        copy constructor
        cria uma nova pista a partir de uma outra pista

        @param f_pst: pista a ser copiada
        """
        # check input
        assert f_pst

        # identificação da pista
        self._s_pst_indc = f_pst.s_pst_indc
        # rumo magnético
        self._f_pst_rumo = f_pst.f_pst_rumo
        # rumo verdadeiro
        self._f_pst_true = f_pst.f_pst_true

        # X
        self._f_pst_x = f_pst.f_pst_x
        # Y
        self._f_pst_y = f_pst.f_pst_y
        # Z
        self._f_pst_z = f_pst.f_pst_z

        # flag ok (bool)
        self._v_pst_ok = f_pst.v_pst_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_pst_indc(self):
        """
        get identificação da pista (indicativo)
        """
        return self._s_pst_indc

    @s_pst_indc.setter
    def s_pst_indc(self, f_val):
        """
        set identificação da pista (indicativo)
        """
        self._s_pst_indc = f_val.strip().upper()

    # ---------------------------------------------------------------------------------------------
    @property
    def v_pst_ok(self):
        """
        get flag pista ok
        """
        return self._v_pst_ok

    @v_pst_ok.setter
    def v_pst_ok(self, f_val):
        """
        set flag pista ok
        """
        self._v_pst_ok = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_rumo(self):
        """
        get rumo magnético da pista
        """
        return self._f_pst_rumo

    @f_pst_rumo.setter
    def f_pst_rumo(self, f_val):
        """
        set rumo magnético da pista
        """
        self._f_pst_rumo = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_true(self):
        """
        get rumo verdadeiro da pista
        """
        return self._f_pst_true

    @f_pst_true.setter
    def f_pst_true(self, f_val):
        """
        set rumo verdadeiro da pista
        """
        self._f_pst_true = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_x(self):
        """
        get X
        """
        return self._f_pst_x

    @f_pst_x.setter
    def f_pst_x(self, f_val):
        """
        set X
        """
        self._f_pst_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_y(self):
        """
        get Y
        """
        return self._f_pst_y

    @f_pst_y.setter
    def f_pst_y(self, f_val):
        """
        set Y
        """
        self._f_pst_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_pst_z(self):
        """
        get Z
        """
        return self._f_pst_z

    @f_pst_z.setter
    def f_pst_z(self, f_val):
        """
        set Z
        """
        self._f_pst_z = f_val

# < the end >--------------------------------------------------------------------------------------
