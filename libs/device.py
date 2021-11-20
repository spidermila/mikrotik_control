import subprocess
from time import monotonic
from typing import List
from typing import Optional

import paramiko

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

        self.interfaces: List[Interface] = []
        self.time_of_last_update: Optional[int] = None

    def enought_time_passed(self, timeout: int = 20) -> bool:
        current_time = int(monotonic())
        if not self.time_of_last_update:
            self.time_of_last_update = current_time
            return True
        if current_time - self.time_of_last_update > timeout:
            self._set_time_since_last_update_now()
            return True
        return False

    def _set_time_since_last_update_now(self):
        current_time = int(monotonic())
        self.time_of_last_update = current_time

    def test_connection(self) -> bool:
        result = False
        if self._ping_test():
            result = True
            if self._ssh_test():
                result = True
            else:
                result = False
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

    def get_interfaces_from_device(self) -> None:
        print(f'Updating interfaces from {self.name}...')
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
            return
        else:
            self.interfaces = []
            remote_cmd = 'interface print terse'
            stdin, stdout, stderr = ssh.exec_command(remote_cmd)
            for line in stdout.readlines():
                if 'name' not in line:
                    break
                new_line = line.strip('\n')
                number = int(new_line.split()[0])
                name = new_line.split('name=')[1].split()[0]
                comment = ''
                if 'comment=' in new_line:
                    raw_comment = new_line.split('comment=')[1].split()[:-1]
                    output = []
                    for item in raw_comment:
                        if '=' in item:
                            break
                        output.append(item)
                    comment = ' '.join(output)
                status = new_line.split()[1]
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
                self.interfaces.append(
                    Interface(
                        number,
                        name,
                        disabled,
                        running,
                        slave,
                        dynamic,
                        comment,
                    ),
                )

            ssh.close()

    def print_cached_interfaces(self) -> None:
        if len(self.interfaces) == 0:
            self.get_interfaces_from_device()
            self._set_time_since_last_update_now()
        if self.enought_time_passed():
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
