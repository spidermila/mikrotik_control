# import getpass
# from typing import List
# from typing import Optional
from libs.configuration import Configuration
from libs.device import Device
# from libs.cprint import cprint


class AccesslistMenu:
    def __init__(
        self,
        config: Configuration,
        selected_device: Device,
    ) -> None:
        self.config = config
        self.selected_device = selected_device
        self.commands = {
            'back': ['q'],
            'help': ['h', 'help'],
            'print': ['p'],
        }

    def run(self) -> bool:
        print(f'>{self.selected_device.name}<')
        command_line = input('dev/capsman/acl: ')
        if len(command_line) == 0:
            return True
        command = command_line.lower().split()[0]
        if command in self.commands['back']:
            return False
        elif command in self.commands['help']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        else:
            print('Unknown command')
            print('')
        return True
