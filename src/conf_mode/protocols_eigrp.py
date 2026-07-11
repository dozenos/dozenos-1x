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

from sys import exit
from sys import argv

from dozenos.config import Config
from dozenos.configverify import has_frr_protocol_in_dict
from dozenos.configverify import verify_vrf
from dozenos.utils.dict import dict_search
from dozenos.utils.process import is_systemd_service_running
from dozenos.frrender import FRRender
from dozenos.frrender import get_frrender_dict
from dozenos import ConfigError
from dozenos import airbag
airbag.enable()

def get_config(config=None):
    if config:
        conf = config
    else:
        conf = Config()

    return get_frrender_dict(conf, argv)

def verify(config_dict):
    if not has_frr_protocol_in_dict(config_dict, 'eigrp'):
        return None

    vrf = None
    if 'vrf_context' in config_dict:
        vrf = config_dict['vrf_context']

    # equivalent of the C foo ? 'a' : 'b' statement
    eigrp = vrf and dict_search(f'vrf.name.{vrf}.protocols.eigrp',
                                 config_dict) or config_dict['eigrp']
    eigrp['policy'] = config_dict['policy']

    if 'system_as' not in eigrp:
        raise ConfigError('EIGRP system-as must be defined!')

    if vrf:
        verify_vrf({'vrf': vrf})

def generate(config_dict):
    if config_dict and not is_systemd_service_running('dozenos-configd.service'):
        FRRender().generate(config_dict)
    return None

def apply(config_dict):
    if config_dict and not is_systemd_service_running('dozenos-configd.service'):
        FRRender().apply()
    return None

if __name__ == '__main__':
    try:
        c = get_config()
        verify(c)
        generate(c)
        apply(c)
    except ConfigError as e:
        print(e)
        exit(1)
