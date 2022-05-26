# import getpass
# from typing import List
# from typing import Optional
from libs.capsman.accesslistmenu import AccesslistMenu
from libs.configuration import Configuration
from libs.device import Device
# from libs.cprint import cprint


class CapsmanMenu:
    def __init__(
        self,
        config: Configuration,
        selected_device: Device,
    ) -> None:
        self.config = config
        self.selected_device = selected_device
        self.commands = {
            'quit': ['q', 'quit', 'exit'],
            'help': ['h', 'help'],
            'access list menu': ['l'],
        }

        self.accesslist_menu = AccesslistMenu(
            self.config,
            self.selected_device,
        )

    def run(self) -> bool:
        print(f'>{self.selected_device.name}<')
        self.selected_device.get_capsman_manager_status()
        command_line = input('dev/capsman: ')
        if len(command_line) == 0:
            return True
        command = command_line.lower().split()[0]
        if command in self.commands['quit']:
            return False
        elif command in self.commands['help']:
            for c in self.commands:
                print(f'{c}: {self.commands[c]}')
        elif command[0] in self.commands['access list menu']:
            while self.accesslist_menu.run():
                ...
        else:
            print('Unknown command')
            print('')
        return True
