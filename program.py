import getpass

from cls import cls
from configuration import Configuration
from device import Device
from mainmenu import MainMenu
from typing import List

class Program:
    def __init__(self) -> None:
        self.config = Configuration(getpass.getpass())
        self.config.check_or_create_config_file()
        self.config.load_config()
        self.devices: List[Device] = []

        self._instantiate_devices()

    def run(self) -> int:
        main_menu = MainMenu(self.config, self.devices)

        cls()
        while main_menu.run():
            ...
        return 0
    
    def _instantiate_devices(self):
        if len(self.config.targets) == 0:
            return
        for target in self.config.targets:
            ...