import getpass
from typing import List

from cls import cls
from configuration import Configuration
from device import Device
from group import Group


class CreateDialog:
    def __init__(
        self,
        config: Configuration,
        devices: List[Device],
        groups: List[Group],
    ) -> None:
        self.config = config
        self.devices = devices
        self.groups = groups

    def _pick_group_dialog(self) -> Group:
        while True:
            group_chosen = False
            if len(self.groups) == 0:
                print('There are no existing groups.')
            else:
                print('Existing groups:')
                for group in self.groups:
                    print(f'{group.name}')
            print('Enter group')
            new_group_name = input('>')
            found = False
            for group in self.groups:
                if new_group_name == group.name:
                    print(f'Using existing group{group.name}')
                    found = True
                    group_chosen = True
                    chosen_group = group
                    break
            if group_chosen:
                break
            if not found:
                print(f"Group {new_group_name} doesn't exist yet")
                print('Create a new group? (yY/nN/q)')
                while True:
                    answer = input('>')
                    if answer.lower() == 'y':
                        self.groups.append(
                            Group(
                                new_group_name,
                                self.config
                            ),
                        )
                        chosen_group = self.groups[-1]
                        print(f'New group{new_group_name} created.')
                        group_chosen = True
                        break
                    elif answer.lower() == 'n':
                        break
                    elif answer.lower() == 'q':
                        exit(0)
                    else:
                        pass
                if group_chosen:
                    break
        return chosen_group

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
        while True:
            try:
                print('Ener port')
                port = int(input('>'))
            except:
                print('Port must be an integer!')
            else:
                if port > 65_535:
                    print('Port must have a value lower than 65,535!')
                else:
                    break
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
        chosen_group = self._pick_group_dialog()

        record = {
            'name': name,
            'address': address,
            'port': port,
            'user': user,
            'password': encrypted_password,
            'group': chosen_group.name,
        }
        self.devices.append(
            Device(
                name,
                address,
                port,
                user,
                encrypted_password,
                chosen_group,
                self.config
            )
        )
        self.config.targets.append(record)
        self.config.save_cfg_to_file()