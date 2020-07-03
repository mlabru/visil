# -*- coding: utf-8 -*-
"""
config_visil

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < import >---------------------------------------------------------------------------------------

# python library
import argparse
import os

# model 
import model.common.data as data

# control
import control.config.config_manager as config

# < class CConfigVisil >---------------------------------------------------------------------------

class CConfigVisil(config.CConfigManager):
    """
    mantém as informações de configuração
    """
    # informações comuns de configuração
    __CFG_VISIL = {}  # __CFG_VISIL

    # ---------------------------------------------------------------------------------------------
    def __init__(self, fs_cnfg):
        """
        constructor
        inicia o gerente de configuração

        @param fs_cnfg: full path do arquivo de configuração
        """
        # inicia a super class
        super(CConfigVisil, self).__init__(fs_cnfg)

        # herdados de CConfigManager
        # self.dct_config    # config manager data dictionary

        # carrega os atributos locais no dicionário de configuração
        for l_key in list(self.__CFG_VISIL.keys()):
            if l_key not in self.dct_config:
                self.dct_config[l_key] = self.__CFG_VISIL[l_key]

        # cria um parser para os argumentos
        l_parser = argparse.ArgumentParser(description="ViSIL (C) 2014-2016.")
        assert l_parser

        # argumento: canal de comunicação
        l_parser.add_argument("-c", "--canal",
                              dest="canal",
                              default=self.dct_config["glb.canal"],
                              help="Canal de comunicação (default: %d)" % int(self.dct_config["glb.canal"]))

        # faz o parser da linha de argumentos
        l_args = l_parser.parse_args()
        assert l_args

        # salva os argumentos no dicionário
        self.dct_config["glb.canal"] = abs(int(l_args.canal))

        # load dirs section
        self.load_dirs()

# < the end >--------------------------------------------------------------------------------------
