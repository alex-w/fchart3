#    fchart3 draws beautiful deepsky charts in vector formats
#    Copyright (C) 2005-2020 fchart authors
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
import os

from .constellation import ConstellationCatalog
from .composite_star_catalog import CompositeStarCatalog
from .deepsky_catalog import DeepskyCatalog
from .hnsky_deepsky import import_hnsky_deepsky
from .vic import import_vic
from . import deepsky_object as deepsky

class UsedCatalogs:
    def __init__(self, data_dir, usno_nomad_file, limiting_magnitude_deepsky=10.0, force_messier=False, force_asterisms=False, force_unknown=False, show_catalogs=None):
        # Read basic catalogs
        self._constellcatalog = ConstellationCatalog(data_dir+os.sep + 'bsc5.dat',
                                               data_dir+os.sep + 'constellationship_western.fab',
                                               data_dir+os.sep + 'constbndJ2000.dat',
                                               data_dir+os.sep + 'cross-id.dat')
        self._starcatalog    = CompositeStarCatalog(data_dir, self._constellcatalog.bsc_map, usno_nomad=usno_nomad_file)
        self._deeplist = self._get_deepsky_list(data_dir, show_catalogs)

        # Apply magnitude selection to deepsky list, build Messier list
        self._reduced_deeplist = []
        self._messierlist=[]
        for dso in self._deeplist:
            if dso.messier > 0:
                self._messierlist.append(dso)
            if force_messier and dso.messier > 0:
                self._reduced_deeplist.append(dso)
            elif dso.mag <= limiting_magnitude_deepsky \
                   and dso.master_object is None \
                   and dso.type != deepsky.GALCL \
                   and (dso.type != deepsky.STARS or force_asterisms or (dso.messier > 0 and dso.type == deepsky.STARS))\
                   and (dso.type != deepsky.PG or force_unknown or dso.type == deepsky.PG and dso.mag > -5.0):
                self._reduced_deeplist.append(dso)

        self._messierlist.sort(key = lambda x: x.messier)
        self._deepskycatalog = DeepskyCatalog(self._reduced_deeplist, force_messier)

    def free_mem(self):
        self._starcatalog.free_mem()

    @property
    def messierlist(self):
        return self._messierlist

    @property
    def starcatalog(self):
        return self._starcatalog

    @property
    def constellcatalog(self):
        return self._constellcatalog

    @property
    def deepskycatalog(self):
        return self._deepskycatalog

    @property
    def deeplist(self):
        return self._deeplist

    @property
    def reduced_deeplist(self):
        return self._reduced_deeplist

    def lookup_dso(self, dso_name):
        index = 0
        cat = ''
        if dso_name[0:3] == 'Sh2':
            cat = 'Sh2'
            index = 4
        elif dso_name[0:2].upper() == '3C':
            cat = '3C'
            index = 2
        else:
            for i in range(len(dso_name)):
                ch = dso_name[i]
                if ch.isalpha():
                    cat += ch
                else:
                    index = i
                    break
            # special handling for Minkowski
            if cat == 'M' and i+1<len(dso_name) and (dso_name[i+1] == '-' or dso_name[i+1] == '_') :
                cat = 'Mi'
            if cat.upper() == 'N' or cat == '' or cat.upper=='NGC':
                cat = 'NGC'

            if cat.upper() == 'I' or cat.upper() == 'IC':
                cat = 'IC'

        name = dso_name[index:].upper().rstrip().lstrip()

        # determine ra, dec of fieldcentre
        found_dso = None
        cat_upper = cat.upper()
        if cat_upper != 'M':
            for dso in self.deeplist:
                if dso.cat.upper() == cat_upper:
                    if name.upper() in dso.all_names:
                        ra = dso.ra
                        dec = dso.dec
                        cat = dso.cat
                        found_dso = dso
                        break
                for syn_dso in dso.synonyms:
                    if syn_dso[0].upper() == cat_upper and name.upper() == syn_dso[1]:
                        ra = dso.ra
                        dec = dso.dec
                        cat = dso.cat
                        found_dso = dso
                        break
                if found_dso:
                    break
        else:
            cat = 'M'
            for mdso in self.messierlist:
                if mdso.messier == int(name):
                    ra = mdso.ra
                    dec = mdso.dec
                    name = str(mdso.messier)
                    found_dso = mdso
                    break

        return found_dso, cat, name

    def _get_deepsky_list(self, data_dir, show_catalogs):
        print('Reading Hnsky...')
        hnskylist = import_hnsky_deepsky(os.path.join(data_dir, 'deep_sky.hnd'), show_catalogs)
        print('Reading VIC...')
        viclist = import_vic(os.path.join(data_dir, 'vic.txt'))
        deeplist = hnskylist + viclist
        deeplist.sort(key=deepsky.cmp_to_key(deepsky.cmp_name))
        return deeplist
