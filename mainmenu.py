from configuration import Configuration
from cprint import cprint
from createdialog import CreateDialog
from device import Device
from group import Group
from typing import List


class MainMenu:
    def __init__(
        self,
        config: Configuration,
        devices: List[Device],
        groups: List[Group],
    ) -> None:
        self.config = config
        self.devices = devices
        self.groups = groups
        
        self.commands = {
        'quit cmnds': ['q', 'quit', 'exit'],
        'help cmnds': ['h', 'help'],
        'list cmnds': ['l', 'list'],
        'create cmnds': ['c'],
        'testall cmnds': ['ta'],
        'device cmnds': ['d'],
    }

    def run(self) -> bool:
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
                if self.config.is_password_correct():
                    for target in self.config.targets:
                        print(f'nme: {target["name"]}')
                        print(f'IPa: {target["address"]}')
                        print(f'prt: {target["port"]}')
                        print(f'usr: {target["user"]}')
                        print(f'grp: {target["group"]}')
                        print('-'*20)
                else:
                    print("Wrong password. Can't decrypt passwords for the devices.")
        elif command in self.commands['create cmnds']:
            create_dialog = CreateDialog(
                self.config,
                self.devices,
                self.groups
            )
            create_dialog.run()
        elif command in self.commands['testall cmnds']:
            if self.config.is_password_correct():
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
                print("Wrong password. Can't decrypt passwords for the devices.")
        elif command[0] in self.commands['device cmnds']:
            if self.config.is_password_correct():
                if len(command) > 1:
                    if command[1:3] == 'li':
                        if len(command) > 3:
                            if command[3] == 'r':
                                # refresh before listing
                                ...
                        self.devices[1].print_cached_interfaces()
                pass
                # dialog for selecting a device
        else:
            print('Unknown command')
            print('')
        return True