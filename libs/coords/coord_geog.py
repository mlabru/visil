#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
coord_geog

manage geographical points, perform conversions, etc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

revision 0.2  2015/nov  mlabru
pep8 style conventions

revision 0.1  2014/nov  mlabru
initial version (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.2$"
__author__ = "Milton Abrunhosa"
__date__ = "2016/01"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import math

import coord_conv as conv
import coord_defs as cdefs

# -------------------------------------------------------------------------------------------------
def __calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo do ângulo entre a referência e o ponto

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return ângulo entre a referência e o ponto
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica coincidência de pontos
    if (ff_lat_pto == ff_lat_ref) and (ff_lng_pto == ff_lng_ref):
        # pontos coincidentes
        return 0.

    # obtém as coordenadas do ponto de referência em radianos
    lf_lat_ref = math.radians(ff_lat_ref)
    lf_lng_ref = math.radians(ff_lng_ref)

    lf_ir = math.cos(lf_lat_ref) * math.cos(lf_lng_ref)
    lf_jr = math.cos(lf_lat_ref) * math.sin(lf_lng_ref)
    lf_kr = math.sin(lf_lat_ref)

    # obtém as coordenadas do ponto em radianos
    lf_lat_pto = math.radians(ff_lat_pto)
    lf_lng_pto = math.radians(ff_lng_pto)

    lf_ip = math.cos(lf_lat_pto) * math.cos(lf_lng_pto)
    lf_jp = math.cos(lf_lat_pto) * math.sin(lf_lng_pto)
    lf_kp = math.sin(lf_lat_pto)

    # distância entre a referência e o ponto
    return (lf_ir * lf_ip) + (lf_jr * lf_jp) + (lf_kr * lf_kp)

# -------------------------------------------------------------------------------------------------
def decl_xyz_0(ff_x, ff_y, ff_z, ff_decl_mag):
    """
    @param ff_x: DOCUMENT ME!
    @param ff_y: DOCUMENT ME!
    @param ff_z: DOCUMENT ME!
    @param ff_decl_mag: DOCUMENT ME!
    """
    #l_log = logging.getLogger("CCoordSys::decl_xyz")
    #l_log.setLevel(logging.DEBUG)
    #l_log.debug("x, y, z / decl (A): {} {} {} {}".format(ff_x, ff_y, ff_z, ff_decl_mag))
                                    
    # quadrante
    li_quad = 0

    # declinação magnética
    lf_dec_mag = 0.

    # ângulo e distância
    lf_ang = 0.
    lf_dst = 0.

    # condições marginais
    if (ff_x != 0.) or (ff_y != 0.):
        # x = 0. ?
        if 0. == ff_x:
            if ff_y > 0.:
                # determinação da distancia & ângulo trigonométrico
                lf_dst = ff_y
                lf_ang = cdefs.D_RAD_PI_2

            else:
                # determinação da distancia & ângulo trigonométrico
                lf_dst = abs(ff_y)
                lf_ang = cdefs.D_RAD_3PI_2

        # y = 0. ?
        elif ff_y == 0.:
            if ff_x > 0.:
                # determinação da distancia & ângulo trigonométrico
                lf_dst = ff_x
                lf_ang = 0.

            else:
                # determinação da distancia & ângulo trigonométrico
                lf_dst = abs(ff_x)
                lf_ang = math.pi

        # senão,...
        else:
            # determinação do quadrante
            if ff_x > 0.:
                if ff_y > 0.:
                    li_quad = 1

                else:
                    li_quad = 4

            elif ff_y > 0.:
                li_quad = 2

            else:
                li_quad = 3

            # determinação da distancia & ângulo trigonométrico
            lf_dst = math.sqrt((ff_x ** 2) + (ff_y ** 2))
            lf_ang = math.atan(abs(ff_y) / abs(ff_x))

        # correção do ângulo trigonométrico devido ao quadrante
        if 2 == li_quad:
            lf_ang = math.pi - lf_ang

        elif 3 == li_quad:
            lf_ang += math.pi

        elif 4 == li_quad:
            lf_ang = cdefs.D_RAD_2PI - lf_ang

        # converte o ângulo trigonométrico em radial
        if lf_ang <= cdefs.D_RAD_PI_2:
            lf_ang = cdefs.D_RAD_PI_2 - lf_ang

        else:
            lf_ang =(cdefs.D_RAD_PI_2 * 5) - lf_ang

        # converte a declinação magnética para radianos
        lf_dec_mag = math.radians(ff_decl_mag)

        # corrige a radial devido a declinação magnética
        if ff_decl_mag < 0.:
            lf_ang += lf_dec_mag

        elif ff_decl_mag > 0.:
            lf_ang -= lf_dec_mag

        # converte a radial em ângulo trigonométrico
        if lf_ang <= cdefs.D_RAD_PI_2:
            lf_ang = cdefs.D_RAD_PI_2 - lf_ang

        else:
            lf_ang =(cdefs.D_RAD_PI_2 * 5) - lf_ang

        # calcula as novas coordenadas X e Y
        ff_x = lf_dst * math.cos(lf_ang)
        ff_y = lf_dst * math.sin(lf_ang)

    #l_log.debug("x, y, z (D): {} {} {}".format(ff_x, ff_y, ff_z))

    # return
    return ff_x, ff_y, ff_z

# -------------------------------------------------------------------------------------------------
def decl_xyz(ff_x, ff_y, ff_z, ff_dcl_mag=cdefs.M_DCL_MAG):
    """
    negativo (O/W), gira no sentido horário

    @param ff_x: DOCUMENT ME!
    @param ff_y: DOCUMENT ME!
    @param ff_z: DOCUMENT ME!
    @param ff_decl_mag: DOCUMENT ME!

    @return ponto declinado
    """
    # declinação em radianos
    lf_dcl_r = math.radians(abs(ff_dcl_mag))

    # sin e cos da declinação
    lf_dcl_sin = math.sin(lf_dcl_r)
    lf_dcl_cos = math.cos(lf_dcl_r)

    # declinação a leste ?
    if ff_dcl_mag > 0.:
        # ajuste da coordenada com a declinação magnética
        ff_x = (ff_x * lf_dcl_cos) - (ff_y * lf_dcl_sin)
        ff_y = (ff_y * lf_dcl_cos) + (ff_x * lf_dcl_sin)

    # senão, declinação a oeste
    else:
        # ajuste da coordenada com a declinação magnética
        ff_x = (ff_x * lf_dcl_cos) + (ff_y * lf_dcl_sin)
        ff_y = (ff_y * lf_dcl_cos) - (ff_x * lf_dcl_sin)

    # return
    return ff_x, ff_y, ff_z

# -------------------------------------------------------------------------------------------------
def geo_azim(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo do azimute entre duas coordenadas geográficas

             azimute          cartesiano
               000               090
            270   090         180   000
               180               270

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return azimute entre a referência e o ponto em radianos
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # condições especiais de retorno
    if (ff_lat_ref == ff_lat_pto) and (ff_lng_ref == ff_lng_pto):
        # pontos coincidentes
        return 0.

    if (ff_lat_ref == ff_lat_pto) and (ff_lng_ref > ff_lng_pto):
        # mesma linha à esquerda
        return math.radians(270.)

    if (ff_lat_ref == ff_lat_pto) and (ff_lng_ref < ff_lng_pto):
        # mesma linha à direita
        return math.radians(90.)

    if (ff_lat_ref > ff_lat_pto) and (ff_lng_ref == ff_lng_pto):
        # mesma coluna abaixo
        return math.pi

    if (ff_lat_ref < ff_lat_pto) and (ff_lng_ref == ff_lng_pto):
        # mesma coluna acima
        return 0.

    # calcula o ângulo (rad)
    lf_gama = __calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)

    if 1 == int(lf_gama):
        lf_arc_gama = 0.

    else:
        lf_arc_gama = math.acos(lf_gama)

    # cálculo do ângulo (rad) entre X e o ponto
    lf_delta = __calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_pto, ff_lng_ref)

    if 1 == int(lf_delta):
        lf_arc_delta = 0.

    else:
        lf_arc_delta = math.acos(lf_delta)

    # cálculo do azimute básico
    lf_aux = math.sin(lf_arc_delta) / math.sin(lf_arc_gama)

    if lf_aux > 1.:
        lf_aux = 1.

    elif lf_aux < -1.:
        lf_aux = -1.

    lf_azim = math.asin(lf_aux)

    li_quad = 0

    # cálculo do azimute corrigido
    if (ff_lat_ref < ff_lat_pto) and (ff_lng_ref < ff_lng_pto): li_quad = 1
    if (ff_lat_ref < ff_lat_pto) and (ff_lng_ref > ff_lng_pto): li_quad = 4
    if (ff_lat_ref > ff_lat_pto) and (ff_lng_ref > ff_lng_pto): li_quad = 3
    if (ff_lat_ref > ff_lat_pto) and (ff_lng_ref < ff_lng_pto): li_quad = 2

    if (2 == li_quad): lf_azim = math.pi - lf_azim
    if (3 == li_quad): lf_azim = math.pi + lf_azim
    if (4 == li_quad): lf_azim = (2 * math.pi) - lf_azim

    # return
    return lf_azim

# -------------------------------------------------------------------------------------------------
def geo_azim_bug(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo do azimute entre dois pontos geográficos
    (válido par distâncias menores que 800NM)

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return azimute entre a referência e o ponto em NM
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica coincidência de pontos
    if (ff_lat_pto == ff_lat_ref) and (ff_lng_pto == ff_lng_ref):
        # pontos coincidentes
        return 0.

    # calcula a distância em latitude (DLA)
    lf_lat_dst = ff_lat_pto - ff_lat_ref

    # calcula a distância em longitude (DLO)
    lf_lng_dst = ff_lng_pto - ff_lng_ref

    # retorna o azimute entre os pontos
    return conv.azm2ang(math.atan2(lf_lat_dst, lf_lng_dst))

# -------------------------------------------------------------------------------------------------
def geo_dist(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo da distância entre dois pontos geográficos

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return distância entre a referência e o ponto em NM
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica coincidência de pontos
    if (ff_lat_pto == ff_lat_ref) and (ff_lng_pto == ff_lng_ref):
        # pontos coincidentes
        return 0.

    # calcula o ângulo
    lf_gama = __calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)

    # retorna o cálculo da distância entre a referência e o ponto
    return math.acos(lf_gama) * cdefs.D_EARTH_RADIUS_NM

# -------------------------------------------------------------------------------------------------
def geo_dist_2(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    cálculo da distância entre dois pontos geográficos
    (válido par distâncias menores que 800NM)

    @param ff_lat_pto: latitude do ponto em graus
    @param ff_lng_pto: longitude do ponto em graus
    @param ff_lat_ref: latitude da referência em graus
    @param ff_lng_ref: longitude da referência em graus

    @return distância entre a referência e o ponto em NM
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica coincidência de pontos
    if (ff_lat_pto == ff_lat_ref) and (ff_lng_pto == ff_lng_ref):
        # pontos coincidentes
        return 0.

    # calcula a distância em latitude
    lf_lat_dst = (ff_lat_pto - ff_lat_ref) ** 2

    # calcula a distância em longitude
    lf_lng_dst = (ff_lng_pto - ff_lng_ref) ** 2

    # retorna a distância entre a referência e o ponto
    return math.sqrt(lf_lat_dst + lf_lng_dst) * cdefs.D_CNV_G2NM

# -------------------------------------------------------------------------------------------------
def geo2pol(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    transforma coordenadas geográficas em coordenadas polares

    @param ff_lat_pto: latitude em graus
    @param ff_lng_pto: longitude em graus
    @param ff_lat_ref: latitude do ponto de referência
    @param ff_lng_ref: longitude do ponto de referência

    @return coordenadas polares do ponto (azimute em graus, distância em NM)
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # verifica se os pontos são coincidentes
    if (ff_lat_ref == ff_lat_pto) and (ff_lng_ref == ff_lng_pto):
        # ok, pontos coincidentes
        return 0., 0.

    # calcula o ângulo
    lf_gama = math.acos(__calc_gama(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref))

    # calcula a distância
    lf_dist = lf_gama * cdefs.D_EARTH_RADIUS_NM

    # calcula o ângulo
    lf_delta = math.acos(__calc_gama(ff_lat_pto, ff_lng_ref, ff_lat_pto, ff_lng_pto))

    # verificação do quadrante
    li_quad = -1

    if (ff_lat_ref < ff_lat_pto) and (ff_lng_ref == ff_lng_pto):
        lf_azim = 0.

    elif (ff_lat_ref == ff_lat_pto) and (ff_lng_ref < ff_lng_pto):
        lf_azim = 90.

    elif (ff_lat_ref > ff_lat_pto) and (ff_lng_ref == ff_lng_pto):
        lf_azim = 180.

    elif (ff_lat_ref == ff_lat_pto) and (ff_lng_ref > ff_lng_pto):
        lf_azim = 270.

    elif (ff_lat_ref < ff_lat_pto) and (ff_lng_ref < ff_lng_pto):
        li_quad = 1

    elif (ff_lat_ref > ff_lat_pto) and (ff_lng_ref < ff_lng_pto):
        li_quad = 2

    elif (ff_lat_ref > ff_lat_pto) and (ff_lng_ref > ff_lng_pto):
        li_quad = 3

    elif (ff_lat_ref < ff_lat_pto) and (ff_lng_ref > ff_lng_pto):
        li_quad = 4

    if -1 != li_quad:

        # seno do azimute
        lf_sin_azm = math.sin(lf_delta) / math.sin(lf_gama)

        # calculo do azimute
        if lf_sin_azm > 1.:
            lf_sin_azm = 1.

        elif lf_sin_azm < -1.:
            lf_sin_azm = -1.

        lf_azim = math.degrees(math.asin(lf_sin_azm))

        if 2 == li_quad:
            lf_azim = 180. - lf_azim

        elif 3 == li_quad:
            lf_azim = 180. + lf_azim

        elif 4 == li_quad:
            lf_azim = 360. - lf_azim

    if lf_azim >= 360.:
        lf_azim -= 360.

    elif lf_azim < 0:
        lf_azim += 360.

    # return
    return lf_azim, lf_dist

# -------------------------------------------------------------------------------------------------
def geo2xy(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    transforma coordenadas geográficas em coordenadas cartesianas

    @param ff_lat_pto: latitude em graus
    @param ff_lng_pto: longitude em graus
    @param ff_lat_ref: latitude do ponto de referência
    @param ff_lng_ref: longitude do ponto de referência

    @return coordenadas polares do ponto (azimute, distância em NM)
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # converte de geográfica para polar
    lf_azim, lf_dist = geo2pol(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)

    # converte de polar para cartesiana
    lf_x = lf_dist * math.sin(math.radians(lf_azim))
    lf_y = lf_dist * math.cos(math.radians(lf_azim))

    # correção das coordenadas X e Y devido ao efeito da declinação magnetica
    # lf_x, lf_y = decl_xyz(lf_x, lf_y, lf_z, f_ref.f_dcl_mag)

    # return
    return lf_x, lf_y

# -------------------------------------------------------------------------------------------------
def geo2xy_2(ff_lat_pto, ff_lng_pto, ff_lat_ref=cdefs.M_REF_LAT, ff_lng_ref=cdefs.M_REF_LNG):
    """
    conversão de coordenadas geográficas

    @param ff_lat_pto: latitude em graus
    @param ff_lng_pto: longitude em graus
    @param ff_lat_ref: coordenadas geográficas de referênica
    @param ff_lng_ref: coordenadas geográficas de referênica

    @return coordenadas X e Y do ponto
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    assert  -90. <= ff_lat_ref <= 90.
    assert -180. <= ff_lng_ref <= 180.

    # cálculo da distância e do azimute geográficos do ponto
    l_vd = geo_dist(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)
    l_vr = geo_azim(ff_lat_pto, ff_lng_pto, ff_lat_ref, ff_lng_ref)

    # converte o azimute para ângulo em radianos
    l_vr = math.radians(conv.azm2ang(math.degrees(l_vr)))

    # cálculo das coordenadas X & Y do ponto
    lf_x = l_vd * math.cos(l_vr)
    lf_y = l_vd * math.sin(l_vr)

    # existe declinação magnética ?
    # if 0. != f_ref.f_dcl_mag:
        # correção das coordenadas X e Y devido ao efeito da declinação magnética
        #decl_xy(f_ref.f_dcl_mag)

    # return x & y
    return lf_x, lf_y

# -------------------------------------------------------------------------------------------------
def geo2xyz_3(ff_lat_pto, ff_lng_pto, ff_alt=0.):
    """
    geodetic coordinates(latitude, longitude, height) can be converted into XY
    """
    # check input
    assert  -90. <= ff_lat_pto <= 90.
    assert -180. <= ff_lng_pto <= 180.

    # calcula x
    lf_x = (ff_lng_pto - float(cdefs.M_REF_LNG)) * cdefs.D_CNV_GR2M

    # calcula y
    lf_y = (ff_lat_pto - float(cdefs.M_REF_LAT)) * cdefs.D_CNV_GR2M

    # elevação
    lf_z = ff_alt

    # retorna as coordenadas xyz
    return lf_x, lf_y, lf_z

# -------------------------------------------------------------------------------------------------
def pol2xyz(ff_azim, ff_dist):
    """
    transforma coordenadas polares em coordenadas cartesianas

    @param ff_azim: azimute
    @param ff_dist: distância

    @return coordenadas cartesianas do ponto
    """
    # check input
    assert 0. <= ff_azim <= 360.

    # converte a distância para metros
    lf_dst = ff_dist

    # converte a radial para ângulo trigonométrico
    lf_azim = math.radians(conv.azm2ang(math.degrees(ff_azim)))

    # converte a distância e ângulo em X e Y
    lf_x = lf_dst * math.cos(lf_azim)
    lf_y = lf_dst * math.sin(lf_azim)

    # return
    return lf_x, lf_y, 0.

# -------------------------------------------------------------------------------------------------
def xyz2geo_3(ff_x, ff_y, ff_z=0.):
    """
    conversão de coordenadas geográficas
    geodetic coordinates (latitude, longitude, height) can be converted into xyz.

    @param ff_x: coordenada x do ponto
    @param ff_y: coordenada y do ponto
    @param ff_z: coordenada z do ponto
    """
    # calcula latitude
    lf_lat = float(cdefs.M_REF_LAT) + (ff_y / cdefs.D_CNV_GR2M)

    # calcula longitude
    lf_lng = float(cdefs.M_REF_LNG) + (ff_x / cdefs.D_CNV_GR2M)

    # calcula altitude
    lf_alt = ff_z

    # retorna as coordenadas lat/long
    return lf_lat, lf_lng, lf_alt

# < the end >--------------------------------------------------------------------------------------
