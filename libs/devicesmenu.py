import getpass
from typing import List
from typing import Optional

from libs.configuration import Configuration
from libs.cprint import cprint
from libs.device import Device
from libs.devicecreatedialog import DeviceCreateDialog
from libs.group import Group
from libs.script import Script


class DevicesMenu:
    def __init__(
        self,
        config: Configuration,
        devices: List[Device],
        groups: List[Group],
        scripts: List[Script],
    ) -> None:
        self.config = config
        self.devices = devices
        self.groups = groups
        self.scripts = scripts
        self.selected_device: Optional[Device] = None
        self.commands = {
            'back': ['q'],
            'help': ['h', 'help'],
            'list details of all devices': ['l'],
            'test connection to all devices': ['tc'],
            'create device': ['c'],
            'refresh devices': ['r'],
            'sort devices': ['s'],
        }

    def run(self) -> bool:
        if len(self.devices) == 0:
            print('There are no devices defined.')
            print('Add a new device?')
            #  TODO: add new device dialog
            return False

        devices_with_idx = []
        indexes = []
        for idx, device in enumerate(self.devices):
            devices_with_idx.append((
                idx,
                f': {device.group}',
                f': {device.name}',
                f': {device.os_version}',
            ))
            indexes.append(idx)

        command_line = input('devices > ')
        if len(command_line) == 0:
            cprint(devices_with_idx)
            return True
        try:
            command = command_line.lower().split()[0]
        except IndexError:
            return True

        if command.isnumeric():
            intcommand = int(command)
            if intcommand in indexes:
                #  TODO: run device menu here
                print('run device menu here')
            else:
                print(
                    'Pick a number from the list of devices or use a command.',
                )
        if command in self.commands['back']:
            return False
        elif command in self.commands['help']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        elif command in self.commands['list details of all devices']:
            if len(self.config.targets) > 0:
                for device in self.devices:
                    print(f'nme: {device.name}')
                    print(f'IPa: {device.address}')
                    print(f'prt: {device.port}')
                    print(f'usr: {device.user}')
                    print(f'grp: {device.group}')
                    print('-'*20)
        elif command in self.commands['create device']:
            device_create_dialog = DeviceCreateDialog(
                self.config,
                self.devices,
                self.groups,
            )
            device_create_dialog.run()
        elif command in self.commands['refresh devices']:
            for device in self.devices:
                device.get_os_version()
        elif command in self.commands['sort devices']:
            self.devices = sorted(
                self.devices,
                key=lambda x: x.group.name, reverse=True,
            )
            self.generate_targets_from_devices()
            self.config.save_cfg_to_file()
        elif command in self.commands['test connection to all devices']:
            print('Testing...')
            output = []
            for device in self.devices:
                ping_result, ssh_result = device.test_connection()
                if ping_result:
                    if ssh_result:
                        output.append((
                            device.name,
                            ': ping ok',
                            ': ssh ok',
                        ))
                    else:
                        output.append((
                            device.name,
                            ': ping ok',
                            ': ssh KO!',
                        ))
                else:
                    if ssh_result:
                        output.append((
                            device.name,
                            ': ping KO!',
                            ': ssh: ok',
                        ))
                    else:
                        output.append((
                            device.name,
                            ': ping KO!',
                            ': ssh: KO!',
                        ))
            print('result:')
            print('-'*15)
            cprint(output)
        else:
            print('Unknown command')
            print('')
        return True

    def edit_dialog(self, device: Device) -> None:
        print(f'Name: {device.name}')
        print('Leave blank to keep')
        new_name = input('> ')
        if new_name != '':
            device.name = new_name

        print(f'IP: {device.address}')
        print('Leave blank to keep')
        new_address = input('> ')
        if new_address != '':
            device.address = new_address

        while True:
            print(f'Port: {device.port}')
            print('Leave blank to keep')
            new_port = input('> ')
            if new_port != '':
                try:
                    device.port = int(new_port)
                except ValueError:
                    print('Port must be an int number')
                else:
                    break
            else:
                break

        print(f'User: {device.user}')
        print('Leave blank to keep')
        new_user = input('> ')
        if new_user != '':
            device.user = new_user

        print('Password:')
        print('Leave blank to keep')
        new_password = getpass.getpass('> ')
        if new_password != '':
            device.encrypted_password = self.config.password_encrypt(
                bytes(new_password, 'utf-8'),
                self.config.password,
            )
        self.generate_targets_from_devices()
        self.config.save_cfg_to_file()

    def generate_targets_from_devices(self) -> None:
        self.config.targets = []
        for device in self.devices:
            record = {
                'name': device.name,
                'address': device.address,
                'port': device.port,
                'user': device.user,
                'password': device.encrypted_password,
                'group': device.group,
            }
            self.config.targets.append(record)
