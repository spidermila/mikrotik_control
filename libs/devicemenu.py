from typing import List
from typing import Optional

from libs.configuration import Configuration
from libs.cprint import cprint
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
            'quit cmnds': ['q', 'quit', 'exit'],
            'help cmnds': ['h', 'help'],
            'list cmnds': ['l'],
            'create cmnds': ['c'],
            'run cmnds': ['r'],
            'edit cmnds': ['e'],
            'select cmnds': ['s'],
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
        if command in self.commands['quit cmnds']:
            return False
        elif command in self.commands['help cmnds']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        elif command in self.commands['list cmnds']:
            if len(self.scripts) > 0:
                for script in self.scripts:
                    print(f'name   : {script.name}')
                    print(f'devices: {script.devices}')
                    print(f'groups : {script.groups}')
                    print(f'scripts: {script.scripts}')
                    print(f'actions: {script.actions}')
                    print('-'*20)
            else:
                print('No scripts defined.')
        elif command in self.commands['create cmnds']:
            ...
        elif command in self.commands['run cmnds']:
            ...
        elif command in self.commands['edit cmnds']:
            ...
        elif command in self.commands['select cmnds']:
            self.selected_device = None
        else:
            print('Unknown command')
            print('')
        return True
