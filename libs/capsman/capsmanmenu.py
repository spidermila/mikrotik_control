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
            'back': ['q'],
            'help': ['h', 'help'],
            'access list menu': ['a'],
        }

        self.accesslist_menu = AccesslistMenu(
            self.config,
            self.selected_device,
        )

    def run(self) -> bool:
        print(f'>{self.selected_device.name}<')
        if not self.selected_device.capsman.status_known:
            self.selected_device.get_capsman_manager_status()
        if self.selected_device.capsman.enabled:
            print('CAPsMAN Enabled')
        else:
            print('CAPsMAN Disabled')
        command_line = input('dev/capsman: ')
        if len(command_line) == 0:
            return True
        command = command_line.lower().split()[0]
        if command in self.commands['back']:
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
