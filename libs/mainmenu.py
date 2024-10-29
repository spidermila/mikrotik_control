from typing import List

from libs.configuration import Configuration
from libs.device import Device
from libs.devicesmenu import DevicesMenu
from libs.group import Group
from libs.script import Script
from libs.scriptsmenu import ScriptsMenu


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
        self.command_history: list[str] = []

        self.devices_menu = DevicesMenu(
            self.config,
            self.devices,
            self.groups,
            self.scripts,
        )

        self.scripts_menu = ScriptsMenu(
            self.config,
            self.devices,
            self.groups,
            self.scripts,
        )

        self.commands = {
            'quit': ['q', 'quit', 'exit'],
            'help': ['h', 'help'],
            'devices menu': ['d'],
            'scripts menu': ['s'],
        }

    def _print_help(self) -> None:
        for c in self.commands:
            print(f'{c}: {self.commands[c]}')

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

        if len(self.command_history) == 0:
            self._print_help()
        command_line = input(': ')
        self.command_history.append(command_line)
        if len(command_line) == 0:
            return True
        try:
            command = command_line.lower().split()[0]
        except IndexError:
            return True
        if command in self.commands['quit']:
            return False
        elif command in self.commands['help']:
            self._print_help()
        elif command[0] in self.commands['devices menu']:
            while self.devices_menu.run():
                ...
        elif command[0] in self.commands['scripts menu']:
            while self.scripts_menu.run():
                ...
        else:
            print('Unknown command')
            print('')
        return True
