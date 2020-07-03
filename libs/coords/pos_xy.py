# -*- coding: utf-8 -*-
"""
pos_xy

revision 1.1  2015/dez  mlabru
pep8 style conventions

revision 1.0  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < CPosXY >---------------------------------------------------------------------------------------

class CPosXY(object):
    """
    CPosXY
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, ff_x=0., ff_y=0.):
        """
        constructor
        """
        # logger
        # M_LOG.info(">> constructor")

        # check input
        # assert ff_x
        # assert ff_y

        # inicia a super classe
        super(CPosXY, self).__init__()

        self.__f_x = ff_x
        # M_LOG.debug("self.__f_x:[%f]", self.__f_x)

        self.__f_y = ff_y
        # M_LOG.debug("self.__f_y:[%f]", self.__f_y)

    # ---------------------------------------------------------------------------------------------
    def __str__(self):
        """
        str magic method
        """
        # return
        return "{}/{}".format(self.__f_x, self.__f_y)

    # =============================================================================================
    # data
    # =============================================================================================

    # ---------------------------------------------------------------------------------------------
    @property
    def f_x(self):
        """X"""
        return self.__f_x
                                            
    @f_x.setter
    def f_x(self, f_val):
        """X"""
        self.__f_x = f_val

    # ---------------------------------------------------------------------------------------------
    @property
    def f_y(self):
        """Y"""
        return self.__f_y
                                            
    @f_y.setter
    def f_y(self, f_val):
        """Y"""
        self.__f_y = f_val

# < the end >--------------------------------------------------------------------------------------
