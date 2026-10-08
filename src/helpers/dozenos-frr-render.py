#!/usr/bin/env python3
#
# Copyright (C) VyOS Inc.
# Modifications Copyright DozenOS Contributors. See git history for details.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or later as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Render the FRR configuration and reload FRR without dozenos-configd.

Only dozenos-configd renders FRR, and only at the end of a commit it handled
itself. Two paths need a render without it: a DHCP lease event, which changes
the rendered configuration without any CLI change, and a commit which fell back
to running the conf-mode scripts directly."""

import sys

from dozenos.config import Config
from dozenos.frrender import FRRender
from dozenos.frrender import frr_applied_config_file
from dozenos.frrender import frr_config_file
from dozenos.frrender import frr_render_lock
from dozenos.frrender import get_frrender_dict
from dozenos.utils.file import read_file
from dozenos import ConfigError


def render() -> None:
    """Reload FRR if the rendered configuration differs from the one FRR was
    last reloaded with.

    A fresh instance has no cached configuration, thus its own change detection
    can not be used here. The rendered file is no substitute for it - a render
    which failed before the reload leaves it unapplied."""
    frr = FRRender()
    frr.generate(get_frrender_dict(Config()))

    if read_file(frr_config_file) == read_file(frr_applied_config_file, None):
        return

    frr.apply()


if __name__ == '__main__':
    try:
        with frr_render_lock():
            render()
    except ConfigError as e:
        print(e)
        sys.exit(1)
