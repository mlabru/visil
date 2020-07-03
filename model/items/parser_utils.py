# -*- coding: utf-8 -*-
"""
parse_utils

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2015/out  mlabru
initial release (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# PyQt library
from PyQt5 import QtCore

# -------------------------------------------------------------------------------------------------
def parse_aerodromo(f_element):
    """
    helper function to parse xml entries

    <aerodromo nAer="SBSP">
      <descricao>Congonhas</descricao>
      <coord> ... </coord>
      <elevacao>2189</elevacao>
      <declmag>-21</declmag>
      <pista> ... </pista>
    </aerodromo>

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle descrição (nome)
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle elevação
    elif "elevacao" == f_element.tagName():
        ldct_tmp["elevacao"] = f_element.text()

    # handle declmag
    elif "declmag" == f_element.tagName():
        ldct_tmp["declmag"] = f_element.text()

    # handle coord
    elif "coord" == f_element.tagName():
        ldct_tmp["coord"] = _parse_crd(f_element)

    # handle posição
    elif "pista" == f_element.tagName():
        # inicia o dicionário de dados
        ldct_pst = {}

        # read identification if available
        if f_element.hasAttribute("nPst"):
            ldct_pst["nPst"] = str(f_element.attribute("nPst"))

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():
            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():
                # atualiza o dicionário de dados
                ldct_pst.update(parse_pista(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a pista
        ldct_tmp["pista"] = ldct_pst

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_aeronave(f_element, f_hora_ini):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle indicativo (ID)
    if "indicativo" == f_element.tagName():
        ldct_tmp["indicativo"] = f_element.text()

    # handle descrição
    elif "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle designador
    elif "designador" == f_element.tagName():
        ldct_tmp["designador"] = f_element.text()

    # handle ssr
    elif "ssr" == f_element.tagName():
        ldct_tmp["ssr"] = f_element.text()

    # handle origem
    elif "origem" == f_element.tagName():
        ldct_tmp["origem"] = f_element.text()

    # handle destino
    elif "destino" == f_element.tagName():
        ldct_tmp["destino"] = f_element.text()

    # handle procedimen
    elif "procedimento" == f_element.tagName():
        ldct_tmp["procedimento"] = f_element.text()

    # handle nivel
    elif "nivel" == f_element.tagName():
        ldct_tmp["nivel"] = f_element.text()

    # handle altitude
    elif "altitude" == f_element.tagName():
        ldct_tmp["altitude"] = f_element.text()

    # handle velocidade
    elif "velocidade" == f_element.tagName():
        ldct_tmp["velocidade"] = f_element.text()

    # handle proa
    elif "proa" == f_element.tagName():
        ldct_tmp["proa"] = f_element.text()

    # handle pilotagem
    elif "pilotagem" == f_element.tagName():
        ldct_tmp["pilotagem"] = f_element.text()

    # handle temptrafeg
    elif "temptrafeg" == f_element.tagName():
        # salva a tupla com a hora inicial corrigida
        ldct_tmp["temptrafeg"] = (f_element.text(), f_hora_ini)

    # handle numsg
    elif "numsg" == f_element.tagName():
        ldct_tmp["numsg"] = f_element.text()

    # handle tempmsg
    elif "tempmsg" == f_element.tagName():
        ldct_tmp["tempmsg"] = f_element.text()

    # handle rvsm
    elif "rvsm" == f_element.tagName():
        ldct_tmp["rvsm"] = f_element.text()

    # handle rota
    elif "rota" == f_element.tagName():
        ldct_tmp["rota"] = f_element.text()

    # handle eet
    elif "eet" == f_element.tagName():
        ldct_tmp["eet"] = f_element.text()

    # handle posição
    elif "posicao" == f_element.tagName():
        # inicia o dicionário de dados
        ldct_pos = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():
            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():
                # atualiza o dicionário de dados
                ldct_pos.update(parse_posicao(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a posição
        ldct_tmp["posicao"] = ldct_pos

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_aproximacao(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle descricao
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle aeródromo
    if "aerodromo" == f_element.tagName():
        ldct_tmp["aerodromo"] = f_element.text()

    # handle pista
    elif "pista" == f_element.tagName():
        ldct_tmp["pista"] = f_element.text()

    # handle flag ILS
    elif "ils" == f_element.tagName():
        ldct_tmp["ils"] = f_element.text()

    # handle flag apxPerdida
    elif "aproxperd" == f_element.tagName():
        ldct_tmp["aproxperd"] = f_element.text()

    # handle número da espera
    elif "espera" == f_element.tagName():
        ldct_tmp["espera"] = f_element.text()

    # handle breakpoint
    elif "breakpoint" == f_element.tagName():
        ldct_tmp["breakpoint"] = _parse_bkp(f_element)

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def _parse_bkp(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_brk = {}

    # read identification if available
    if f_element.hasAttribute("nBrk"):
        ldct_brk["nBrk"] = int(f_element.attribute("nBrk"))

    # obtém o primeiro nó da sub-árvore
    l_node = f_element.firstChild()
    assert l_node is not None

    # percorre a sub-árvore...
    while not l_node.isNull():
        # tenta converter o nó em um elemento
        l_element = l_node.toElement()
        assert l_element is not None

        # o nó é um elemento ?
        if not l_element.isNull():
            # atualiza o dicionário de dados
            ldct_brk.update(parse_breakpoint(l_element))

        # próximo nó
        l_node = l_node.nextSibling()
        assert l_node is not None

    # retorna o dicionário de dados
    return ldct_brk

# -------------------------------------------------------------------------------------------------
def parse_breakpoint(f_element):
    """
    helper function to parse xml entries

    <breakpoint nBrk="1">
      <coord>
        ...
      </coord>  
      <altitude>5200</altitude>
      <velocidade>200</velocidade>
      <razdes>800</razdes>
      <razsub>800</razsub>
      <procedimento>ESP032</procedimento>
    </breakpoint>

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle altitude
    if "altitude" == f_element.tagName():
        ldct_tmp["altitude"] = f_element.text()

    # handle velocidade
    elif "velocidade" == f_element.tagName():
        ldct_tmp["velocidade"] = f_element.text()

    # handle razdes
    elif "razdes" == f_element.tagName():
        ldct_tmp["razdes"] = f_element.text()

    # handle razsub
    elif "razsub" == f_element.tagName():
        ldct_tmp["razsub"] = f_element.text()

    # handle procedimento
    elif "procedimento" == f_element.tagName():
        ldct_tmp["procedimento"] = f_element.text()

    # handle coord
    elif "coord" == f_element.tagName():
        ldct_tmp["coord"] = _parse_crd(f_element)

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_coord(f_element):
    """
    helper function to parse xml entries

    <coord>
      <tipo>F</tipo>
      <cpoA>IND</cpoA>
      <cpoB>5</cpoB>
      <cpoC>338</cpoC>
      <cpoD>1.5</cpoD>
    </coord>

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case tipo de coordenada
    if "tipo" == f_element.tagName():
        ldct_tmp["tipo"] = f_element.text()

    # handle latitude/X/cpoA
    elif "cpoA" == f_element.tagName():
        ldct_tmp["cpoA"] = f_element.text()

    # handle longitude/Y/cpoB
    elif "cpoB" == f_element.tagName():
        ldct_tmp["cpoB"] = f_element.text()

    # handle cpoC
    elif "cpoC" == f_element.tagName():
        ldct_tmp["cpoC"] = f_element.text()

    # handle cpoD
    elif "cpoD" == f_element.tagName():
        ldct_tmp["cpoD"] = f_element.text()

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def _parse_crd(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_crd = {}

    # obtém o primeiro nó da sub-árvore
    l_node = f_element.firstChild()
    assert l_node is not None

    # percorre a sub-árvore
    while not l_node.isNull():
        # tenta converter o nó em um elemento
        l_element = l_node.toElement()
        assert l_element is not None

        # o nó é um elemento ?
        if not l_element.isNull():
            # atualiza o dicionário de dados
            ldct_crd.update(parse_coord(l_element))

        # próximo nó
        l_node = l_node.nextSibling()
        assert l_node is not None

    # retorna o dicionário de dados
    return ldct_crd

# -------------------------------------------------------------------------------------------------
def parse_espera(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle descricao (nome)
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle fixo (descrição)
    elif "fixo" == f_element.tagName():
        ldct_tmp["fixo"] = f_element.text()

    # handle sentido
    elif "sentido" == f_element.tagName():
        ldct_tmp["sentido"] = f_element.text()

    # handle rumo
    elif "rumo" == f_element.tagName():
        ldct_tmp["rumo"] = f_element.text()

    # handle declmag
    elif "declmag" == f_element.tagName():
        ldct_tmp["declmag"] = f_element.text()

    # handle breakpoint
    elif "breakpoint" == f_element.tagName():
        ldct_tmp["breakpoint"] = _parse_bkp(f_element)

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_exercicio(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle descrição
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle hora início
    elif "horainicio" == f_element.tagName():
        ldct_tmp["horainicio"] = f_element.text()

    # handle meteorologia
    elif "meteorologia" == f_element.tagName():
        # inicia o dicionário de dados
        ldct_met = {}

        # obtém o primeiro nó da sub-árvore
        lo_node = f_element.firstChild()
        assert lo_node is not None

        # percorre a sub-árvore
        while not lo_node.isNull():
            # tenta converter o nó em um elemento
            lo_element = lo_node.toElement()
            assert lo_element is not None

            # o nó é um elemento ?
            if not lo_element.isNull():
                # atualiza o dicionário de dados
                ldct_met.update(parse_meteorologia(lo_element))

            # próximo nó
            lo_node = lo_node.nextSibling()
            assert lo_node is not None

        # atualiza o dicionário com a meteorologia
        ldct_tmp["meteorologia"] = ldct_met
    '''
    # handle consoles
    elif "consoles" == f_element.tagName():
        # inicia a lista de consoles
        l_lstCon = []

        l_node_list = f_element.elementsByTagName("console"))

        # obtém o primeiro nó da sub-árvore
        lo_node = f_element.firstChild()
        assert(lo_node is not None

        # percorre a sub-árvore
        while not lo_node.isNull():
            # tenta converter o nó em um elemento
            lo_element = lo_node.toElement()
            assert lo_element is not None

            # o nó é um elemento ?
            if not lo_element.isNull():
                # atualiza o dicionário de dados
                l_lstCon.append(parseConsole(lo_element))

            # próximo nó
            lo_node = lo_node.nextSibling()
            assert lo_node is not None

        # atualiza o dicionário com a lista de consoles
        ldct_tmp["consoles"] = l_lstCon

    # handle mapas
    elif "mapas" == f_element.tagName():
        # inicia a lista de mapas
        l_lstMap = []

        l_node_list = f_element.elementsByTagName("subMapa"))

        for li_ndx in xrange(l_node_list.length()):
            lo_element = l_node_list.at(li_ndx).toElement()
            assert lo_element is not None

            # faz o parse do elemento
            l_lstMap.append(parse_mapa(lo_element))

        # atualiza o dicionário com a lista de consoles
        ldct_tmp["mapas"] = l_lstMap

    # handle situação
    elif "situacao" == f_element.tagName():
        # inicia o dicionário de situacao
        ldctSit = {}

        # obtém o primeiro nó da sub-árvore
        lo_node = f_element.firstChild()
        assert lo_node is not None

        # percorre a sub-árvore
        while(not lo_node.isNull()):
            # tenta converter o nó em um elemento
            lo_element = lo_node.toElement()
            assert lo_element is not None

            # o nó é um elemento ?
            if not lo_element.isNull():
                # faz o parse do elemento
                ldctSit.update(parse_situacao(lo_element))

            # próximo nó
            lo_node = lo_node.nextSibling()
            assert lo_node is not None

        # atualiza o dicionário com a lista de consoles
        ldct_tmp["situacao"] = ldctSit
    '''
    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_fixo(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle indicativo
    if "indicativo" == f_element.tagName():
        ldct_tmp["indicativo"] = f_element.text()

    # handle descrição
    elif "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle tipo
    elif "tipo" == f_element.tagName():
        ldct_tmp["tipo"] = f_element.text()

    # handle posição
    elif "coord" == f_element.tagName():
        ldct_tmp["coord"] = _parse_crd(f_element)

    # handle VOR
    # elif "VOR" == f_element.tagName():
        # ldct_tmp["VOR"] = f_element.text()

    # handle NDB
    # elif "NDB" == f_element.tagName():
        # ldct_tmp["NDB"] = f_element.text()

    # handle DME
    # elif "DME" == f_element.tagName():
        # ldct_tmp["DME"] = f_element.text()

    # handle freqüência
    # elif "frequencia" == f_element.tagName():
        # ldct_tmp["frequencia"] = f_element.text()

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
'''def parse_hora(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_data = {}

    # handle hora
    if "hora" == f_element.tagName():
        ldct_data["hora"] = f_element.text()

    # handle minutos
    elif "min" == f_element.tagName():
        ldct_data["min"] = f_element.text()

    # retorna o dicionário de dados
    return ldct_data
'''
# -------------------------------------------------------------------------------------------------
def parse_ils(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle aerodromo
    if "aerodromo" == f_element.tagName():
        ldct_tmp["aerodromo"] = f_element.text()

    # handle pista
    elif "pista" == f_element.tagName():
        ldct_tmp["pista"] = f_element.text()

    # handle altitudegp
    elif "altitudegp" == f_element.tagName():
        ldct_tmp["altitudegp"] = f_element.text()

    # handle angrampa
    elif "angrampa" == f_element.tagName():
        ldct_tmp["angrampa"] = f_element.text()

    # handle altitmapt
    elif "altitmapt" == f_element.tagName():
        ldct_tmp["altitmapt"] = f_element.text()

    # handle procedimento
    elif "procedimento" == f_element.tagName():
        ldct_tmp["procedimento"] = f_element.text()

    # handle breakpoint
    elif "breakpoint" == f_element.tagName():
        ldct_tmp["breakpoint"] = _parse_bkp(f_element)

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
'''def parse_mapa(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # handle subMapa
    if "subMapa" == f_element.tagName():
        li_num = f_element.text()

    # retorna o número do mapa
    return li_num
'''
# -------------------------------------------------------------------------------------------------
def parse_meteorologia(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle altitude de transição
    if "alttrans" == f_element.tagName():
        ldct_tmp["alttrans"] = f_element.text()

    # handle indicativo de condição meteorológica
    elif "condmet" == f_element.tagName():
        ldct_tmp["condmet"] = f_element.text()

    # handle limite inferior do QNH
    elif "infqnh" == f_element.tagName():
        ldct_tmp["infqnh"] = f_element.text()

    # handle número da formação meteorológica
    elif "numForm" == f_element.tagName():
        ldct_tmp["numForm"] = f_element.text()

    # handle pendente do QNH
    elif "pendqnh" == f_element.tagName():
        ldct_tmp["pendqnh"] = f_element.text()

    # handle QNH
    elif "qnh" == f_element.tagName():
        ldct_tmp["qnh"] = f_element.text()

    # handle limite superior do QNH
    elif "supqnh" == f_element.tagName():
        ldct_tmp["supqnh"] = f_element.text()

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_performance(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle descrição
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle esteira
    elif "esteira" == f_element.tagName():
        ldct_tmp["esteira"] = f_element.text()

    # handle teto de serviço (DIST) / altitude máxima
    elif "tetosv" == f_element.tagName():
        ldct_tmp["tetosv"] = f_element.text()

    # handle faixa
    elif "faixa" == f_element.tagName():
        ldct_tmp["faixa"] = f_element.text()

    # handle velocidade de decolagem (VELO) / velocidade mínima de decolagem
    elif "veldec" == f_element.tagName():
        ldct_tmp["veldec"] = f_element.text()

    # handle velocidade de subida na decolagem (VELO) / velocidade de subida
    elif "velsbdec" == f_element.tagName():
        ldct_tmp["velsbdec"] = f_element.text()

    # handle velocidade de aproximação (VELO) / velocidade máxima de pouso
    elif "velapx" == f_element.tagName():
        ldct_tmp["velapx"] = f_element.text()

    # handle velocidade de cruzeiro (VELO)
    elif "velcruz" == f_element.tagName():
        ldct_tmp["velcruz"] = f_element.text()

    # handle velocidade máxima de cruzeiro (VELO) / velocidade máxima
    elif "velmxcrz" == f_element.tagName():
        ldct_tmp["velmxcrz"] = f_element.text()

    # handle razão de subida na decolagem (VELO)
    elif "rzsubdec" == f_element.tagName():
        ldct_tmp["rzsubdec"] = f_element.text()

    # handle razão máxima subida na decolagem (VELO)
    elif "rzmxsbdec" == f_element.tagName():
        ldct_tmp["rzmxsbdec"] = f_element.text()

    # handle razão de subida de cruzeiro (VELO) / razão de subida
    elif "rzsbcrz" == f_element.tagName():
        ldct_tmp["rzsbcrz"] = f_element.text()

    # handle razão máxima de subida de cruzeiro (VELO)
    elif "rzmxsbcrz" == f_element.tagName():
        ldct_tmp["rzmxsbcrz"] = f_element.text()

    # handle razão de descida na aproximação (VELO)
    elif "rzdescapx" == f_element.tagName():
        ldct_tmp["rzdescapx"] = f_element.text()

    # handle razão máxima descida na aproximação (VELO)
    elif "rzmxdesapx" == f_element.tagName():
        ldct_tmp["rzmxdesapx"] = f_element.text()

    # handle razão de descida de cruzeiro (VELO) / razão de descida
    elif "rzdescrz" == f_element.tagName():
        ldct_tmp["rzdescrz"] = f_element.text()

    # handle razão máxima descida de cruzeiro (VELO) / razão máxima de descida
    elif "rzmxdescrz" == f_element.tagName():
        ldct_tmp["rzmxdescrz"] = f_element.text()

    # handle razão de variação de velocidade (aceleração) (ACEL) / aceleração de vôo
    elif "razvarvel" == f_element.tagName():
        ldct_tmp["razvarvel"] = f_element.text()

    # handle razão máxima variação de velocidade (aceleração) (ACEL)
    elif "rzmxvarvel" == f_element.tagName():
        ldct_tmp["rzmxvarvel"] = f_element.text()
    '''
    # handle desaceleração de vôo
    elif "desacelcrz" == f_element.tagName():
        ldct_tmp["desacelcrz"] = f_element.text()

    # handle aceleração mínima de decolagem
    elif "acelmindep" == f_element.tagName():
        ldct_tmp["acelmindep"] = f_element.text()

    # handle desaceleração máxima de pouso
    elif "desacelmaxarr" == f_element.tagName():
        ldct_tmp["desacelmaxarr"] = f_element.text()

    # handle velocidade de circuito
    elif "velckt" == f_element.tagName():
        ldct_tmp["velckt"] = f_element.text()

    # handle altitude de circuito
    elif "altckt" == f_element.tagName():
        ldct_tmp["altckt"] = f_element.text()

    # handle circuito
    elif "numckt" == f_element.tagName():
        ldct_tmp["numckt"] = f_element.text()

    # handle razão de curva em rota
    elif "razcrvrot" == f_element.tagName():
        ldct_tmp["razcrvrot"] = f_element.text()

    # handle razão de curva no solo
    elif "razcrvslo" == f_element.tagName():
        ldct_tmp["razcrvslo"] = f_element.text()

    # handle razão de curva no tráfego
    elif "razcrvtrf" == f_element.tagName():
        ldct_tmp["razcrvtrf"] = f_element.text()

    # handle velocidade máxima de taxi
    elif "velmaxtax" == f_element.tagName():
        ldct_tmp["velmaxtax"] = f_element.text()
    '''
    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_pista(f_element):
    """
    helper function to parse xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle identificação (ID)
    if "nPst" == f_element.tagName():
        ldct_tmp["nPst"] = f_element.text()

    # handle comprimento
    # elif "comprimento" == f_element.tagName():
        # ldct_tmp["comprimento"] = f_element.text()

    # handle largura
    # elif "largura" == f_element.tagName():
        # ldct_tmp["largura"] = f_element.text()

    # handle rumo
    elif "rumo" == f_element.tagName():
        ldct_tmp["rumo"] = f_element.text()

    # handle coord
    elif "coord" == f_element.tagName():
        ldct_tmp["coord"] = _parse_crd(f_element)

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_posicao(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle case tipo de coordenada
    if "tipocoord" == f_element.tagName():
        ldct_tmp["tipocoord"] = f_element.text()

    # handle X/cpoA
    elif "latitude" == f_element.tagName():
        ldct_tmp["latitude"] = f_element.text()

    # handle Y/cpoB
    elif "longitude" == f_element.tagName():
        ldct_tmp["longitude"] = f_element.text()

    # handle Z/cpoC
    elif "cpoC" == f_element.tagName():
        ldct_tmp["cpoC"] = f_element.text()

    # handle cpoD
    elif "cpoD" == f_element.tagName():
        ldct_tmp["cpoD"] = f_element.text()

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_radar(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle ID
    if "indicativo" == f_element.tagName():
        ldct_tmp["indicativo"] = f_element.text()

    # handle descrição
    elif "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle elevação
    elif "elevacao" == f_element.tagName():
        ldct_tmp["elevacao"] = f_element.text()

    # handle alcancehor
    elif "alcancehor" == f_element.tagName():
        ldct_tmp["alcancehor"] = f_element.text()

    # handle alcancever
    elif "alcancever" == f_element.tagName():
        ldct_tmp["alcancever"] = f_element.text()

    # handle alcancesec
    elif "alcancesec" == f_element.tagName():
        ldct_tmp["alcancesec"] = f_element.text()

    # handle angmin
    elif "angmin" == f_element.tagName():
        ldct_tmp["angmin"] = f_element.text()

    # handle angmax
    elif "angmax" == f_element.tagName():
        ldct_tmp["angmax"] = f_element.text()

    # handle posição
    elif "posicao" == f_element.tagName():
        # inicia o dicionário de dados
        ldct_pos = {}

        # obtém o primeiro nó da sub-árvore
        l_node = f_element.firstChild()
        assert l_node is not None

        # percorre a sub-árvore
        while not l_node.isNull():
            # tenta converter o nó em um elemento
            l_element = l_node.toElement()
            assert l_element is not None

            # o nó é um elemento ?
            if not l_element.isNull():
                # atualiza o dicionário de dados
                ldct_pos.update(parse_posicao(l_element))

            # próximo nó
            l_node = l_node.nextSibling()
            assert l_node is not None

        # atualiza o dicionário com a posição
        ldct_tmp["posicao"] = ldct_pos

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_root_element(f_element):
    """
    helper function to parse xml entries

    @param f_element: root element to parse
    """
    # inicia o dicionário de dados
    ldct_root = {}

    # salva o tagName
    # ldct_root["tagName"] = f_element.tagName()
    ldct_root["tagName"] = f_element.tagName()

    # para todos os atributos...
    for li_ndx in range(f_element.attributes().size()):
        # obtém o atributo
        l_attr = f_element.attributes().item(li_ndx).toAttr()

        # associa o atributo ao valor
        # ldct_root[str(l_attr.name()).upper()] = l_attr.value()
        ldct_root[str(l_attr.name()).upper()] = l_attr.value()

    # retorna o dicionário de dados
    return ldct_root

# -------------------------------------------------------------------------------------------------
'''def parse_situacao(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_data = {}

    # handle hora de início
    if "horaIni" == f_element.tagName():
        # inicia o dicionário de situacao
        ldct_hor = {}

        # obtém o primeiro nó da sub-árvore
        lo_node = f_element.firstChild()
        assert lo_node is not None

        # percorre a sub-árvore
        while not lo_node.isNull():
            # tenta converter o nó em um elemento
            lo_element = lo_node.toElement()

            assert lo_element is not None

            # o nó é um elemento ?
            if not lo_element.isNull():
                # faz o parse do elemento
                ldct_hor.update(parse_hora(lo_element))

            # próximo nó
            lo_node = lo_node.nextSibling()
            assert lo_node is not None

        # atualiza o dicionário com a lista de consoles
        ldct_data["horaIni"] = ldct_hor

    # retorna o dicionário de dados
    return ldct_data
'''
# -------------------------------------------------------------------------------------------------
def parse_subida(f_element):
    """
    helper function to the constructor, parses xml entries

    <subida nSub="1">
      <descricao>BGC 2A</descricao>
      <aerodromo>SBGR</aerodromo>
      <pista>09R</pista>
                           
      <breakpoint nBrk="1"> ... </breakpoint>
    </subida>

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle descricao (nome)
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle aeródromo
    elif "aerodromo" == f_element.tagName():
        ldct_tmp["aerodromo"] = f_element.text()

    # handle pista
    elif "pista" == f_element.tagName():
        ldct_tmp["pista"] = f_element.text()

    # handle breakpoint
    elif "breakpoint" == f_element.tagName():
        ldct_tmp["breakpoint"] = _parse_bkp(f_element)

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_trafego(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle indicativo
    if "indicativo" == f_element.tagName():
        ldct_tmp["indicativo"] = f_element.text()

    # handle designador
    elif "designador" == f_element.tagName():
        ldct_tmp["designador"] = f_element.text()

    # handle ssr
    elif "ssr" == f_element.tagName():
        ldct_tmp["ssr"] = f_element.text()

    # handle origem
    elif "origem" == f_element.tagName():
        ldct_tmp["origem"] = f_element.text()

    # handle destino
    elif "destino" == f_element.tagName():
        ldct_tmp["destino"] = f_element.text()

    # handle procedimen
    elif "procedimento" == f_element.tagName():
        ldct_tmp["procedimento"] = f_element.text()

    # handle nivel
    elif "nivel" == f_element.tagName():
        ldct_tmp["nivel"] = f_element.text()

    # handle altitude
    elif "altitude" == f_element.tagName():
        ldct_tmp["altitude"] = f_element.text()

    # handle velocidade
    elif "velocidade" == f_element.tagName():
        ldct_tmp["velocidade"] = f_element.text()

    # handle proa
    elif "proa" == f_element.tagName():
        ldct_tmp["proa"] = f_element.text()

    # handle temptrafego
    elif "temptrafego" == f_element.tagName():
        ldct_tmp["temptrafego"] = f_element.text()

    # handle numsg
    elif "numsg" == f_element.tagName():
        ldct_tmp["numsg"] = f_element.text()

    # handle tempmsg
    elif "tempmsg" == f_element.tagName():
        ldct_tmp["tempmsg"] = f_element.text()

    # handle rvsm
    elif "rvsm" == f_element.tagName():
        ldct_tmp["rvsm"] = f_element.text()

    # handle rota
    elif "rota" == f_element.tagName():
        ldct_tmp["rota"] = f_element.text()

    # handle eet
    elif "eet" == f_element.tagName():
        ldct_tmp["eet"] = f_element.text()

    # handle niveltrj
    elif "niveltrj" == f_element.tagName():
        ldct_tmp["niveltrj"] = f_element.text()

    # handle veltrj
    elif "veltrj" == f_element.tagName():
        ldct_tmp["veltrj"] = f_element.text()

    # handle posição
    elif "coord" == f_element.tagName():
        ldct_tmp["coord"] = _parse_crd(f_element)

    # retorna o dicionário de dados
    return ldct_tmp

# -------------------------------------------------------------------------------------------------
def parse_trajetoria(f_element):
    """
    helper function to the constructor, parses xml entries

    @param f_element: element to parse
    """
    # inicia o dicionário de dados
    ldct_tmp = {}

    # handle descrição
    if "descricao" == f_element.tagName():
        ldct_tmp["descricao"] = f_element.text()

    # handle proa
    elif "proa" == f_element.tagName():
        ldct_tmp["proa"] = f_element.text()

    # handle star
    elif "star" == f_element.tagName():
        ldct_tmp["star"] = f_element.text()

    # handle breakpoint
    elif "breakpoint" == f_element.tagName():
        ldct_tmp["breakpoint"] = _parse_bkp(f_element)

    # retorna o dicionário de dados
    return ldct_tmp

# < the end >--------------------------------------------------------------------------------------
