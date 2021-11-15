import getpass

from cls import cls
from configuration import Configuration

class Create_Dialog:
    def __init__(self, config: Configuration) -> None:
        self.config = config

    def run(self):
        if len(self.config.targets) > 0:
            if not self.config.is_password_correct(self.config.targets[0]['password']):
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
        record = {
            'name': name,
            'address':address,
            'port':port,
            'user':user,
            'password':f'{self.config.password_encrypt(bytes(device_password,"utf-8"))}',
        }
        self.config['targets'].append(record)
        save_cfg(data)