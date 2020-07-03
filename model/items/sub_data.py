# -*- coding: utf-8 -*-
"""
sub_data

mantém as informações sobre o dicionário de procedimento de subidas

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import sys

# PyQt library
from PyQt5 import QtCore
# FIXME QtXml is no longer supported.
from PyQt5 import QtXml

# model
import model.items.sub_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as event

# < module data >----------------------------------------------------------------------------------

# logger
# M_LOG = logging.getLogger(__name__)
# M_LOG.setLevel(logging.DEBUG)

# < class CSubData >-------------------------------------------------------------------------------

class CSubData(dict):
    """
    mantém as informações sobre o dicionário de procedimento de subida

    <subida nSub="1">
        <descricao>BGC 2A</descricao>
        <aerodromo>SBGR</aerodromo>
        <pista>09R</pista>

        <breakpoint nBrk="1"> ... </breakpoint>
    </subida>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None):
        """
        @param f_model: model manager
        @param f_data: dados dos procedimentos de subida
        """
        # logger
        # M_LOG.info("__init__:>>")
        
        # check input
        assert f_model

        # inicia a super class
        super(CSubData, self).__init__()

        # salva o model manager
        self._model = f_model

        # salva o event manager
        self._event = f_model.event

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, list):
                # cria um procedimento de subida com os dados da lista
                # self._make_sub(f_data)
                pass

            # recebeu um procedimento de subida ?
            elif isinstance(f_data, CSubData):
                # copia o procedimento de subida
                # self.copy_sub(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de procedimento de subida
            else:
                # carrega o dicionário de procedimento de subida de um arquivo em disco
                self._load_file(f_data)

    # ---------------------------------------------------------------------------------------------
    def _load_file(self, fs_sub_pn):
        """
        carrega os dados do procedimento de subida de um arquivo em disco

        @param fs_sub_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("_load_file:>>")
        
        # check input
        assert fs_sub_pn

        # carrega o arquivo de procedimento de subida
        self._parse_sub_xml(fs_sub_pn + ".xml")

    # ---------------------------------------------------------------------------------------------
    def _make_sub(self, fdct_root, fdct_data):
        """
        carrega os dados de procedimento de subida a partir de um dicionário

        @param f_lstData: lista de dados de procedimento de subida

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("_make_sub:>>")
        
        # check input
        assert fdct_root is not None
        assert fdct_data is not None

        # é uma procedimento de subida do newton ?
        if "subidas" != fdct_root["tagName"]:
            # logger
            l_log = logging.getLogger("CCSubData::_make_sub")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E01: não é um arquivo de procedimentos de subida.")
                                                
            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é um arquivo do newton ?
        if "NEWTON" != fdct_root["FORMAT"]:
            # logger
            l_log = logging.getLogger("CCSubData::_make_sub")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E02: não está em um formato aceito.")
                                                
            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # é a assinatura do newton ?
        if "1961" != fdct_root["CODE"]:
            # logger
            l_log = logging.getLogger("CCSubData::_make_sub")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E03: não tem a assinatura correta.")
                                                
            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # se não for, cai fora...
            sys.exit(1)

        # verifica se existe identificação
        if "nSub" in fdct_data:
            # cria procedimento de subida
            l_sub = model.CSubNEW(self._model, fdct_data, fdct_root["VERSION"])
            assert l_sub

            # coloca a procedimento de subida no dicionário
            self[fdct_data["nSub"]] = l_sub

        # senão, não existe identificação
        else:
            # monta uma mensagem
            ls_msg = "não tem identificação. Subida não incluída."

            # logger
            l_log = logging.getLogger("CCSubData::_make_sub")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # retorna Ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def _parse_sub_xml(self, fs_sub_pn):
        """
        carrega o arquivo de procedimentos de subida

        @param fs_sub_pn: pathname do arquivo em disco
        """
        # logger
        # M_LOG.info("_parse_sub_xml:>>")
        
        # check input
        assert fs_sub_pn

        # cria o QFile para o arquivo XML do procedimentos de subida
        l_data_file = QtCore.QFile(fs_sub_pn)
        assert l_data_file is not None

        # abre o arquivo XML do procedimentos de subida
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():
            # logger
            l_log = logging.getLogger("CCSubData::_parse_sub_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E01: erro na abertura de {}.".format(fs_sub_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do procedimento de subida
        # FIXME QtXml is no longer supported.
        l_xdoc_sub = QtXml.QDomDocument("subidas")
        assert l_xdoc_sub is not None

        # erro na carga do documento ?
        if not l_xdoc_sub.setContent(l_data_file):
            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CCSubData::_parse_sub_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E02: falha no parse de {}.".format(fs_sub_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # fecha o arquivo
        l_data_file.close()

        # obtém o elemento raíz do documento
        l_elem_root = l_xdoc_sub.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de procedimento de subida
        l_node_list = l_elem_root.elementsByTagName("subida")

        # para todos os nós na lista...
        for li_ndx in range(l_node_list.length()):
            # inicia o dicionário de dados
            ldct_data = {}

            # inicia a lista de breakpoints
            ldct_data["breakpoints"] = []

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nSub"):
                ldct_data["nSub"] = int(l_element.attribute("nSub"))

            # obtém o primeiro nó da sub-árvore
            l_node = l_element.firstChild()
            assert l_node is not None

            # percorre a sub-árvore
            while not l_node.isNull():
                # tenta converter o nó em um elemento
                l_element = l_node.toElement()
                assert l_element is not None

                # o nó é um elemento ?
                if not l_element.isNull():
                    # faz o parse do elemento
                    ldct_tmp = parser.parse_subida(l_element)

                    # tem breakpoint ?
                    if "breakpoint" in ldct_tmp:
                        # atualiza o dicionário com o breakpoint
                        ldct_data["breakpoints"].append(ldct_tmp["breakpoint"])

                        # apaga este elemento
                        del ldct_tmp["breakpoint"]

                    # atualiza o dicionário de dados
                    ldct_data.update(ldct_tmp)

                # próximo nó
                l_node = l_node.nextSibling()
                assert l_node is not None

            # carrega os dados de procedimento de subida a partir de um dicionário
            self._make_sub(ldct_root, ldct_data)

    # ---------------------------------------------------------------------------------------------
    def save2disk(self, fs_sub_pn=None):
        """
        salva os dados da procedimento de subida em um arquivo em disco

        @param fs_sub_pn: path name do arquivo onde salvar

        @return flag e mensagem
        """
        # logger
        # M_LOG.info("save2disk:>>")
        
        # return code
        lv_ok = True

        # mensagem
        ls_msg = "save ok"

        # retorna flag e mensagem
        return lv_ok, ls_msg

# < the end >--------------------------------------------------------------------------------------
