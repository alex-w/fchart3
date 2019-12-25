#    fchart draws beautiful deepsky charts in vector formats
#    Copyright (C) 2005-202 fchart authors0
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
from numpy import *
import os
import sys
from fchart.astrocalc import *

class IndexRecord:
    def __init__(self, first_record, num_records, ra_min, dec_min, ra_max, dec_max):
        """
        Angles are in radians
        """
        self.centre       = ((ra_max+ra_min)/2.0, (dec_max+dec_min)/2.0)
        self.first_record = first_record
        self.num_records  = num_records
        self.max_angular_distance = angular_distance(self.centre,
                                                     (ra_min, dec_min))
        d    = angular_distance(self.centre, (ra_min, dec_max))
        if d > self.max_angular_distance:
            self.max_angular_distance = d


class TychoIndex:
    def __init__(self, filename):
        self.records_in_main = 2539913
        self.records_in_supl1= 17588
        self.records_in_supl2= 1146
        self.index_list = []
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()


        for i in range(len(lines)):
            l = lines[i]
            linesplit = l.split('|')
            start = int(linesplit[0])
            ra_min = float(linesplit[2])*pi/180
            ra_max = float(linesplit[3])*pi/180
            dec_min = float(linesplit[4])*pi/180
            dec_max = float(linesplit[5])*pi/180
            end = start
            if i != (len(lines)-1):
                end = int(lines[i+1].split('|')[0])
                num_records = end - start
                start -= 1
                self.index_list.append(IndexRecord(start, num_records, ra_min, dec_min, ra_max, dec_max))
        N = len(self.index_list)
        self.ra           = zeros(N)*0.0
        self.dec          = zeros(N)*0.0
        self.max_radius   = zeros(N)*0.0
        self.first_record = zeros(N)

        for i in range(N):
            self.ra[i], self.dec[i] = self.index_list[i].centre
            self.max_radius[i]      = self.index_list[i].max_angular_distance
            self.first_record[i]    = self.index_list[i].first_record


#====================>>>  StarCatalog  <<<====================

class StarCatalog:

    def __init__(self, filename='', indexfilename=''):
        self.catalog = zeros((0,3),dtype=float32)

        if filename != '':
            print(str(self.read_catalog(filename))+' stars loaded.')

        self.index = TychoIndex(indexfilename)


    def read_catalog(self, filename):
        """
        Reads a starcatalog from disc. Format: binary file. One record
        contains:

        32 bit float: ra in radians
        32 bit float: dec in radians
        32 bit float: magnitude

        These floats should be stored most significant byte first (big-endian)

        """
        num_bytes    = os.path.getsize(filename)
        num_records  = num_bytes//12 # 4 bytes times 3 floats
        # read from file using numarray function
        self.catalog = fromfile(filename, float32).reshape((num_records, 3))
        if sys.byteorder == 'little':
            self.catalog.byteswap()
        return num_records


    def select_stars(self, fieldcentre, radius, lm_stars):
        """
        return an array containing [[ra, dec, mag], [ra, dec, mag]]
        etc... for all stars in the field centred around fieldcentre
        with radius 'radius'

        fieldcentre is a tuple (ra, dec) in radians. radius is also in
        radians
        """
        stars_in_catalog = self.catalog.shape[0]

        region_selection = zeros(stars_in_catalog,dtype=bool_)
        fieldsize = angular_distance(fieldcentre, (fieldcentre[0] - radius, fieldcentre[1] - radius))
        d = angular_distance(fieldcentre, (fieldcentre[0] - radius, fieldcentre[1] + radius))
        if d > fieldsize:
            fieldsize = d

        ang_dist = angular_distance(fieldcentre, (self.index.ra, self.index.dec))
        select_regions = (ang_dist - fieldsize - self.index.max_radius) <= 0.0
        first_records = self.index.first_record[select_regions]

        # end records are start of next region...
        temp = select_regions[0:-1].copy()
        select_regions[1:] = temp
        select_regions[0] = False
        end_records   = self.index.first_record[select_regions]

        for i in range(len(first_records)):
            region_selection[int(first_records[i]):int(end_records[i])] = True
        region_selection[self.index.records_in_main:] = True

        selection_array = transpose(array([region_selection,
                                           region_selection,
                                           region_selection],dtype=bool_))

        selected_regions = self.catalog[selection_array]
        stars_in_field = len(selected_regions)//3
        selected_regions = reshape(selected_regions, (stars_in_field, 3))

        ra = selected_regions[:,0]
        dec = selected_regions[:,1]

        ra_sep = abs(ra-fieldcentre[0])
        toosmall = ra_sep < pi
        norm_ra_sep = toosmall * ra_sep + logical_not(toosmall) * (2*pi-ra_sep)
        star_in_field = logical_and(norm_ra_sep*cos(dec) < radius, abs(dec-fieldcentre[1]) < radius)

        selection_array = transpose(array([star_in_field,
                                           star_in_field,
                                           star_in_field],dtype=bool_))
        position_selection = selected_regions[selection_array]
        stars_in_field = len(position_selection)//3
        position_selection = reshape(position_selection, (stars_in_field, 3))

        # select on magnitude
        mag = position_selection[:,2]
        bright_enough = mag <= lm_stars

        selection_array = transpose(array([bright_enough,
                                           bright_enough,
                                           bright_enough], dtype=bool_))
        selection = position_selection[selection_array]
        stars_in_field = len(selection)//3
        selection =  reshape(selection, (stars_in_field, 3))

        return selection


__all__ =['StarCatalog']
