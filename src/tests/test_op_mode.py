# Copyright VyOS maintainers and contributors <maintainers@vyos.io>
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

from unittest import TestCase

import dozenos.opmode

class TestDozenOSOpMode(TestCase):
    def test_field_name_normalization(self):
        from dozenos.opmode import _normalize_field_name

        self.assertEqual(_normalize_field_name(" foo bar "), "foo_bar")
        self.assertEqual(_normalize_field_name("foo-bar"), "foo_bar")
        self.assertEqual(_normalize_field_name("foo (bar) baz"), "foo_bar_baz")
        self.assertEqual(_normalize_field_name("load%"), "load_percentage")

    def test_dict_fields_normalization_non_unique(self):
        from dozenos.opmode import _normalize_field_names

        # Space and dot are both replaced by an underscore,
        # so dicts like this cannor be normalized uniquely
        data = {"foo bar": True, "foo.bar": False}

        with self.assertRaises(dozenos.opmode.InternalError):
            _normalize_field_names(data)

    def test_dict_fields_normalization_simple_dict(self):
        from dozenos.opmode import _normalize_field_names

        data = {"foo bar": True, "Bar-Baz": False}
        self.assertEqual(_normalize_field_names(data), {"foo_bar": True, "bar_baz": False})

    def test_dict_fields_normalization_nested_dict(self):
        from dozenos.opmode import _normalize_field_names

        data = {"foo bar": True, "bar-baz": {"baz-quux": {"quux-xyzzy": False}}}
        self.assertEqual(_normalize_field_names(data),
          {"foo_bar": True, "bar_baz": {"baz_quux": {"quux_xyzzy": False}}})

    def test_dict_fields_normalization_mixed(self):
        from dozenos.opmode import _normalize_field_names

        data = [{"foo bar": True, "bar-baz": [{"baz-quux": {"quux-xyzzy": [False]}}]}]
        self.assertEqual(_normalize_field_names(data),
          [{"foo_bar": True, "bar_baz": [{"baz_quux": {"quux_xyzzy": [False]}}]}])

    def test_dict_fields_normalization_primitive(self):
        from dozenos.opmode import _normalize_field_names

        data = [1, False, "foo"]
        self.assertEqual(_normalize_field_names(data), [1, False, "foo"])
