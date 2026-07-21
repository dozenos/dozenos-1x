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

import os
import paramiko
import re
import unittest

from base_dozenostest_shim import DozenOSUnitTestSHIM

from dozenos.configsession import ConfigSessionError
from dozenos.defaults import config_files
from dozenos.utils.auth import get_local_passwd_entries
from dozenos.utils.process import cmdl
from dozenos.utils.process import is_systemd_service_running
from dozenos.utils.process import process_named_running
from dozenos.utils.file import read_file
from dozenos.utils.file import write_file
from dozenos.xml_ref import default_value

PROCESS_NAME = 'sshd'
SSHD_CONF = '/run/sshd/sshd_config'
base_path = ['service', 'ssh']
pki_path = ['pki']

key_rsa = '/etc/ssh/ssh_host_rsa_key'
key_dsa = '/etc/ssh/ssh_host_dsa_key'
key_ed25519 = '/etc/ssh/ssh_host_ed25519_key'
trusted_user_ca = config_files['sshd_user_ca']
test_command = 'uname -a'

def get_config_value(key):
    tmp = read_file(SSHD_CONF)
    tmp = re.findall(f'\n?{key}\s+(.*)', tmp)
    return tmp

trusted_user_ca_path = base_path + ['trusted-user-ca']
# CA and signed user key generated using:
# ssh-keygen -f dozenos-ssh-ca.key
# ssh-keygen -f dozenos_testca  -C "dozenos_tesca@dozenos.local"
# ssh-keygen -s dozenos-ssh-ca.key -I dozenos_testca@dozenos.local -n dozenos,dozenos_testca -V +520w dozenos_testca.pub
ca_cert_data = """
AAAAB3NzaC1yc2EAAAADAQABAAABgQDAfP5YRTOkcZXD4njC6fVAUwbFMuqXN3cMoyEHBT
uiaEgQ1IH7L92foCurrMnNZVLmOUZxMnX5pHXVkIsV+FhchpucqMDvtihTpuC52KbPXSGg
y+sstVLjcrwPpT5MTD7BO0WV0LR9CWJjVDCvBKnLtBbd64XTAE7EgF0digpuQ5fCLHt2yt
/xhjfHGSXn9jsC9KlcLvTE0OjZuLSVA917m/9t3/l/UFXhk3iGkx4UzO9wOuzclgRHkBNv
Iu3YTM94FIYHszChSIPt331F46koM43JhMbNWOdfxKODhpRMduwNDgOis9dWy+sRoftjfm
7w/DdMTnWi4HFJSwMJll/frlpyBtSF3QMxVZ+qYKnmFdzgholMGDZ3vT9ugRrDNs0eHEoW
nFcWsu5O1Ed/qGTFC/r0eMKVgbCB3wpPwZxi1993cNWgdeYk/d/YOuS3A1y6DtQBc8nJD/
Gfhrf1uTTbW29nKVoJclzvrplkhYxXeNlALlVyqFmCteGmtj64XxU=
"""

cert_user_key = """-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
"""

cert_user_signed = """
ssh-rsa-cert-v01@openssh.com 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
bFzYKJ0OVLA9gWKrIntgw==
"""

class TestServiceSSH(DozenOSUnitTestSHIM.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestServiceSSH, cls).setUpClass()

        # ensure we can also run this test on a live system - so lets clean
        # out the current configuration :)
        cls.cli_delete(cls, base_path)
        cls.cli_delete(cls, ['vrf'])

    def tearDown(self):
        # Check for running process
        self.assertTrue(process_named_running(PROCESS_NAME))

        # delete testing SSH config
        self.cli_delete(base_path)
        self.cli_delete(['vrf'])
        self.cli_commit()

        self.assertTrue(os.path.isfile(key_rsa))
        self.assertTrue(os.path.isfile(key_dsa))
        self.assertTrue(os.path.isfile(key_ed25519))

        # Established SSH connections remains running after service is stopped.
        # We cannot use process_named_running here - we rather need to check
        # that the systemd service is no longer running
        self.assertFalse(is_systemd_service_running(PROCESS_NAME))
        # always forward to base class
        super().tearDown()

    def test_ssh_default(self):
        # Check if SSH service runs with default settings - used for checking
        # behavior of <defaultValue> in XML definition
        self.cli_set(base_path)

        # commit changes
        self.cli_commit()

        # Check configured port against CLI default value
        port = get_config_value('Port')
        cli_default = default_value(base_path + ['port'])
        self.assertEqual(port, cli_default)

    def test_ssh_single_listen_address(self):
        # Check if SSH service can be configured and runs
        self.cli_set(base_path + ['port', '1234'])
        self.cli_set(base_path + ['disable-host-validation'])
        self.cli_set(base_path + ['disable-password-authentication'])
        self.cli_set(base_path + ['loglevel', 'verbose'])
        self.cli_set(base_path + ['client-keepalive-interval', '100'])
        self.cli_set(base_path + ['listen-address', '127.0.0.1'])

        # commit changes
        self.cli_commit()

        # Check configured port
        port = get_config_value('Port')[0]
        self.assertTrue('1234' in port)

        # Check DNS usage
        dns = get_config_value('UseDNS')[0]
        self.assertTrue('no' in dns)

        # Check PasswordAuthentication
        pwd = get_config_value('PasswordAuthentication')[0]
        self.assertTrue('no' in pwd)

        # Check loglevel
        loglevel = get_config_value('LogLevel')[0]
        self.assertTrue('VERBOSE' in loglevel)

        # Check listen address
        address = get_config_value('ListenAddress')[0]
        self.assertTrue('127.0.0.1' in address)

        # Check keepalive
        keepalive = get_config_value('ClientAliveInterval')[0]
        self.assertTrue('100' in keepalive)

    def test_ssh_multiple_listen_addresses(self):
        # Check if SSH service can be configured and runs with multiple
        # listen ports and listen-addresses
        ports = ['22', '2222', '2223', '2224']
        for port in ports:
            self.cli_set(base_path + ['port', port])

        addresses = ['127.0.0.1', '::1']
        for address in addresses:
            self.cli_set(base_path + ['listen-address', address])

        # commit changes
        self.cli_commit()

        # Check configured port
        tmp = get_config_value('Port')
        for port in ports:
            self.assertIn(port, tmp)

        # Check listen address
        tmp = get_config_value('ListenAddress')
        for address in addresses:
            self.assertIn(address, tmp)

    def test_ssh_vrf_single(self):
        vrf = 'mgmt'
        # Check if SSH service can be bound to given VRF
        self.cli_set(base_path + ['vrf', vrf])

        # VRF does yet not exist - an error must be thrown
        with self.assertRaises(ConfigSessionError):
            self.cli_commit()

        self.cli_set(['vrf', 'name', vrf, 'table', '1338'])

        # commit changes
        self.cli_commit()

        # Check for process in VRF
        tmp = cmdl(['ip', 'vrf', 'pids', vrf])
        self.assertIn(PROCESS_NAME, tmp)

    def test_ssh_vrf_multi(self):
        # Check if SSH service can be bound to multiple VRFs
        vrfs = ['red', 'blue', 'green']
        for vrf in vrfs:
            self.cli_set(base_path + ['vrf', vrf])

        # VRF does yet not exist - an error must be thrown
        with self.assertRaises(ConfigSessionError):
            self.cli_commit()

        table = 12345
        for vrf in vrfs:
            self.cli_set(['vrf', 'name', vrf, 'table', str(table)])
            table += 1

        # commit changes
        self.cli_commit()

        # Check for process in VRF
        for vrf in vrfs:
            tmp = cmdl(['ip', 'vrf', 'pids', vrf])
            self.assertIn(PROCESS_NAME, tmp)

    def test_ssh_login(self):
        # Perform SSH login and command execution with a predefined user. The
        # result (output of uname -a) must match the output if the command is
        # run natively.
        #
        # We also try to login as an invalid user - this is not allowed to work.
        test_user = 'ssh_test'
        test_pass = 'v2i57DZs8idUwMN3VC92'

        self.cli_set(base_path)
        self.cli_set(['system', 'login', 'user', test_user, 'authentication',
                      'plaintext-password', test_pass])

        # commit changes
        self.cli_commit()

        # Login with proper credentials
        output, error = self.ssh_send_cmd(test_command, test_user, test_pass)
        # verify login
        self.assertFalse(error)
        self.assertEqual(output, cmdl(test_command.split()))

        # Login with invalid credentials
        with self.assertRaises(paramiko.ssh_exception.AuthenticationException):
            output, error = self.ssh_send_cmd(test_command, 'invalid_user',
                                              'invalid_password')

        self.cli_delete(['system', 'login', 'user', test_user])
        self.cli_commit()

        # After deletion the test user is not allowed to remain in /etc/passwd
        usernames = [x.pw_name for x in get_local_passwd_entries()]
        self.assertNotIn(test_user, usernames)

    def test_ssh_dynamic_protection(self):
        # check sshguard service

        SSHGUARD_CONFIG = '/etc/sshguard/sshguard.conf'
        SSHGUARD_WHITELIST = '/etc/sshguard/whitelist'
        SSHGUARD_PROCESS = 'sshguard'
        block_time = '123'
        detect_time = '1804'
        port = '22'
        threshold = '10'
        allow_list = ['192.0.2.0/24', '2001:db8::/48']

        self.cli_set(base_path + ['dynamic-protection', 'block-time', block_time])
        self.cli_set(base_path + ['dynamic-protection', 'detect-time', detect_time])
        self.cli_set(base_path + ['dynamic-protection', 'threshold', threshold])
        for allow in allow_list:
            self.cli_set(base_path + ['dynamic-protection', 'allow-from', allow])

        # commit changes
        self.cli_commit()

        # Check configured port
        tmp = get_config_value('Port')
        self.assertIn(port, tmp)

        # Check sshgurad service
        self.assertTrue(process_named_running(SSHGUARD_PROCESS))

        sshguard_lines = [
            f'THRESHOLD={threshold}',
            f'BLOCK_TIME={block_time}',
            f'DETECTION_TIME={detect_time}',
        ]

        tmp_sshguard_conf = read_file(SSHGUARD_CONFIG)
        for line in sshguard_lines:
            self.assertIn(line, tmp_sshguard_conf)

        tmp_whitelist_conf = read_file(SSHGUARD_WHITELIST)
        for allow in allow_list:
            self.assertIn(allow, tmp_whitelist_conf)

        # Delete service ssh dynamic-protection
        # but not service ssh itself
        self.cli_delete(base_path + ['dynamic-protection'])
        self.cli_commit()

        self.assertFalse(process_named_running(SSHGUARD_PROCESS))

    # Network Device Collaborative Protection Profile
    def test_ssh_ndcpp(self):
        ciphers = ['aes128-cbc', 'aes128-ctr', 'aes256-cbc', 'aes256-ctr']
        host_key_algs = ['sk-ssh-ed25519@openssh.com', 'ssh-rsa', 'ssh-ed25519']
        kexes = [
            'diffie-hellman-group14-sha1',
            'ecdh-sha2-nistp256',
            'ecdh-sha2-nistp384',
            'ecdh-sha2-nistp521',
        ]
        macs = ['hmac-sha1', 'hmac-sha2-256', 'hmac-sha2-512']
        rekey_time = '60'
        rekey_data = '1024'

        for cipher in ciphers:
            self.cli_set(base_path + ['cipher', cipher])
        for host_key in host_key_algs:
            self.cli_set(base_path + ['hostkey-algorithm', host_key])
        for kex in kexes:
            self.cli_set(base_path + ['key-exchange', kex])
        for mac in macs:
            self.cli_set(base_path + ['mac', mac])
        # Optional rekey parameters
        self.cli_set(base_path + ['rekey', 'data', rekey_data])
        self.cli_set(base_path + ['rekey', 'time', rekey_time])

        # commit changes
        self.cli_commit()

        ssh_lines = [
            'Ciphers aes128-cbc,aes128-ctr,aes256-cbc,aes256-ctr',
            'HostKeyAlgorithms sk-ssh-ed25519@openssh.com,ssh-rsa,ssh-ed25519',
            'MACs hmac-sha1,hmac-sha2-256,hmac-sha2-512',
            'KexAlgorithms diffie-hellman-group14-sha1,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521',
            'RekeyLimit 1024M 60M',
        ]
        tmp_sshd_conf = read_file(SSHD_CONF)

        for line in ssh_lines:
            self.assertIn(line, tmp_sshd_conf)

    def test_ssh_pubkey_accepted_algorithm(self):
        algs = [
            'ssh-ed25519',
            'ecdsa-sha2-nistp256',
            'ecdsa-sha2-nistp384',
            'ecdsa-sha2-nistp521',
            'ssh-dss',
            'ssh-rsa',
            'rsa-sha2-256',
            'rsa-sha2-512',
        ]

        expected = 'PubkeyAcceptedAlgorithms '
        for alg in algs:
            self.cli_set(base_path + ['pubkey-accepted-algorithm', alg])
            expected = f'{expected}{alg},'
        expected = expected[:-1]

        self.cli_commit()
        tmp_sshd_conf = read_file(SSHD_CONF)
        self.assertIn(expected, tmp_sshd_conf)

    def test_ssh_trusted_user_ca(self):
        ca_cert_name = 'test_ca'
        public_key_type = 'ssh-rsa'
        public_key_data = ca_cert_data.replace('\n', '')
        test_user = 'dozenos_testca'
        principal = 'dozenos'
        user_auth_base = ['system', 'login', 'user', test_user]

        # create user account
        self.cli_set(user_auth_base)
        self.cli_set(pki_path + ['openssh', ca_cert_name, 'public',
                                 'key', public_key_data])
        self.cli_set(pki_path + ['openssh', ca_cert_name, 'public',
                                 'type', public_key_type])
        self.cli_set(trusted_user_ca_path, value=ca_cert_name)
        self.cli_commit()

        trusted_user_ca_config = get_config_value('TrustedUserCAKeys')
        self.assertIn(trusted_user_ca, trusted_user_ca_config)

        authorize_principals_file_config = get_config_value('AuthorizedPrincipalsFile')
        self.assertIn('none', authorize_principals_file_config)

        ca_key_contents = read_file(trusted_user_ca).lstrip().rstrip()
        self.assertIn(f'{public_key_type} {public_key_data}', ca_key_contents)

        # Verify functionality by logging into the system using signed user key
        key_filename = f'/tmp/{test_user}'
        write_file(key_filename, cert_user_key, mode=0o600)
        write_file(f'{key_filename}-cert.pub', cert_user_signed.replace('\n', ''))

        # Login with proper credentials
        output, error = self.ssh_send_cmd(test_command, test_user, password=None,
                                          key_filename=key_filename)
        # Verify login
        self.assertFalse(error)
        self.assertEqual(output, cmdl(test_command.split()))

        # Enable user principal name - logins only allowed if certificate contains
        # said principal name
        self.cli_set(user_auth_base + ['authentication', 'principal', principal])
        self.cli_commit()

        # Verify generated SSH principals
        authorized_principals_file = f'/home/{test_user}/.ssh/authorized_principals'
        authorized_principals = read_file(authorized_principals_file, sudo=True)
        self.assertIn(principal, authorized_principals)

        # Login with proper credentials
        output, error = self.ssh_send_cmd(test_command, test_user, password=None,
                                          key_filename=key_filename)
        # Verify login
        self.assertFalse(error)
        self.assertEqual(output, cmdl(test_command.split()))

        self.cli_delete(trusted_user_ca_path)
        self.cli_delete(user_auth_base)
        self.cli_delete(['pki', 'ca', ca_cert_name])
        self.cli_commit()

        # Verify the CA key is removed
        trusted_user_ca_config = get_config_value('TrustedUserCAKeys')
        self.assertNotIn(trusted_user_ca, trusted_user_ca_config)
        self.assertFalse(os.path.exists(trusted_user_ca))

        authorize_principals_file_config = get_config_value('AuthorizedPrincipalsFile')
        self.assertNotIn('none', authorize_principals_file_config)
        self.assertFalse(os.path.exists(f'/home/{test_user}/.ssh/authorized_principals'))

    def test_ssh_fido(self):
        # Order does matter for this test because of how the template
        # collects and maps the options.
        opt_map = {
            'pin-required': 'verify-required',
            'touch-required': 'touch-required',
        }
        expected = 'PubkeyAuthOptions '
        for k, v in opt_map.items():
            self.cli_set(base_path + ['fido', k])
            expected = f'{expected}{v} '
        expected = expected[:-1]
        self.cli_commit()
        tmp_sshd_conf = read_file(SSHD_CONF)
        self.assertIn(expected, tmp_sshd_conf)


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=DozenOSUnitTestSHIM.TestCase.debug_on())
