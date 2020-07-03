# -*- coding: utf-8 -*-
"""
esp_data

mantém as informações sobre o dicionário de procedimento de esperas

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
import model.items.esp_new as model
import model.items.parser_utils as parser

# control
import control.events.events_basic as events

# < class CEspData >-------------------------------------------------------------------------------

class CEspData(dict):
    """
    mantém as informações sobre o dicionário de procedimento de espera

    <espera nEsp="1">
        <descricao>Espera IND (274D)</descricao>
        <fixo>IND</fixo>
        <sentido>D</sentido>
        <rumo>274</rumo>
        <declmag>-21</declmag>
    </espera>
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_model, f_data=None):
        """
        @param f_model: model manager
        @param f_data: dados dos procedimento de esperas
        """
        # check input
        assert f_model

        # inicia a super class
        super(CEspData, self).__init__()

        # salva o model manager localmente
        self._model = f_model

        # salva o event manager localmente
        self._event = f_model.event

        # recebeu dados ?
        if f_data is not None:
            # recebeu uma lista ?
            if isinstance(f_data, list):
                # cria um procedimento de espera com os dados da lista
                # self.make_esp(f_data)
                pass

            # recebeu um procedimento de espera ?
            elif isinstance(f_data, CEspData):
                # copia o procedimento de espera
                # self.copy_esp(f_data)
                pass

            # senão, recebeu o pathname de um arquivo de procedimento de espera
            else:
                # carrega o dicionário de procedimento de espera de um arquivo em disco
                self.load_file(f_data)

    # ---------------------------------------------------------------------------------------------
    def load_file(self, fs_esp_pn):
        """
        carrega os dados do procedimento de espera de um arquivo em disco

        @param fs_esp_pn: pathname do arquivo em disco
        """
        # check input
        assert fs_esp_pn

        # carrega o arquivo de procedimento de espera
        self.parse_esp_xml(fs_esp_pn + ".xml")

    # ---------------------------------------------------------------------------------------------
    def make_esp(self, fdct_root, fdct_data):
        """
        carrega os dados de procedimento de espera a partir de um dicionário

        @param fdct_data: lista de dados de procedimento de espera

        @return flag e mensagem
        """
        # check input
        assert fdct_root is not None
        assert fdct_data is not None

        # é um procedimento de espera do newton ?
        if "esperas" != fdct_root["tagName"]:
            # logger
            l_log = logging.getLogger("CEspData::make_esp")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E01: não é um arquivo de procedimento de espera.")

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
            l_log = logging.getLogger("CEspData::make_esp")
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
            l_log = logging.getLogger("CEspData::make_esp")
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
        if "nEsp" in fdct_data:
            # cria procedimento de espera
            l_esp = model.CEspNEW(self._model, fdct_data, fdct_root["VERSION"])
            assert l_esp

            # coloca a procedimento de espera no dicionário
            self[fdct_data["nEsp"]] = l_esp

        # senão, não existe identificação
        else:
            # monta uma mensagem
            ls_msg = "não tem identificação. Espera não incluída."

            # logger
            l_log = logging.getLogger("CEspData::make_esp")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E04: {}".format(ls_msg))

            # se não for, cai fora...
            return False, ls_msg

        # retorna Ok
        return True, None

    # ---------------------------------------------------------------------------------------------
    def parse_esp_xml(self, fs_esp_pn):
        """
        carrega o arquivo de procedimentos de espera

        @param fs_esp_pn: pathname do arquivo em disco
        """
        # check input
        assert fs_esp_pn

        # cria o QFile para o arquivo XML do procedimentos de espera
        l_data_file = QtCore.QFile(fs_esp_pn)
        assert l_data_file is not None

        # abre o arquivo XML do procedimentos de espera
        l_data_file.open(QtCore.QIODevice.ReadOnly)

        # erro na abertura do arquivo ?
        if not l_data_file.isOpen():
            # logger
            l_log = logging.getLogger("CEspData::parse_esp_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E01: erro na abertura de {}".format(fs_esp_pn))

            # cria um evento de quit
            l_evt = events.CQuit()
            assert l_evt

            # dissemina o evento
            self._event.post(l_evt)

            # termina a aplicação
            sys.exit(1)

        # cria o documento XML do procedimento de espera
        # FIXME QtXml is no longer supported.
        l_xdoc_esp = QtXml.QDomDocument("esperas")
        assert l_xdoc_esp is not None

        # erro na carga do documento ?
        if not l_xdoc_esp.setContent(l_data_file):
            # fecha o arquivo
            l_data_file.close()

            # logger
            l_log = logging.getLogger("CEspData::parse_esp_xml")
            l_log.setLevel(logging.CRITICAL)
            l_log.critical("<E02: falha no parse de {}".format(fs_esp_pn))

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
        l_elem_root = l_xdoc_esp.documentElement()
        assert l_elem_root is not None

        # faz o parse dos atributos do elemento raíz
        ldct_root = parser.parse_root_element(l_elem_root)

        # cria uma lista com os elementos de procedimento de espera
        l_node_list = l_elem_root.elementsByTagName("espera")

        # para todos os nós na lista...
        for li_ndx in range(l_node_list.length()):
            # inicia o dicionário de dados
            ldct_data = {}

            # inicia a lista de break-points
            ldct_data["breakpoints"] = []

            # obtém um nó da lista
            l_element = l_node_list.at(li_ndx).toElement()
            assert l_element is not None

            # read identification if available
            if l_element.hasAttribute("nEsp"):
                ldct_data["nEsp"] = int(l_element.attribute("nEsp"))

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
                    ldct_tmp = parser.parse_espera(l_element)

                    # atualiza o dicionário com o breakpoint
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

            # carrega os dados de procedimento de espera a partir de um dicionário
            self.make_esp(ldct_root, ldct_data)

    # ---------------------------------------------------------------------------------------------
    def save2disk(self, fs_esp_pn=None):
        """
        salva os dados da procedimento de espera em um arquivo em disco

        @param fs_esp_pn: path name do arquivo onde salvar

        @return flag e mensagem
        """
        # return code
        lv_ok = True

        # mensagem
        ls_msg = "save Ok"

        # retorna flag e mensagem
        return lv_ok, ls_msg

# < the end >--------------------------------------------------------------------------------------
