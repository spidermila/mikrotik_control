from typing import List

from libs.configuration import Configuration
from libs.device import Device
from libs.devicemenu import DeviceMenu
from libs.group import Group
from libs.script import Script
from libs.scriptmenu import ScriptMenu


class MainMenu:
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
        self.password_verified = False

        self.device_menu = DeviceMenu(
            self.config,
            self.devices,
            self.groups,
            self.scripts,
        )

        self.script_menu = ScriptMenu(
            self.config,
            self.devices,
            self.groups,
            self.scripts,
        )

        self.commands = {
            'quit': ['q', 'quit', 'exit'],
            'help': ['h', 'help'],
            'device menu': ['d'],
            'script menu': ['s'],
        }

    def run(self) -> bool:
        if not self.password_verified:
            if not self.config.is_password_correct():
                print(
                    'Wrong password. '
                    "Can't decrypt passwords for the devices.\n"
                    "If you've lost your password, "
                    'create a new configuration file '
                    'and start over.',
                )
                return False
            else:
                self.password_verified = True

        command_line = input(': ')
        if len(command_line) == 0:
            return True
        command = command_line.lower().split()[0]
        if command in self.commands['quit']:
            return False
        elif command in self.commands['help']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        elif command[0] in self.commands['device menu']:
            while self.device_menu.run():
                ...
        elif command[0] in self.commands['script menu']:
            while self.script_menu.run():
                ...
        else:
            print('Unknown command')
            print('')
        return True
