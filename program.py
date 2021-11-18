import getpass

from cls import cls
from configuration import Configuration
from device import Device
from group import Group
from mainmenu import MainMenu
from typing import List
from typing import Optional

class Program:
    def __init__(self) -> None:
        self.config = Configuration(getpass.getpass())
        self.config.check_or_create_config_file()
        self.config.load_config()
        self.devices: List[Device] = []
        self.groups: List[Group] = []

        self._instantiate_groups()
        self._instantiate_devices()
        

    def run(self) -> int:
        main_menu = MainMenu(
            self.config,
            self.devices,
            self.groups,
        )

        cls()
        while main_menu.run():
            ...
        return 0
    
    def _instantiate_devices(self):
        if len(self.config.targets) == 0:
            return
        for target in self.config.targets:
            self.devices.append(
                Device(
                    target['name'],
                    target['address'],
                    target['port'],
                    target['user'],
                    target['password'],
                    target['group'],
                    self.config
                )
            )

    def _instantiate_groups(self):
        if len(self.config.targets) == 0:
            return
        for target in self.config.targets:
            if not self.group_by_name_exists(
                target['group']
            ):
                self.groups.append(
                    Group(
                        target['group'],
                        self.config
                    )
                )

    def get_group_by_name(self, lookup_name: str) -> Optional[Group]:
        assert self.group_by_name_exists(lookup_name)
        for group in self.groups:
            if group.name == lookup_name:
                return group
        return None
    
    def group_by_name_exists(self, lookup_name: str) -> bool:
        for group in self.groups:
            if group.name == lookup_name:
                return True
        return False