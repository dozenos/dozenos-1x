# Copyright VyOS maintainers and contributors <maintainers@vyos.io>
# Modifications Copyright DozenOS Contributors. See git history for details.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.

from dozenos.ifconfig.section import Section
from dozenos.ifconfig.control import Control
from dozenos.ifconfig.interface import Interface
from dozenos.ifconfig.operational import Operational
from dozenos.ifconfig.vrrp import VRRP

from dozenos.ifconfig.bond import BondIf
from dozenos.ifconfig.bridge import BridgeIf
from dozenos.ifconfig.dummy import DummyIf
from dozenos.ifconfig.ethernet import EthernetIf
from dozenos.ifconfig.geneve import GeneveIf
from dozenos.ifconfig.loopback import LoopbackIf
from dozenos.ifconfig.macvlan import MACVLANIf
from dozenos.ifconfig.input import InputIf
from dozenos.ifconfig.vxlan import VXLANIf
from dozenos.ifconfig.wireguard import WireGuardIf
from dozenos.ifconfig.vtun import VTunIf
from dozenos.ifconfig.vti import VTIIf
from dozenos.ifconfig.pppoe import PPPoEIf
from dozenos.ifconfig.tunnel import TunnelIf
from dozenos.ifconfig.wireless import WiFiIf
from dozenos.ifconfig.l2tpv3 import L2TPv3If
from dozenos.ifconfig.macsec import MACsecIf
from dozenos.ifconfig.veth import VethIf
from dozenos.ifconfig.wwan import WWANIf
from dozenos.ifconfig.sstpc import SSTPCIf
