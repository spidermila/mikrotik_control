from typing import List
from typing import Optional

from libs.configuration import Configuration
from libs.cprint import cprint
from libs.createdialog import CreateDialog
from libs.device import Device
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
            'list interfaces': ['li'],
            'create device': ['c'],
            'edit device': ['e'],
            'select device': ['s'],
            'testall devices': ['ta'],
        }

    def run(self) -> bool:
        if not self.selected_device:
            if len(self.devices) == 0:
                return False
            print('Select a device to manage:')
            print('Leave empty to go back.')
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
                for target in self.config.targets:
                    print(f'nme: {target["name"]}')
                    print(f'IPa: {target["address"]}')
                    print(f'prt: {target["port"]}')
                    print(f'usr: {target["user"]}')
                    print(f'grp: {target["group"]}')
                    print('-'*20)
        elif command in self.commands['list interfaces']:
            self.selected_device.print_cached_interfaces()
        elif command in self.commands['create device']:
            create_dialog = CreateDialog(
                self.config,
                self.devices,
                self.groups,
            )
            create_dialog.run()
        elif command in self.commands['edit device']:
            ...
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
