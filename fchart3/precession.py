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

from numpy import array, cos, sin

# Angles.
ASEC2RAD = 4.848136811095359935899141e-6
# Time.
T0 = 2451545.0


# from skyfield/precession.lib
def compute_precession_matrix(jd_tdb):
    """Return the rotation matrices for precessing to an array of epochs.
    `jd_tdb` - array of TDB Julian dates

    The array returned has the shape `(3, 3, n)` where `n` is the number
    of dates that have been provided as input.

    """
    eps0 = 84381.406

    # 't' is time in TDB centuries.

    t = (jd_tdb - T0) / 36525.0

    # Numerical coefficients of psi_a, omega_a, and chi_a, along with
    # epsilon_0, the obliquity at J2000.0, are 4-angle formulation from
    # Capitaine et al. (2003), eqs. (4), (37), & (39).

    psia   = ((((-    0.0000000951  * t
                 +    0.000132851 ) * t
                 -    0.00114045  ) * t
                 -    1.0790069   ) * t
                 + 5038.481507    ) * t

    omegaa = ((((+    0.0000003337  * t
                 -    0.000000467 ) * t
                 -    0.00772503  ) * t
                 +    0.0512623   ) * t
                 -    0.025754    ) * t + eps0

    chia   = ((((-    0.0000000560  * t
                 +    0.000170663 ) * t
                 -    0.00121197  ) * t
                 -    2.3814292   ) * t
                 +   10.556403    ) * t

    eps0 = eps0 * ASEC2RAD
    psia = psia * ASEC2RAD
    omegaa = omegaa * ASEC2RAD
    chia = chia * ASEC2RAD

    sa = sin(eps0)
    ca = cos(eps0)
    sb = sin(-psia)
    cb = cos(-psia)
    sc = sin(-omegaa)
    cc = cos(-omegaa)
    sd = sin(chia)
    cd = cos(chia)

    # Compute elements of precession rotation matrix equivalent to
    # R3(chi_a) R1(-omega_a) R3(-psi_a) R1(epsilon_0).

    rot3 = array(((cd * cb - sb * sd * cc,
                   cd * sb * ca + sd * cc * cb * ca - sa * sd * sc,
                   cd * sb * sa + sd * cc * cb * sa + ca * sd * sc),
                  (-sd * cb - sb * cd * cc,
                   -sd * sb * ca + cd * cc * cb * ca - sa * cd * sc,
                   -sd * sb * sa + cd * cc * cb * sa + ca * cd * sc),
                  (sb * sc,
                   -sc * cb * ca - sa * cc,
                   -sc * cb * sa + cc * ca)))
    return rot3
