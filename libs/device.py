import subprocess
from typing import Optional

import paramiko

from libs.capsman.capsman import Capsman
from libs.configuration import Configuration
from libs.cprint import cprint
from libs.group import Group
from libs.interface import Interface

# paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)


class Device:
    def __init__(
            self,
            name: str,
            address: str,
            port: int,
            user: str,
            encrypted_password: str,
            group: Group,
            config: Configuration,
    ) -> None:
        self.name = name
        self.address = address
        self.port = port
        self.user = user
        self.encrypted_password = encrypted_password
        self.group = group
        self.config = config

        self.interfaces: list[Interface] = []
        self.os_version: str = ''
        self.time_of_last_update: Optional[int] = None

        self.capsman = Capsman()

    def test_connection(self) -> list[bool]:
        result = [False, False]
        if self._ping_test():
            result[0] = True
            if self._ssh_test():
                result[1] = True
        return result

    def _ssh_test(self) -> bool:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(
                hostname=self.address,
                port=self.port,
                username=self.user,
                password=self.config.password_decrypt(
                    bytes(self.encrypted_password, 'utf-8'),
                ),
                look_for_keys=False,
            )
        except (
            paramiko.AuthenticationException,
            paramiko.SSHException,
        ) as err:
            print(f'ssh err on {self.name}: {err}')
            return False
        else:
            # remote_cmd = 'interface print terse'
            # stdin, stdout, stderr = ssh.exec_command(remote_cmd)
            # for line in stdout.readlines():
            #     print(line.strip('\n'))
            # print((
            #   "Options available to deal with the "
            #   f"connectios are many like\n{dir(ssh)}"
            # ))
            ssh.close()
            return True

    def _ping_test(self) -> bool:
        result = subprocess.run(
            [
                'ping',
                '-c1',
                self.address,
            ],
            shell=False,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            print('-'*20)
            print(f'Error when pinging {self.name}')
            print('stdout:')
            print(f"{result.stdout.decode('utf-8')}")
            print('stderr:')
            print(f"{result.stderr.decode('utf-8')}")
            print('-'*20)
            return False
        return True

    def _ssh_call(self, remote_cmd: str) -> list:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(
                hostname=self.address,
                port=self.port,
                username=self.user,
                password=self.config.password_decrypt(
                    bytes(self.encrypted_password, 'utf-8'),
                ),
                look_for_keys=False,
            )
        except paramiko.AuthenticationException as err:
            print(f'ssh err on {self.name}: {err}')
            return []
        else:
            stdin, stdout, stderr = ssh.exec_command(remote_cmd)
            output = []
            for line in stdout.readlines():
                output.append(line.strip('\n'))
            ssh.close()
            return output

    def get_interfaces_from_device(self) -> None:
        print(f'Updating interfaces from {self.name}...')
        output = self._ssh_call('interface print terse')
        self.interfaces = []
        for line in output:
            if 'name' not in line:
                break
            number = int(line.split()[0])
            name = line.split('name=')[1].split()[0]
            comment = ''
            if 'comment=' in line:
                raw_comment = line.split('comment=')[1].split()[:-1]
                output = []
                for item in raw_comment:
                    if '=' in item:
                        break
                    output.append(item)
                comment = ' '.join(output)
            status = line.split()[1]
            if 'X' in status:
                disabled = True
            else:
                disabled = False
            if 'R' in status:
                running = True
            else:
                running = False
            if 'S' in status:
                slave = True
            else:
                slave = False
            if 'D' in status:
                dynamic = True
            else:
                dynamic = False
            interface = Interface(
                    number,
                    name,
                    disabled,
                    running,
                    slave,
                    dynamic,
                    comment,
            )
            interface._set_time_since_last_update_now()
            self.interfaces.append(interface)

    def get_os_version(self) -> None:
        output = self._ssh_call('system package print')
        for line in output:
            if 'routeros' in line:
                self.os_version = line.split()[2]
                print(f'{self.name} os version refreshed')

    def get_name(self) -> str:
        output = self._ssh_call('system identity print')
        return output[0].split()[1]

    def get_capsman_manager_status(self) -> None:
        # print(f'Updating capsman status from {self.name}...')
        output = self._ssh_call('caps-man manager print')
        for line in output:
            if 'enabled:' in line:
                if 'yes' in line:
                    self.capsman.enabled = True
                else:
                    self.capsman.enabled = False
                self.capsman.status_known = True
                return

    def get_capsman_acl(self) -> None:
        output = self._ssh_call('caps-man access-list print terse')
        self.capsman.acl.items = []
        for line in output:
            if len(line.split()) > 1:
                number = line.split()[0]
                if 'comment=' in line:
                    comment = line.split(
                        'mac-address',
                    )[0].split('comment=')[1].strip()
                else:
                    comment = ''
                if 'mac-address' in line:
                    macaddress = line.split('mac-address=')[-1].split()[0]
                else:
                    macaddress = ''
                if 'interface' in line:
                    interface = line.split('interface=')[-1].split()[0]
                else:
                    interface = ''
                if 'action' in line:
                    action = line.split('action=')[-1].split()[0]
                else:
                    action = ''
                self.capsman.acl.additem(
                    number,
                    comment,
                    macaddress,
                    interface,
                    action,
                )

    def print_cached_interfaces(self) -> None:
        if len(self.interfaces) == 0:
            self.get_interfaces_from_device()
        if self.interfaces[0].enought_time_passed():
            self.get_interfaces_from_device()
        if len(self.interfaces) == 0:
            print('No interfaces found')
            return
        rows = []
        for interface in self.interfaces:
            status = ''
            if interface.dynamic:
                status += 'D'
            if interface.running:
                status += 'R'
            if interface.slave:
                status += 'S'
            if interface.disabled:
                status += 'X'
            row = [
                f'{interface.number}',
                f':{interface.name}',
                f':{status}',
                f':{interface.comment}',
            ]
            rows.append(row)
        cprint(rows)
