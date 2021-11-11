import io
import secrets
import getpass

try:
    import yaml
except(NameError, ModuleNotFoundError):
    import sys
    print('PyYAML is needed for this game.')
    raise ImportError(f'PyYAML is needed for this game.\nInstall it: {sys.executable} -m pip install PyYAML')

from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from os import system
from pathlib import Path
from sys import platform


def cls() -> None:
    if platform.find('linux') != -1:
        cls_command = 'clear'
    elif platform.find('win') != -1:
        cls_command = 'cls'
    elif platform.find('darwin') != -1:
        cls_command = 'clear'
    else:
        print('Unknown OS. cls will not work!')
        cls_command = False # type: ignore
    if cls_command: system(cls_command)


def save_cfg(data, filename: str = 'cfg.yaml') -> None:
    with io.open(filename, 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)


def load_cfg(filename: str = 'cfg.yaml') -> dict:
    if Path(filename).is_file():
        with open(filename, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    else:
        print(f"File {filename} doesn't exist.")
        # TODO generate a map or something...
        exit()
    return data


def _derive_key(password: bytes, salt: bytes, iterations: int = 100_000) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=default_backend())
    return b64e(kdf.derive(password))


def password_encrypt(message: bytes, password: str, iterations: int = 100_000) -> str:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    ).decode('utf-8')


def password_decrypt(token: bytes, password: str) -> str:
    try:
        decoded = b64d(token)
        salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(iter, 'big')
        key = _derive_key(password.encode(), salt, iterations)
        return Fernet(key).decrypt(token).decode('utf-8')
    except:
        return 'Invalid password'


def is_password_correct(token: bytes, password: str) -> bool:
    try:
        decoded = b64d(token)
        salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
        iterations = int.from_bytes(iter, 'big')
        key = _derive_key(password.encode(), salt, iterations)
        Fernet(key).decrypt(token).decode('utf-8')
    except:
        return False
    return True


def create_dialog(password: str) -> None:
    data = load_cfg()
    if len(data['targets']) > 0:
        if not is_password_correct(data['targets'][0]['password'], password):
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
        'password':f'{password_encrypt(bytes(device_password,"utf-8"),password)}',
    }
    data['targets'].append(record)
    save_cfg(data)


def main() -> int:
    password = getpass.getpass()

    commands = {
        'quit cmnds': ['q', 'quit', 'exit'],
        'help cmnds': ['h', 'help'],
        'list cmnds': ['l', 'list'],
        'create cmnds': ['c', 'create'],
    }

    # TODO: zkontrolovat, jestli existuje cfg.yaml
    # TODO: zkontrolovat, jestli ma cfg.yaml minimalni interni strukturu
    
    '''\
    data = {
        'targets':
        [
            {
                'name': 'Router 3011',
                'address':'192.168.111.1',
                'port':22,
                'user':'control',
                'password':f'{password_encrypt(bytes("heslo.pro.Control","utf-8"),password)}',
            },
            {
                'name':'AP Obyvak',
                'address':'192.168.111.111',
                'port':22,
                'user':'control',
                'password':f'{password_encrypt(bytes("heslo.pro.Control","utf-8"),password)}',
            },
        ],
        'neco':'neco dalsiho',
    }

    save_cfg(data)
    '''

    cls()
    while True:
        command_line = input(': ')
        if len(command_line) > 0:
            command = command_line.lower().split()[0]
            if command in commands['quit cmnds']:
                return 0
            elif command in commands['help cmnds']:
                for c in commands:
                    print(f'{c}: {commands[c]}')
            elif command in commands['list cmnds']:
                data = load_cfg()
                if len(data['targets']) > 0:
                    if is_password_correct(data['targets'][0]['password'], password):
                        for device in data['targets']:
                            print(f'nme: {device["name"]}')
                            print(f'IPa: {device["address"]}')
                            print(f'prt: {device["port"]}')
                            print(f'usr: {device["user"]}')
                            print('-'*20)
                    else:
                        print("Wrong password. Can't decrypt passwords for the devices.")
            elif command in commands['create cmnds']:
                create_dialog(password)
            else:
                print('Unknown command')
                print('')

if __name__ == '__main__':
    raise SystemExit(main())