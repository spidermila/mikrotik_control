import getpass
from typing import List

from libs.cls import cls
from libs.configuration import Configuration
from libs.device import Device
from libs.devicehandler import DeviceHandler
from libs.group import Group
from libs.grouphandler import GroupHandler
from libs.mainmenu import MainMenu
from libs.script import Script
from libs.scripthandler import ScriptHandler


class Program:
    def __init__(self) -> None:
        self.config = Configuration(getpass.getpass())
        self.config.check_or_create_config_file()
        self.config.load_config()

        self.device_handler = DeviceHandler(self.config)
        self.device_handler.instantiate_devices()

        self.group_handler = GroupHandler(self.config)
        self.group_handler.instantiate_groups()

        self.script_handler = ScriptHandler()
        self.script_handler.load_scripts()
        self.script_handler.instantiate_scripts()

        self.devices: List[Device] = self.device_handler.devices
        self.groups: List[Group] = self.group_handler.groups
        self.scripts: List[Script] = self.script_handler.scripts

    def run(self) -> int:
        main_menu = MainMenu(
            self.config,
            self.devices,
            self.groups,
            self.scripts,
        )

        cls()
        while main_menu.run():
            ...
        return 0
