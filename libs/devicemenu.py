import getpass
from typing import List
from typing import Optional

from libs.configuration import Configuration
from libs.cprint import cprint
from libs.device import Device
from libs.devicecreatedialog import DeviceCreateDialog
from libs.group import Group
from libs.script import Script


class DeviceMenu:
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
            'quit': ['q', 'quit', 'exit'],
            'help': ['h', 'help'],
            'list all devices': ['l'],
            'testall devices': ['ta'],
            'create device': ['c'],
            'edit device': ['e'],
            'select device': ['s'],
            'list interfaces': ['li'],
        }

    def run(self) -> bool:
        if not self.selected_device:
            if len(self.devices) == 0:
                return False
            print('Select a device to manage:')
            print('Leave empty to go back to main menu.')
            devices_with_idx = []
            indexes = []
            for idx, device in enumerate(self.devices):
                devices_with_idx.append((idx, f': {device.name}'))
                indexes.append(idx)
            cprint(devices_with_idx)
            while True:
                answer = input('> ')
                if len(answer) == 0:
                    return False
                try:
                    intanswer = int(answer)
                except ValueError:
                    print('Pick a number.')
                else:
                    if intanswer in indexes:
                        self.selected_device = self.devices[intanswer]
                        break
                    else:
                        print('Pick a number from the list of devices.')
        print(f'>{self.selected_device.name}<')
        command_line = input('dev: ')
        if len(command_line) == 0:
            return True
        command = command_line.lower().split()[0]
        if command in self.commands['quit']:
            return False
        elif command in self.commands['help']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        elif command in self.commands['list all devices']:
            if len(self.config.targets) > 0:
                for device in self.devices:
                    print(f'nme: {device.name}')
                    print(f'IPa: {device.address}')
                    print(f'prt: {device.port}')
                    print(f'usr: {device.user}')
                    print(f'grp: {device.group}')
                    print('-'*20)
        elif command in self.commands['list interfaces']:
            self.selected_device.print_cached_interfaces()
        elif command in self.commands['create device']:
            device_create_dialog = DeviceCreateDialog(
                self.config,
                self.devices,
                self.groups,
            )
            device_create_dialog.run()
        elif command in self.commands['edit device']:
            self.edit_dialog(self.selected_device)
        elif command in self.commands['select device']:
            self.selected_device = None
        elif command in self.commands['testall devices']:
            print('Testing...')
            output = []
            for device in self.devices:
                if device.test_connection():
                    output.append((device.name, ': ok'))
                else:
                    output.append((device.name, ': KO!'))
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
