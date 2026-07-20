#!/usr/bin/env python3
#
# Copyright VyOS maintainers and contributors <maintainers@vyos.io>
# Modifications Copyright DozenOS Contributors. See git history for details.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or later as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This script is a helper to run VTYSH commands for "show evpn", allowing for the --raw flag to output JSON

import sys
import typing
import json

import dozenos.opmode
from dozenos.utils.process import cmdl

def show_evpn(raw: bool, command: typing.Optional[str]):
    if raw:
        command = f"{command} json"
        evpnDict = {}
        try:
            evpnDict['evpn'] = json.loads(cmdl(['vtysh', '-c', command]))
        except:
            raise dozenos.opmode.DataUnavailable(f"\"{command.replace(' json', '')}\" is invalid or has no JSON option")

        return evpnDict
    else:
        return cmdl(['vtysh', '-c', command])

if __name__ == '__main__':
    try:
        res = dozenos.opmode.run(sys.modules[__name__])
        if res:
            print(res)
    except (ValueError, dozenos.opmode.Error) as e:
        print(e)
        sys.exit(1)
