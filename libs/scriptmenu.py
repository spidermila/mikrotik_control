from typing import List

from libs.configuration import Configuration
from libs.device import Device
from libs.group import Group
from libs.script import Script


class ScriptMenu:
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

        self.commands = {
            'quit': ['q', 'quit', 'exit'],
            'help': ['h', 'help'],
            'list scripts': ['l'],
            'create script': ['c'],
            'run script': ['r'],
            'edit script': ['e'],
        }

    def run(self) -> bool:
        command_line = input('scr: ')
        if len(command_line) == 0:
            return True
        command = command_line.lower().split()[0]
        if command in self.commands['quit']:
            return False
        elif command in self.commands['help']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        elif command in self.commands['list scripts']:
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
        elif command in self.commands['create script']:
            ...
        elif command in self.commands['run script']:
            ...
        elif command in self.commands['edit script']:
            ...
        else:
            print('Unknown command')
            print('')
        return True
