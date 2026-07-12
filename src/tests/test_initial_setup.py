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

import unittest
import dozenos.configtree
import dozenos.initialsetup as vis

from unittest import TestCase
from dozenos.xml_ref import definition
from dozenos.xml_ref.pkg_cache.dozenos_1x_cache import reference

class TestInitialSetup(TestCase):
    def setUp(self):
        with open('tests/data/config.boot.default', 'r') as f:
            config_string = f.read()
            self.config = dozenos.configtree.ConfigTree(config_string)
            self.xml = definition.Xml()
            self.xml.define(reference)

    def test_set_user_password(self):
        vis.set_user_password(self.config, 'dozenos', 'dozenosdozenos')

        # Old password hash from the default config
        old_pw = '$6$NfJ1k88mNBeNT/s5$buA/YH21b7raV6mUonph9jiPr4TqUujp0sRQvMm2d5SDF7py2O0EqxN2QL0.797xu7egKJjoZq0EtkDuhXd5c0'
        new_pw = self.config.return_value(["system", "login", "user", "dozenos", "authentication", "encrypted-password"])

        # Just check it changed the hash, don't try to check if hash is good
        self.assertNotEqual(old_pw, new_pw)

    def test_disable_user_password(self):
        vis.disable_user_password(self.config, 'dozenos')
        new_pw = self.config.return_value(["system", "login", "user", "dozenos", "authentication", "encrypted-password"])

        self.assertEqual(new_pw, '!')

    def test_set_ssh_key_with_name(self):
        test_ssh_key = " ssh-rsa fakedata dozenos@dozenos "
        vis.set_user_ssh_key(self.config, 'dozenos', test_ssh_key)

        key_type = self.config.return_value(["system", "login", "user", "dozenos", "authentication", "public-keys", "dozenos@dozenos", "type"])
        key_data = self.config.return_value(["system", "login", "user", "dozenos", "authentication", "public-keys", "dozenos@dozenos", "key"])

        self.assertEqual(key_type, 'ssh-rsa')
        self.assertEqual(key_data, 'fakedata')
        self.assertTrue(self.xml.is_tag(["system", "login", "user", "dozenos", "authentication", "public-keys"]))

    def test_set_ssh_key_without_name(self):
        # If key file doesn't include a name, the function will use user name for the key name

        test_ssh_key = " ssh-rsa fakedata  "
        vis.set_user_ssh_key(self.config, 'dozenos', test_ssh_key)

        key_type = self.config.return_value(["system", "login", "user", "dozenos", "authentication", "public-keys", "dozenos", "type"])
        key_data = self.config.return_value(["system", "login", "user", "dozenos", "authentication", "public-keys", "dozenos", "key"])

        self.assertEqual(key_type, 'ssh-rsa')
        self.assertEqual(key_data, 'fakedata')
        self.assertTrue(self.xml.is_tag(["system", "login", "user", "dozenos", "authentication", "public-keys"]))

    def test_create_user(self):
        vis.create_user(self.config, 'jrandomhacker', password='qwerty', key=" ssh-rsa fakedata jrandomhacker@foovax ")

        self.assertTrue(self.config.exists(["system", "login", "user", "jrandomhacker"]))
        self.assertTrue(self.config.exists(["system", "login", "user", "jrandomhacker", "authentication", "public-keys", "jrandomhacker@foovax"]))
        self.assertTrue(self.config.exists(["system", "login", "user", "jrandomhacker", "authentication", "encrypted-password"]))
        self.assertEqual(self.config.return_value(["system", "login", "user", "jrandomhacker", "level"]), "admin")

    def test_set_hostname(self):
        vis.set_host_name(self.config, "dozenos-test")

        self.assertEqual(self.config.return_value(["system", "host-name"]), "dozenos-test")

    def test_set_name_servers(self):
        vis.set_name_servers(self.config, ["192.0.2.10", "203.0.113.20"])
        servers = self.config.return_values(["system", "name-server"])

        self.assertIn("192.0.2.10", servers)
        self.assertIn("203.0.113.20", servers)

    def test_set_gateway(self):
        vis.set_default_gateway(self.config, '192.0.2.1')

        self.assertTrue(self.config.exists(['protocols', 'static', 'route', '0.0.0.0/0', 'next-hop', '192.0.2.1']))
        self.assertTrue(self.xml.is_tag(['protocols', 'static', 'mroute', '0.0.0.0/0', 'next-hop']))
        self.assertTrue(self.xml.is_tag(['protocols', 'static', 'mroute']))

if __name__ == "__main__":
    unittest.main()
