#    fchart3 draws beautiful deepsky charts in vector formats
#    Copyright (C) 2005-2025 fchart3 authors
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

from .base_renderer import BaseRenderer


CARDINAL_DIRECTIONS = [
    ("N", 0),
    ("NW", math.pi / 4),
    ("W", math.pi / 2),
    ("SW", math.pi / 2 + math.pi / 4),
    ("S", math.pi),
    ("SE", math.pi + math.pi / 4),
    ("E", 3 * math.pi / 2),
    ("NE", 3 * math.pi / 2 + math.pi / 4),
]


class HorizonRenderer(BaseRenderer):
    def draw(self, ctx, state):
        if ctx.cfg.show_horizon:
            self.draw_horizon(ctx, state)

    def draw_horizon(self, ctx, state):
        gfx = ctx.gfx
        cfg = ctx.cfg
        gfx.save()
        gfx.set_linewidth(cfg.horizon_linewidth)
        gfx.set_solid_line()
        gfx.set_pen_rgb(cfg.horizon_color)

        daz = ctx.field_radius / 10
        x11, y11, z11 = (None, None, None)
        agg_az = 0
        nzopt = not ctx.transf.is_zoptim()

        alt = 0

        while True:
            x12, y12, z12 = ctx.transf.horizontal_to_xyz(ctx.center_celestial[0] + agg_az, alt)
            x22, y22, z22 = ctx.transf.horizontal_to_xyz(ctx.center_celestial[0] - agg_az, 0)
            if x11 is not None and (nzopt or (z11 > 0 and z12 > 0)):
                gfx.line(x11, y11, x12, y12)
                gfx.line(x21, y21, x22, y22)
            agg_az = agg_az + daz
            if agg_az > math.pi:
                break
            if y11 is not None and x12 < -ctx.drawing_width / 2:
                break
            x11, y11, z11 = (x12, y12, z12)
            x21, y21, z21 = (x22, y22, z22)

        gfx.restore()

        label_fh = cfg.cardinal_directions_font_scale * gfx.gi_default_font_size
        gfx.set_font(gfx.gi_font, label_fh)

        for label, azimuth in CARDINAL_DIRECTIONS:
            x, y, z = ctx.transf.horizontal_to_xyz(azimuth, 0)
            if z > 0:
                x_up, y_up, _ = ctx.transf.horizontal_to_xyz(azimuth, math.pi / 20)
                gfx.save()
                gfx.set_pen_rgb(cfg.cardinal_directions_color)
                gfx.translate(x, y)
                text_ang = math.atan2(x_up - x, y_up - y)
                gfx.rotate(-text_ang)
                gfx.text_centred(0, label_fh, label)
                gfx.restore()
