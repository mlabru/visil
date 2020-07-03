# -*- coding: utf-8 -*-
"""
brk_model

mantém os detalhes de um breakpoint

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < class CBrkModel >------------------------------------------------------------------------------

class CBrkModel(object):
    """
    mantém as informações específicas sobre um breakpoint
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):

        # init super class
        super(CBrkModel, self).__init__()

        # flag ok (bool)
        self._v_brk_ok = False

        # identificação do breakpoint
        self._i_brk_id = 0

        # X (m)
        self._f_brk_x = 0.
        # Y (m)
        self._f_brk_y = 0.
        # Z (m)
        self._f_brk_z = 0.

    # ---------------------------------------------------------------------------------------------
    def copy_brk(self, f_brk):
        """
        copy constructor
        cria um novo breakpoint a partir de um outro breakpoint

        @param f_brk: breakpoint a ser copiado
        """
        # check input
        assert f_brk

        # identificação
        self._i_brk_id = f_brk.i_brk_id

        # X
        self._f_brk_x = f_brk.f_brk_x
        # Y
        self._f_brk_y = f_brk.f_brk_y
        # Z
        self._f_brk_z = f_brk.f_brk_z

        # flag ok (bool)
        self._v_brk_ok = f_brk.v_brk_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def v_brk_ok(self):
        return self._v_brk_ok

    @v_brk_ok.setter
    def v_brk_ok(self, f_val):
        self._v_brk_ok = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def i_brk_id(self):
        return self._i_brk_id

    @i_brk_id.setter
    def i_brk_id(self, f_val):
        self._i_brk_id = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_brk_x(self):
        return self._f_brk_x

    @f_brk_x.setter
    def f_brk_x(self, f_val):
        self._f_brk_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_brk_y(self):
        return self._f_brk_y

    @f_brk_y.setter
    def f_brk_y(self, f_val):
        self._f_brk_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_brk_z(self):
        return self._f_brk_z

    @f_brk_z.setter
    def f_brk_z(self, f_val):
        self._f_brk_z = f_val

# < the end >--------------------------------------------------------------------------------------
