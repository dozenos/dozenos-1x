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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import dozenos.opmode

from dozenos.utils.boot import is_uefi_system
from dozenos.utils.system import get_secure_boot_certificates
from dozenos.utils.system import get_secure_boot_state

def _get_raw_data(name=None):
    sb_data = {
        'state' : get_secure_boot_state(),
        'uefi' : is_uefi_system()
    }
    return sb_data

def _get_formatted_output(raw_data):
    if not raw_data['uefi']:
        print('System run in legacy BIOS mode!')
    state = 'enabled' if raw_data['state'] else 'disabled'
    return f'SecureBoot {state}'

def show(raw: bool):
    sb_data = _get_raw_data()
    if raw:
        return sb_data
    else:
        return _get_formatted_output(sb_data)

def _get_formatted_detail(certificates):
    out = []
    for certificate in certificates:
        out.append(f'Issuer:  {certificate["issuer"]}')
        out.append(f'Subject: {certificate["subject"]}')
    return '\n'.join(out)

def show_detail(raw: bool):
    if not get_secure_boot_state():
        raise dozenos.opmode.UnsupportedOperation('SecureBoot disabled')

    certificates = get_secure_boot_certificates()
    if not certificates:
        raise dozenos.opmode.DataUnavailable('No Linux Kernel signature certificate found')

    if raw:
        return certificates
    else:
        return _get_formatted_detail(certificates)

if __name__ == "__main__":
    try:
        res = dozenos.opmode.run(sys.modules[__name__])
        if res:
            print(res)
    except (ValueError, dozenos.opmode.Error) as e:
        print(e)
        sys.exit(1)
