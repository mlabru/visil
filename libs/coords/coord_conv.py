# -*- coding: utf-8 -*-
"""
coord_conv
manage geographical points, perform conversions, etc

revision 2.0  2020/  mlabru
converted to python 3

revision 1.1  2015/nov  mlabru
pep8 style conventions

revision 1.0  2014/nov  mlabru
initial version (Linux/Python)
"""
# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import math
import re

# < module data >----------------------------------------------------------------------------------

# logging level
M_LOG = logging.getLogger(__name__)
M_LOG.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------
def azm2ang(ff_azim):
    """
    conversão de um azimute em ângulo cartesiano e vice-versa

             azimute          cartesiano
               000               090
            270   090   <=>   180   000
               180               270

    @param ff_azim: azimute ou ângulo em graus

    @return ângulo cartesiano ou azimute em graus
    """
    # logger
    # M_LOG.info(">> azm2ang")

    # normaliza o sistema de referência entre azimute e ângulo
    return (90. - ff_azim) if ff_azim <= 90. else (450. - ff_azim)

# -------------------------------------------------------------------------------------------------
def deg2dms(ff_deg):
    """
    conversão de graus para o formato ggg° mm' ss.sss"

    @param ff_deg: graus

    @return: ggg° mm' ss.sss"
    """
    # logger
    # M_LOG.info(">> deg2dms")

    # valor absoluto
    lf_deg = abs(ff_deg)

    # calcula os graus
    li_deg = int(lf_deg)

    # calcula os minutos
    lf_min = lf_deg - li_deg
    li_min = int(lf_min * 60.)

    # calcula os segundos
    lf_sec = ((lf_min * 60.) - li_min) * 60

    # converte em segundos
    # li_all = int ((lf_deg - li_deg) * 3600.0)
    # calcula os minutos
    # li_min = int(li_all / 60)
    # calcula os segundos
    # lf_sec = li_all % 60

    # retorna a string
    return int(ff_deg), int(li_min), lf_sec

# -------------------------------------------------------------------------------------------------
def deg2str(ff_deg):
    """
    converte de
    """
    # logger
    # M_LOG.info(">> deg2str")

    # retorna a string
    return u"%3d° %02d' %05.3f\"" % (deg2dms(ff_deg))

# -------------------------------------------------------------------------------------------------
def dms2deg(fi_deg, fi_min, ff_sec):
    """
    converte de ggg° mm' ss.sss para decimal
    """
    # logger
    # M_LOG.info(">> dms2deg")

    # converte para graus
    lf_deg = abs(fi_deg) + (fi_min / 60.) + (ff_sec / 3600.)

    # retorna o valor em graus
    return lf_deg if fi_deg >= 0 else -lf_deg

# -------------------------------------------------------------------------------------------------
def dms2str(fi_deg, fi_min, ff_sec):
    """
    converte de
    """
    # logger
    # M_LOG.info(">> dms2str")

    # retorna a string
    return u"%3d° %02d' %05.3f\"" % (fi_deg, fi_min, ff_sec)

# -------------------------------------------------------------------------------------------------
def format_ica_lat(ff_lat):
    """
    conversão de uma latitude em graus para o formato GGMM.mmmH

    @param ff_lat: latitude em graus

    @return string no formato GGMM.mmmH
    """
    # logger
    # M_LOG.info(">> format_ica_lat")

    # converte os graus para D/M/S
    lf_deg, lf_min, lf_seg = deg2dms(ff_lat)

    # converte para GGMM.mmm
    lf_deg = (abs(lf_deg) * 100) + lf_min + (lf_seg / 60.)

    # return latitude
    # return "{}{:4.3f}".format('S' if ff_lat <= 0 else 'N', lf_deg)
    return "{:4.3f}{}".format(lf_deg, 'S' if ff_lat <= 0 else 'N')

# -------------------------------------------------------------------------------------------------
def format_ica_lng(ff_lng):
    """
    conversão de uma longitude em graus para o formato GGGMM.mmmH

    @param ff_lng: longitude em graus

    @return string no formato GGGMM.mmmH
    """
    # logger
    # M_LOG.info(">> format_ica_lng")

    # converte os graus para D/M/S
    lf_deg, lf_min, lf_seg = deg2dms(ff_lng)

    # converte para GGGMM.mmm
    lf_deg = (abs(lf_deg) * 100) +  lf_min + (lf_seg / 60.)

    # return longitude
    # return "{}{:5.3f}".format('W' if ff_lng <= 0 else 'E', lf_deg)
    return "{:5.3f}{}".format(lf_deg, 'W' if ff_lng <= 0 else 'E')

# -------------------------------------------------------------------------------------------------
def gms2deg(ff_dms):
    """
    converte de gggmmss.ss para decimal

    @param ff_dms: ponto no formato gggmmss.ss

    @return coordenada em graus
    """
    # logger
    # M_LOG.info(">> gms2deg")

    # valor absoluto
    lf_dms = abs(ff_dms)

    # obtém os segundos
    ls_ec = lf_dms % 100

    # segundos inválidos ?
    if ls_ec > 59.99:
        # logger
        l_log = logging.getLogger("coord_conv::gms2deg")
        l_log.setLevel(logging.NOTSET)
        l_log.warning("segundos (%2.2f) maior que 59.99." % ls_ec)

    # senão, segundos válidos
    else:
        # obtém os minutos
        l_min = ((lf_dms - ls_ec) / 100.) % 100

        # minutos inválidos ?
        if l_min > 59.:
            # logger
            l_log = logging.getLogger("coord_conv::gms2deg")
            l_log.setLevel(logging.NOTSET)
            l_log.warning("minutos (%2.2f) maior que 59." % l_min)

        # senão, minutos válidos
        else:
            # obtém os graus
            lf_dms = int(lf_dms / 10000.)

            # calcula os graus
            lf_dms += (l_min / 60.) + (ls_ec / 3600.)

    # retorna o valor convertido
    return lf_dms

# -------------------------------------------------------------------------------------------------
def lat2deg(ff_lat_rad):
    """
    converts the latitude from radian to decimal

    @return the latitude in decimal
    """
    # logger
    # M_LOG.info(">> lat2deg")

    # calcula
    lf_lat = math.degrees(ff_lat_rad)

    # normaliza
    if lf_lat > 90.:
        lf_lat = 90

    elif lf_lat < -90.:
        lf_lat = -90

    # return the latitude in decimal
    return lf_lat

# -------------------------------------------------------------------------------------------------
def lat2dms(ff_lat):
    """
    conversão de latitude em graus para o formato ggg° mm' ss.ss" N/S

    @param ff_lat: latitude em graus

    @return ggg° mm' ss.sss" N/S
    """
    # logger
    # M_LOG.info(">> lat2dms")

    # normaliza
    if ff_lat > 90.:
        ff_lat = 90

    elif ff_lat < -90.:
        ff_lat = -90

    # retorna a tupla
    return deg2dms(abs(ff_lat)), 'S' if ff_lat < 0 else 'N'

# -------------------------------------------------------------------------------------------------
def lng2deg(ff_lng_rad):
    """
    converts the longitude from radian to decimal

    @return the longitude in decimal
    """
    # logger
    # M_LOG.info(">> lng2deg")

    # converte para graus
    lf_lng = math.degrees(ff_lng_rad)

    # normaliza
    if lf_lng > 180.:
        lf_lng = 180

    elif lf_lng < -180.:
        lf_lng = -180

    # return the longitude in decimal
    return lf_lng

# -------------------------------------------------------------------------------------------------
def lng2dms(ff_lng):
    """
    conversão de longitude em graus para o formato ggg° mm' ss.ss" E/W

    @param ff_lng: graus

    @return ggg° mm' ss.sss" E/W
    """
    # logger
    # M_LOG.info(">> lng2dms")

    # normaliza
    if ff_lng > 180.:
        ff_lng = 180

    elif ff_lng < -180.:
        ff_lng = -180

    # retorna a tupla
    return deg2dms(abs(ff_lng)), 'W' if ff_lng < 0 else 'E'

# -------------------------------------------------------------------------------------------------
def parse_adc(fs_in):
    """
    conversão de uma latitude/longitude(no formato XGGG MM SS) para coordenada geográfica

    @param fs_in: string no formato XGGG MM SS

    @return objeto latitude/longitude
    """
    # logger
    # M_LOG.info(">> parse_adc")

    # coordinates field decoding
    l_coord = fs_in.split()

    # hemisfério sul/oeste ?
    if l_coord[0][0].upper() in ['O', 'S', 'W']:
        li_sgn = -1

    # hemisfério norte/leste ?
    elif l_coord[0][0].upper() in ['E', 'N']:        
        li_sgn = 1

    # otherwise,...
    else:
        # return error
        return None

    # init coord
    lf_crd = None

    # converte graus
    li_deg = int(l_coord[0][1:])

    # graus válidos ?
    if -180 <= li_deg <= 180:
        # converte minutos
        li_min = int(l_coord[1])

        # minutos válidos ?
        if 0 <= li_min <= 59:
            # converte segundos
            li_sec = int(l_coord[2])

            # segundos válidos ?
            if li_sec >= 0:
                # cria uma coordenada
                lf_crd = dms2deg(li_deg, li_min, li_sec) * li_sgn

    # return longitude or latitude
    return lf_crd

# -------------------------------------------------------------------------------------------------
def parse_aisweb(fs_in):
    """
    conversão de uma latitude/longitude(no formato X:GGG:MM:SS.ss) para coordenada geográfica

    @param fs_in: string no formato X:GGG:MM:SS.ss

    @return objeto latitude/longitude
    """
    # logger
    # M_LOG.info(">> parse_aisweb")

    # coordinates field decoding
    l_coord = fs_in.split(':')

    # hemisfério sul/oeste ?
    if l_coord[0].upper() in ['O', 'S', 'W']:
        li_sgn = -1

    # hemisfério norte/leste ?
    elif l_coord[0].upper() in ['E', 'N']:        
        li_sgn = 1

    # otherwise,...
    else:
        # return error
        return -1.

    # init coord
    lf_crd = -1.

    # converte graus
    li_deg = int(l_coord[1])

    # graus válidos ?
    if -180 <= li_deg <= 180:
        # converte minutos
        li_min = int(l_coord[2])

        # minutos válidos ?
        if 0 <= li_min <= 59:
            # converte segundos
            lf_sec = float(l_coord[3])

            # segundos válidos ?
            if lf_sec >= 0.:
                # cria uma coordenada
                lf_crd = dms2deg(li_deg, li_min, lf_sec) * li_sgn

    # return longitude or latitude
    return lf_crd

# -------------------------------------------------------------------------------------------------
def parse_faa(fs_in):
    """
    @param fs_in: coordenada no formato Hgggmmss.ss

    @return coordenada em graus
    """
    # logger
    # M_LOG.info(">> parse_faa")

    # converte a entrada para maiúscula
    fs_in = fs_in.upper()

    # inicia a saída
    lf_crd = None

    # hemisfério inválido ?
    if not fs_in[0] in ['E', 'L', 'N', 'O', 'S', 'W']:
        # logger
        l_log = logging.getLogger("CCoordTRK::parse_faa")
        l_log.setLevel(logging.NOTSET)
        l_log.warning(u"hemisfério(%s) inválido." % fs_in[0])

    # senão, hemisfério ok
    else:
        # converte para graus
        lf_crd = dms2deg(float(fs_in[1:]))

        # graus inválidos ?
        if (((fs_in[0] in ['E', 'L', 'O', 'W']) and (lf_crd > 180.)) or
            ((fs_in[0] in ['N', 'S']) and (lf_crd > 90.))):
            # logger
            l_log = logging.getLogger("coord_conv::parse_faa")
            l_log.setLevel(logging.NOTSET)
            l_log.warning(u"graus fora do intervalo válido.")

        # senão, graus ok. hemisfério sul ou oeste ?
        elif fs_in[0] in ['O', 'S', 'W']:
            # converte para negativo
            lf_crd = -lf_crd

    # retorna a coordenada em graus
    return lf_crd

# -------------------------------------------------------------------------------------------------
def parse_ica(fs_in):
    """
    conversão de uma latitude/longitude(no formato GGGMM.mmmH/GGMM.mmmH) para coordenada

    @param fs_in: string no formato GGGMM.mmmH(lng) ou GGMM.mmmH(lat)

    @return objeto latitude/longitude
    """
    # logger
    # M_LOG.info(">> parse_ica")

    # converte a entrada para maiúscula
    fs_in = fs_in.upper()

    # coordinates field decoding
    l_coord = re.split(r"([E|L|N|O|S|W])", fs_in)

    # converte a coordenada
    lf_deg = float(l_coord[0])

    # gms decoding
    li_deg = int(lf_deg / 100.)
    lf_min = lf_deg % 100
    lf_sec = (lf_min - int(lf_min)) * 60

    # cria uma coordenada
    lf_crd = dms2deg(li_deg, int(lf_min), lf_sec) * -1 if l_coord[1] in ['O', 'S', 'W'] else 1

    # return longitude or latitude
    return lf_crd

# -------------------------------------------------------------------------------------------------
def parse_ica_2(fs_in):
    """
    conversão de uma latitude/longitude(no formato GGGMM.mmmH/GGMM.mmmH) para coordenada

    @param fs_in: string no formato GGGMM.mmmH(lng) ou GGMM.mmmH(lat)

    @return objeto latitude/longitude
    """
    # logger
    # M_LOG.info(">> parse_ica_2")

    # converte a entrada para maiúscula
    fs_in = fs_in.upper()

    # coordinates field decoding
    l_coord = re.split(r"([E|L|N|O|S|W])", fs_in)

    # deslocamento da lat/lng
    xxGRD = 2 if(l_coord[1] in ['N', 'S']) else 3

    # gms decoding
    li_deg = int(l_coord[0][:xxGRD])
    lf_min = float(l_coord[0][xxGRD:])
    lf_sec = (lf_min - int(lf_min)) * 60

    # cria uma coordenada
    lf_crd = dms2deg(li_deg, int(lf_min), lf_sec) * -1 if l_coord[1] in ['O', 'S', 'W'] else 1

    # return longitude or latitude
    return lf_crd

# -------------------------------------------------------------------------------------------------
def round_32(f_val):
    """
    converts a value in 32th of nautical miles

    @return nautical miles in 1/32
    """
    # logger
    # M_LOG.info(">> round_32")

    # return
    return long(round(f_val * 32.))

# -------------------------------------------------------------------------------------------------
def round_from_32(f_val):
    """
    converts a 32th of nautical miles into a distance

    @return distance in nautical miles
    """
    # logger
    # M_LOG.info(">> round_from_32")

    # return
    return f_val / 32.

# < the end >--------------------------------------------------------------------------------------
