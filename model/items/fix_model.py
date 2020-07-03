# -*- coding: utf-8 -*-
"""
fix_model

mantém os detalhes de um fixo

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# model
import model.newton.defs_newton as ldefs

# < class CFixModel >------------------------------------------------------------------------------

class CFixModel(object):
    """
    mantém as informações específicas sobre fixo
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self):
        """
        constructor
        """
        # flag ok (bool)
        self._v_fix_ok = False

        # identificação do fixo
        self._i_fix_id = -1
        # indicativo do fixo
        self._s_fix_indc = ""
        # descriçao do fixo
        self._s_fix_desc = ""

        # tipo do fixo (VOR, NDB, DME ou " ")
        self._en_fix_tipo = ldefs.E_BRANCO

        # X
        self._f_fix_x = 0.
        # Y
        self._f_fix_y = 0.
        # Z
        self._f_fix_z = 0.

    # ---------------------------------------------------------------------------------------------
    def copy_fix(self, f_fix):
        """
        copy constructor. Copia para este fixo os dados de um outro fixo

        @param f_fix: fixo a ser copiado
        """
        # check input
        assert f_fix

        # identificação do fixo
        self._i_fix_id = f_fix.i_fix_id
        # indicativo do fixo
        self._s_fix_indc = f_fix.s_fix_indc
        # descrição do fixo
        self._s_fix_desc = f_fix.s_fix_desc
        # tipo do fixo
        self._en_fix_tipo = f_fix.en_fix_tipo

        # X
        self._f_fix_x = f_fix.f_fix_x
        # Y
        self._f_fix_y = f_fix.f_fix_y
        # Z
        self._f_fix_z = f_fix.f_fix_z

        # flag ok (bool)
        self._v_fix_ok = f_fix.v_fix_ok

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def s_fix_desc(self):
        """
        get descrição
        """
        return self._s_fix_desc

    @s_fix_desc.setter
    def s_fix_desc(self, f_val):
        """
        set descrição
        """
        self._s_fix_desc = f_val.strip()
        
    # ---------------------------------------------------------------------------------------------
    @property
    def v_fix_dme(self):
        """
        get flag DME
        """
        return ldefs.E_DME == self._en_fix_tipo

    # ---------------------------------------------------------------------------------------------
    @property
    def i_fix_id(self):
        """
        get ID
        """
        return self._i_fix_id

    @i_fix_id.setter
    def i_fix_id(self, f_val):
        """
        set ID
        """
        self._i_fix_id = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def s_fix_indc(self):
        """
        get indicativo
        """
        return self._s_fix_indc

    @s_fix_indc.setter
    def s_fix_indc(self, f_val):
        """
        set indicativo
        """
        self._s_fix_indc = f_val.strip()

    # ---------------------------------------------------------------------------------------------
    @property
    def v_fix_ndb(self):
        """
        get flag NDB
        """
        return ldefs.E_NDB == self._en_fix_tipo

    # ---------------------------------------------------------------------------------------------
    @property
    def v_fix_ok(self):
        """
        get flag Ok
        """
        return self._v_fix_ok

    @v_fix_ok.setter
    def v_fix_ok(self, f_val):
        """
        set flag Ok
        """
        self._v_fix_ok = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def en_fix_tipo(self):
        """
        get tipo de fixo
        """
        return self._en_fix_tipo

    @en_fix_tipo.setter
    def en_fix_tipo(self, f_val):
        """
        set tipo de fixo
        """
        # check input
        assert f_val in ldefs.SET_TIPOS_FIXOS

        # salva tipo de fixo
        self._en_fix_tipo = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def v_fix_vor(self):
        """
        get flag VOR
        """
        return ldefs.E_VOR == self._en_fix_tipo

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_x(self):
        """
        get X
        """
        return self._f_fix_x

    @f_fix_x.setter
    def f_fix_x(self, f_val):
        """
        set X
        """
        self._f_fix_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_y(self):
        """
        get Y
        """
        return self._f_fix_y

    @f_fix_y.setter
    def f_fix_y(self, f_val):
        """
        set Y
        """
        self._f_fix_y = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_fix_z(self):
        """
        get Z
        """
        return self._f_fix_z

    @f_fix_z.setter
    def f_fix_z(self, f_val):
        """
        set Z
        """
        self._f_fix_z = f_val

# < the end >--------------------------------------------------------------------------------------
