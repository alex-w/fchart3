#    fchart3 draws beautiful deepsky charts in vector formats
#    Copyright (C) 2005-2023 fchart authors
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

from enum import Enum

class Planet(Enum):
    MERCURY = (1, "Mercury")
    VENUS   = (2, "Venus")
    EARTH   = (3, "Earth")
    MARS    = (4, "Mars")
    JUPITER = (5, "Jupiter")
    SATURN  = (6, "Saturn")
    URANUS  = (7, "Uranus")
    NEPTUNE = (8, "Neptune")
    PLUTO   = (9, "Pluto")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

class PlanetObject:
    def __init__(self, planet, ra, dec):
        self.planet = planet
        self.ra = ra
        self.dec = dec
