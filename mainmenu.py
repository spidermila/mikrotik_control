from configuration import Configuration
from cprint import cprint
from createdialog import CreateDialog
from device import Device
from typing import Any
from typing import List
from typing import Tuple


class MainMenu:
    def __init__(self, config: Configuration, devices: List[Device]) -> None:
        self.config = config
        self.devices = devices
        self.commands = {
        'quit cmnds': ['q', 'quit', 'exit'],
        'help cmnds': ['h', 'help'],
        'list cmnds': ['l', 'list'],
        'create cmnds': ['c', 'create'],
        'testall cmnds': ['ta'],
    }

    def run(self) -> bool:
        command_line = input(': ')
        if len(command_line) > 0:
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
                            print('-'*20)
                    else:
                        print("Wrong password. Can't decrypt passwords for the devices.")
            elif command in self.commands['create cmnds']:
                create_dialog = CreateDialog(self.config)
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
            else:
                print('Unknown command')
                print('')
        return True