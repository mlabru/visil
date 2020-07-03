# -*- coding: utf-8 -*-
"""
aer_model

mantém os detalhes de um aeródromo

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < class CAerModel >------------------------------------------------------------------------------

class CAerModel(object):
    """
    mantém as informações específicas sobre aeródromo
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # flag ok (bool)
        self._v_aer_ok = False

        # identificação do aeródromo (indicativo)
        self._s_aer_indc = ""

        # descrição do aeródromo (nome)
        self._s_aer_desc = ""

        # elevação do aeródromo (m)
        self._f_aer_elev = 0

    # ---------------------------------------------------------------------------------------------
    def copy_aer(self, f_aer):
        """
        copy constructor
        cria um novo aeródromo a partir de um outro aeródromo

        @param f_aer: aeródromo a ser copiado
        """
        # check input
        assert f_aer

        # identificação do aeródromo
        self._s_aer_indc = f_aer.s_aer_indc

        # descrição do aeródromo
        self._s_aer_desc = f_aer.s_aer_desc

        # elevação (m)
        self._f_aer_elev = f_aer.f_aer_elev

        # flag ok (bool)
        self._v_aer_ok = f_aer.v_aer_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_aer_elev(self):
        """
        get elevação
        """
        return self._f_aer_elev

    @f_aer_elev.setter
    def f_aer_elev(self, f_val):
        """
        set elevação
        """
        self._f_aer_elev = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_aer_indc(self):
        """
        get identificação do aeródromo (indicativo)
        """
        return self._s_aer_indc

    @s_aer_indc.setter
    def s_aer_indc(self, f_val):
        """
        set identificação do aeródromo (indicativo)
        """
        self._s_aer_indc = f_val.strip().upper()

    # ---------------------------------------------------------------------------------------------
    @property
    def s_aer_desc(self):
        """
        get descrição
        """
        return self._s_aer_desc

    @s_aer_desc.setter
    def s_aer_desc(self, f_val):
        """
        set descrição
        """
        self._s_aer_desc = f_val.strip()

    # ---------------------------------------------------------------------------------------------
    @property
    def v_aer_ok(self):
        """
        get flag ok
        """
        return self._v_aer_ok

    @v_aer_ok.setter
    def v_aer_ok(self, f_val):
        """
        set flag ok
        """
        self._v_aer_ok = f_val

# < the end >--------------------------------------------------------------------------------------
