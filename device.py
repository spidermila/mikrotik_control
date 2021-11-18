import paramiko
import subprocess

from configuration import Configuration

# paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

class Device:
    def __init__(
            self,
            name: str,
            address: str,
            port: int,
            user: str,
            encrypted_password: str,
            config: Configuration
        ) -> None:
        self.name = name
        self.address = address
        self.port = port
        self.user = user
        self.encrypted_password = encrypted_password
        self.config = config
    
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
                    self.encrypted_password
                ),
                look_for_keys=False
            )
        except paramiko.AuthenticationException as err:
            print(f'ssh err on {self.name}: {err}')
            return False
        else:
            # remote_cmd = 'interface print terse'
            # stdin, stdout, stderr = ssh.exec_command(remote_cmd)
            # for line in stdout.readlines():
            #     print(line.strip('\n'))
            # print("Options available to deal with the connectios are many like\n{}".format(dir(ssh)))
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
            check=False
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
