# -*- coding: utf-8 -*-
"""
prc_model

mantém os detalhes de um procedimento

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < class CPrcModel >------------------------------------------------------------------------------

class CPrcModel(object):
    """
    mantém as informações específicas sobre procedimento
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # flag ok (bool)
        self._v_prc_ok = False

        # identificação do procedimento
        self._i_prc_id = 0

        # descrição do procedimento
        self._s_prc_desc = ""

    # ---------------------------------------------------------------------------------------------
    def copy_prc(self, f_prc):
        """
        copy constructor
        cria um novo procedimento a partir de outro procedimento

        @param f_prc: procedimento a ser copiado
        """
        # check input
        assert f_prc

        # identificação do procedimento
        self.i_prc_id = f_prc.i_prc_id

        # descrição do procedimento
        self.s_prc_desc = f_prc.s_prc_desc

        # flag ok (bool)
        self.v_prc_ok = f_prc.v_prc_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_prc_desc(self):
        """
        get descrição
        """
        return self._s_prc_desc

    @s_prc_desc.setter
    def s_prc_desc(self, f_val):
        """
        set descrição
        """
        self._s_prc_desc = f_val.strip()

    # ---------------------------------------------------------------------------------------------
    @property
    def i_prc_id(self):
        """
        get identificação do procedimento (indicativo)
        """
        return self._i_prc_id

    @i_prc_id.setter
    def i_prc_id(self, f_val):
        """
        set identificação do procedimento (indicativo)
        """
        self._i_prc_id = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_prc_ok(self):
        """
        get flag ok
        """
        return self._v_prc_ok

    @v_prc_ok.setter
    def v_prc_ok(self, f_val):
        """
        set flag ok
        """
        self._v_prc_ok = f_val

# < the end >--------------------------------------------------------------------------------------
