from typing import List

from libs.configuration import Configuration
from libs.cprint import cprint
from libs.createdialog import CreateDialog
from libs.device import Device
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

        self.script_menu = ScriptMenu(
            self.config,
            self.devices,
            self.groups,
            self.scripts,
        )

        self.commands = {
            'quit cmnds': ['q', 'quit', 'exit'],
            'help cmnds': ['h', 'help'],
            'list cmnds': ['l', 'list'],
            'create cmnds': ['c'],
            'testall cmnds': ['ta'],
            'device cmnds': ['d'],
            'script cmnds': ['s'],
        }

    def run(self) -> bool:
        if not self.password_verified:
            if not self.config.is_password_correct():
                print(
                    "Wrong password. Can't decrypt passwords for the devices.",
                )
                return False
            else:
                self.password_verified = True

        command_line = input(': ')
        if len(command_line) == 0:
            return True
        command = command_line.lower().split()[0]
        if command in self.commands['quit cmnds']:
            return False
        elif command in self.commands['help cmnds']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        elif command in self.commands['list cmnds']:
            if len(self.config.targets) > 0:
                for target in self.config.targets:
                    print(f'nme: {target["name"]}')
                    print(f'IPa: {target["address"]}')
                    print(f'prt: {target["port"]}')
                    print(f'usr: {target["user"]}')
                    print(f'grp: {target["group"]}')
                    print('-'*20)

        elif command in self.commands['create cmnds']:
            create_dialog = CreateDialog(
                self.config,
                self.devices,
                self.groups,
            )
            create_dialog.run()
        elif command in self.commands['testall cmnds']:
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
        elif command[0] in self.commands['device cmnds']:
            if len(command) > 1:
                if command[1:3] == 'li':
                    if len(command) > 3:
                        if command[3] == 'r':
                            # refresh before listing
                            ...
                    self.devices[1].print_cached_interfaces()
            pass
            # dialog for selecting a device
        elif command[0] in self.commands['script cmnds']:
            while self.script_menu.run():
                ...
        else:
            print('Unknown command')
            print('')
        return True
