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
        try:
            command = command_line.lower().split()[0]
        except IndexError:
            return True
        if command in self.commands['back']:
            return False
        elif command in self.commands['help']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        elif command in self.commands['print']:
            self.selected_device.get_capsman_acl()
            for item in self.selected_device.capsman.acl.items:
                print(
                    f'{item.number} |' +
                    f'{item.macaddress} |' +
                    f'{item.comment} |' +
                    f'{item.interface} |' +
                    f'{item.action}',
                )
        else:
            print('Unknown command')
            print('')
        return True
