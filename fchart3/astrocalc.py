#    fchart3 draws beautiful deepsky charts in vector formats
#    Copyright (C) 2005-2024 fchart authors
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import math


def angular_distance(position1, position2):
    """
    Compute angular distance between start and end point.
    These points are tuples (ra,dec) in radians. Result is also in radians.
    """
    if position1[0] == position2[0] and position1[0] == position2[0]:
        return 0.0
    (ra1, dec1) = position1
    (ra2, dec2) = position2
    a = ra1-ra2
    arg = math.sin(dec1)*math.sin(dec2) + math.cos(dec1)*math.cos(dec2)*math.cos(a)
    return math.acos(arg)


def justify_angle(angle, lower_bound, upper_bound):
    """
    Justifies angle to interval lower_bound <= angle <
    upper_bound. The routine assumes periodic boundary conditions.

    Usage:
       justify_angle(371, 0, 360)      => 11
       justify_angle(-0.5*pi, 0, 2*pi) => 1.5*pi
    """

    step = upper_bound - lower_bound

    k = int((angle-lower_bound)/step)
    if angle < lower_bound:
        angle += (k+1)*step
    else:
        if angle >= upper_bound:
            angle -= k*step
    return angle


def rad2hms_t(angle):
    sign = 1
    if angle < 0:
        sign = -1
    p2 = 2.0*math.pi
    h = (sign*angle/p2)*24.0
    h_int = int(h + 1e-8)
    m = (h - h_int)*60.0
    m_int = int(m + 1e-8)
    s = (m - m_int)*60.0

    if s <= 1e-6:
        s = 0
        #if fabs(s*100 - int(s*100)) < 1e-4:
    s = int(100*s + 0.5)/100.0
    return h_int, m_int, s, sign


def rad2dms_t(angle):
    sign = 1
    if angle < 0:
        sign = -1
    p2 = 2.0*math.pi
    d = (sign*angle/p2)*360.0
    d_int = int(d + 1e-8)
    m = (d - d_int)*60.0
    m_int = int(m + 1e-8)
    s = (m - m_int)*60.0

    if s <= 1e-6:
        s = 0
    s = int(100*s + 0.5)/100.0
    return d_int, m_int, s, sign


def rad2hms(angle):
    """
    Converts an angle in radians to a string in a 24-hour, hour,
    minute, seconds format. 0 <= angle < 2math.pi.

    Usage:
        rad2hms(0.345) => '1h19m4.09054368322'
    """
    h_int, m_int, s, sign = rad2hms_t(angle)

    return str(sign*h_int) + 'h' + str(m_int) + 'm' + str(s)


def rad2dms(angle):
    """
    Converts an angle in radians to a string in a 360 degree, degree,
    minute, seconds format. 0 <= angle < 2math.pi.

    Usage:
        rad2dms(0.345) => '19d46m1.35815524824'
    """
    d_int, m_int, s, sign = rad2dms_t(angle)
    return str(sign*d_int)+'d'+str(m_int)+'m'+str(s)


def dms2rad(d, m=0, s=0, sign=1):
    """
    Converts an angle in degrees(d), minutes(m) and seconds(s) into
    radians. The parameters d, m and s MUST be positive. If a negative
    angle needs to be converted, then sign must be set to -1.
    """
    return sign*(d + m/60.0 + s/3600.0)*math.pi/180.0


def hms2rad(h, m=0, s=0, sign=1):
    """
    Converts an angle in hours(h), minutes(m) and seconds(s) into
    radians. If a negative angle needs to be converted, then sign must
    be set to -1.

    """
    return sign*(h + m/60.0 + s/3600.0)*math.pi/12.0


def lm_to_radec(lm, fieldcentre):
    """
    Inverse of SIN projection. Converts lm (l, m) with respect to
    a fieldcentre (alpha0, delta0) to equatorial coordinates (alpha,
    delta). All units are in radians. lm is a tuple:
    (l,m). Fieldcentre is a tuple (alpha0, delta0). The routine
    returns a tuple (alpha, delta). The formulae are taken from
    Greisen 1983: AIPS Memo 27, 'Non-linear Coordinate Systems in
    AIPS'
    """
    (l, m) = lm
    (alpha0, delta0) = fieldcentre
    alpha = alpha0 + math.atan2(l,(math.cos(delta0)*math.sqrt(1-l*l -m*m) - m*math.sin(delta0)))
    delta = math.asin((m*math.cos(delta0) + math.sin(delta0)*math.sqrt(1-l*l - m*m)))
    return alpha, delta


def radec_to_lm(radec, fieldcentre):
    """
    SIN projection. Converts radec (alpha, delta) with respect to
    a fieldcentre (alpha0, delta0) to direction cosines (l, m). All
    units are in radians. radec is a tuple (alpha, delta), Fieldcentre
    is a tuple (alpha0, delta0). The routine returns a tuple (l,m).
    The formulae are taken from Greisen 1983: AIPS Memo 27,
    'Non-linear Coordinate Systems in AIPS'
    """
    (ra, dec) = radec
    (ra0, dec0) = fieldcentre
    delta_ra = ra - ra0
    l = math.cos(dec)*math.sin(delta_ra)
    m = math.sin(dec)*math.cos(dec0) - math.cos(dec)*math.cos(delta_ra)*math.sin(dec0)
    return l, m


def radec_to_lmz(ra, dec, fieldcentre):
    """
    SIN projection. Converts radec (alpha, delta) with respect to
    a fieldcentre (alpha0, delta0) to direction cosines (l, m, z). All
    units are in radians. radec is a tuple (alpha, delta), Fieldcentre
    is a tuple (alpha0, delta0). The routine returns a tuple (l,m,z).
    The formulae are taken from Greisen 1983: AIPS Memo 27,
    'Non-linear Coordinate Systems in AIPS'
    """
    (ra0, dec0) = fieldcentre
    delta_ra = ra - ra0

    sin_dec = math.sin(dec)
    cos_dec = math.cos(dec)
    cos_dec0 = math.cos(dec0)
    sin_dec0 = math.sin(dec0)
    cos_delta_ra = math.cos(delta_ra)

    z = sin_dec*sin_dec0 + cos_dec*cos_dec0*cos_delta_ra
    l = cos_dec*math.sin(delta_ra) if z>0 else 0
    m = sin_dec*cos_dec0 - cos_dec*cos_delta_ra*sin_dec0 if z>0 else 0
    return l, m, z


def radec_to_xyz(ra, dec, fieldcentre, scale, fc_sincos_dec):
    """
    SIN projection. Converts radec (alpha, delta) with respect to
    a fieldcentre (alpha0, delta0) to coordinates (x, y, z). All
    units are in radians. radec is a tuple (alpha, delta), Fieldcentre
    is a tuple (alpha0, delta0). The routine returns a tuple (x,y,z).
    The formulae are taken from Greisen 1983: AIPS Memo 27,
    'Non-linear Coordinate Systems in AIPS'
    """
    (ra0, dec0) = fieldcentre
    delta_ra = ra - ra0

    sin_dec = math.sin(dec)
    cos_dec = math.cos(dec)
    cos_dec0 = fc_sincos_dec[1] # math.cos(dec0)
    sin_dec0 = fc_sincos_dec[0] # math.sin(dec0)
    cos_delta_ra = math.cos(delta_ra)

    z = sin_dec*sin_dec0 + cos_dec*cos_dec0*cos_delta_ra
    x = -cos_dec*math.sin(delta_ra)*scale if z>0 else 0
    y = (sin_dec*cos_dec0 - cos_dec*cos_delta_ra*sin_dec0)*scale if z>0 else 0
    return x, y, z


def radec_to_xy(ra, dec, fieldcentre, scale, fc_sincos_dec):
    """
    SIN projection. Converts radec (alpha, delta) with respect to
    a fieldcentre (alpha0, delta0) to coordinates (x, y, z). All
    units are in radians. radec is a tuple (alpha, delta), Fieldcentre
    is a tuple (alpha0, delta0). The routine returns a tuple (x,y,z).
    The formulae are taken from Greisen 1983: AIPS Memo 27,
    'Non-linear Coordinate Systems in AIPS'
    """
    (ra0, dec0) = fieldcentre
    delta_ra = ra - ra0

    sin_dec = math.sin(dec)
    cos_dec = math.cos(dec)
    cos_dec0 = fc_sincos_dec[1] # math.cos(dec0)
    sin_dec0 = fc_sincos_dec[0] # math.sin(dec0)
    cos_delta_ra = math.cos(delta_ra)

    x = -cos_dec*math.sin(delta_ra)*scale
    y = (sin_dec*cos_dec0 - cos_dec*cos_delta_ra*sin_dec0)*scale
    return x, y


def direction_ddec(radec, fieldcentre, fc_sincos_dec):
    """
    Gives the angle between true north and map north on any
    location in a SIN projection. Positive means that the true north
    is pointing east of the map north.

    ra, dec , ra0 and dec0 are in radians
    """

    (ra0, dec0) = fieldcentre
    (ra, dec) = radec

    cos_dec0 = fc_sincos_dec[1]  # math.cos(dec0)
    sin_dec0 = fc_sincos_dec[0]  # math.sin(dec0)

    angle = math.atan2(-math.sin(dec)*math.sin(ra-ra0), math.cos(dec)*cos_dec0 + math.sin(dec)*sin_dec0*math.cos(ra-ra0))
    return angle


def sphere_to_rect(ra, dec):
    """
    Convert from spherical coordinates to Rectangular direction.
    """
    cos_dec = math.cos(dec)
    return (math.cos(ra) * cos_dec, math.sin(ra) * cos_dec, math.sin(dec))


def rect_to_sphere(x1, x2, x3):
    """
    Convert from Rectangular direction to spherical coordinate components.
    """
    r = math.sqrt(x1*x1 + x2*x2 + x3*x3)
    ra = math.atan2(x2, x1)
    dec = math.asin(x3/r)
    return ra, dec


def pos_angle(ra1, dec1, ra2, dec2):
    """
    Calculate the position angle between two points.
    Returns:
    float: The position angle (in radians).
    """
    delta_ra = ra2 - ra1
    a = math.atan2(math.sin(delta_ra), math.cos(dec1) * math.tan(dec2) - math.sin(dec1) * math.cos(delta_ra))
    a += math.pi
    a = a % (2 * math.pi)
    return a


def radec_to_horizontal(lst, sincos_lat, ra, dec):
    """
    Convert Equatorial coordinates (ra, dec) to Horizontal coordinates (Alt, Az).
    :param lst: Local Sidereal Time in radians
    :param sincos_lat: precomputed array of sin+cos of observer's latitude
    :param ra: Right Ascension in radians
    :param dec: Declination in radians
    :return: (Alt, Az) in radians
    """

    hour_angle = (lst - ra) % (2 * math.pi)

    sin_lat = sincos_lat[0]
    cos_lat = sincos_lat[1]
    sin_dec = math.sin(dec)
    cos_dec = math.cos(dec)
    sin_ha = math.sin(hour_angle)
    cos_ha = math.cos(hour_angle)

    sin_alt = sin_dec * sin_lat + cos_dec * cos_lat * cos_ha
    alt = math.asin(sin_alt)

    cos_alt = math.sqrt(max(0.0, 1.0 - sin_alt*sin_alt))
    if abs(cos_alt) < 1e-15:
        cos_alt = math.cos(alt)

    arg = (sin_dec - sin_lat * sin_alt) / (cos_lat * cos_alt)

    if arg <= -1.0:
        az = math.pi
    elif arg >= 1.0:
        az = 0.0
    else:
        az = math.acos(arg)

    if sin_ha > 0.0 and abs(az) > 1e-15:
        az = 2.0 * math.pi - az

    az = (2 * math.pi - az) % (2 * math.pi)

    return alt, az


def horizontal_to_radec(lst, sincos_lat, alt, az):
    """
    Invert the transformation done by radec_to_horizontal(...).
    Given horizontal coordinates (alt, az) and local sidereal time (lst),
    recover equatorial coordinates (ra, dec).

    :param lst: Local Sidereal Time [radians]
    :param sincos_lat: (sin(latitude), cos(latitude))
    :param alt: altitude [radians]
    :param az:  azimuth [radians] as returned by radec_to_horizontal
    :return: (ra, dec) in radians
    """
    sin_lat, cos_lat = sincos_lat

    sin_alt = math.sin(alt)
    cos_alt = math.cos(alt)

    sin_dec = sin_lat * sin_alt + cos_lat * cos_alt * math.cos(az)

    if sin_dec > 1.0:
        sin_dec = 1.0
    elif sin_dec < -1.0:
        sin_dec = -1.0

    dec = math.asin(sin_dec)

    cos_dec = math.cos(dec)
    denom = cos_dec * cos_lat
    if abs(denom) < 1.0e-15:
        hour_angle = 0.0
    else:
        cos_ha = (sin_alt - sin_dec * sin_lat) / denom
        cos_ha = max(-1.0, min(1.0, cos_ha))

        sin_ha = math.sqrt(max(0.0, 1.0 - cos_ha*cos_ha))
        if az >= math.pi:
            sin_ha = -sin_ha

        hour_angle = math.atan2(sin_ha, cos_ha)

    ra = (lst - hour_angle) % (2.0 * math.pi)

    return ra, dec


__all__ = ['angular_distance', 'justify_angle', 'rad2hms_t','rad2dms_t',
           'rad2dms', 'rad2hms',
           'hms2rad', 'dms2rad', 'lm_to_radec', 'radec_to_lm', 'radec_to_lmz',
           'radec_to_xyz', 'radec_to_xy', 'direction_ddec',
           'sphere_to_rect', 'rect_to_sphere',
           'radec_to_horizontal'
           ]
