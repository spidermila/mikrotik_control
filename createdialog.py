import getpass
from typing import List

from cls import cls
from configuration import Configuration
from device import Device


class CreateDialog:
    def __init__(self, config: Configuration, devices: List[Device]) -> None:
        self.config = config
        self.devices = devices

    def run(self):
        if len(self.config.targets) > 0:
            if not self.config.is_password_correct():
                print("Wrong password. Can't decrypt passwords for the devices.")
                return
        cls()
        print('Name of the new device')
        name = input('>')
        print('Ener IP address')
        address = input('>')
        print('Ener port')
        port = int(input('>'))
        print('Ener user (default: control)')
        user = input('>')
        if len(user) == 0:
            user = 'control'
        print('Ener password')
        device_password = getpass.getpass('>')
        encrypted_password = self.config.password_encrypt(
            bytes(device_password,"utf-8"),
            self.config.password
        )
        record = {
            'name': name,
            'address': address,
            'port': port,
            'user': user,
            'password': encrypted_password,
        }
        self.devices.append(
            Device(
                name,
                address,
                port,
                user,
                encrypted_password,
                self.config
            )
        )
        self.config.targets.append(record)
        self.config.save_cfg_to_file()