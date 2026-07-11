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

import dozenos.configtree

from unittest import TestCase

class TestConfigDiff(TestCase):
    def setUp(self):
        with open('tests/data/config.left', 'r') as f:
            config_string = f.read()
            self.config_left = dozenos.configtree.ConfigTree(config_string)

        with open('tests/data/config.right', 'r') as f:
            config_string = f.read()
            self.config_right = dozenos.configtree.ConfigTree(config_string)

        self.config_null = dozenos.configtree.ConfigTree('')

    def test_unit(self):
        diff = dozenos.configtree.DiffTree(self.config_left, self.config_null)
        sub = diff.sub
        self.assertEqual(sub, self.config_left)

        diff = dozenos.configtree.DiffTree(self.config_null, self.config_left)
        add = diff.add
        self.assertEqual(add, self.config_left)

    def test_symmetry(self):
        lr_diff = dozenos.configtree.DiffTree(self.config_left,
                                           self.config_right)
        rl_diff = dozenos.configtree.DiffTree(self.config_right,
                                           self.config_left)

        sub = lr_diff.sub
        add = rl_diff.add
        self.assertEqual(sub, add)
        add = lr_diff.add
        sub = rl_diff.sub
        self.assertEqual(add, sub)

    def test_identity(self):
        lr_diff = dozenos.configtree.DiffTree(self.config_left,
                                           self.config_right)

        sub = lr_diff.sub
        inter = lr_diff.inter
        add = lr_diff.add

        r_union = dozenos.configtree.union(add, inter)
        l_union = dozenos.configtree.union(sub, inter)

        # here we must compare string representations instead of using
        # dunder equal, as we assert equivalence of the values list, which
        # is optionally ordered at render
        self.assertEqual(r_union.to_string(),
                         self.config_right.to_string(ordered_values=True))
        self.assertEqual(l_union.to_string(),
                         self.config_left.to_string(ordered_values=True))
