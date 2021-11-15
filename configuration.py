import io
import secrets

try:
    import yaml
except(NameError, ModuleNotFoundError):
    import sys
    print('PyYAML is needed for this game.')
    raise ImportError(f'PyYAML is needed for this game.\nInstall it: {sys.executable} -m pip install PyYAML')

from base64 import urlsafe_b64encode as b64e
from base64 import urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pathlib import Path

class Configuration:
    def __init__(self, password: str, filename: str = 'cfg.yaml') -> None:
        self.password = password
        self.filename = filename

    def save_cfg(self, data) -> None:
        with io.open(self.filename, 'w', encoding='utf8') as outfile:
            yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

    def _derive_key(
            self,
            password: bytes,
            salt: bytes,
            iterations: int = 100_000
        ) -> bytes:
        """Derive a secret key from a given password and salt"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=salt,
            iterations=iterations, backend=default_backend())
        return b64e(kdf.derive(password))

    def password_encrypt(
            self,
            message: bytes,
            password: str,
            iterations: int = 100_000
        ) -> str:
        salt = secrets.token_bytes(16)
        key = self._derive_key(password.encode(), salt, iterations)
        return b64e(
            b'%b%b%b' % (
                salt,
                iterations.to_bytes(4, 'big'),
                b64d(Fernet(key).encrypt(message)),
            )
        ).decode('utf-8')

    def password_decrypt(self, token: bytes) -> str:
        try:
            decoded = b64d(token)
            salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
            iterations = int.from_bytes(iter, 'big')
            key = self. _derive_key(self.password.encode(), salt, iterations)
            return Fernet(key).decrypt(token).decode('utf-8')
        except:
            return 'Invalid password'

    def is_password_correct(self, token: bytes) -> bool:
        try:
            decoded = b64d(token)
            salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
            iterations = int.from_bytes(iter, 'big')
            key = self._derive_key(self.password.encode(), salt, iterations)
            Fernet(key).decrypt(token).decode('utf-8')
        except:
            return False
        return True

    def load_config(self) -> None:
        if Path(self.filename).is_file():
            with open(self.filename, 'r') as stream:
                try:
                    data = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        else:
            print(f"File {self.filename} doesn't exist.")
            raise
        self.targets = data['targets']

    def check_or_create_config_file(self) -> None:
        if Path(self.filename).is_file():
            file_has_data = False
            with open(self.filename, 'r') as stream:
                try:
                    data = yaml.safe_load(stream)
                    file_has_data = True
                except yaml.YAMLError as exc:
                    file_has_data = False
                    # print(exc)
            if file_has_data:
                if isinstance(data, dict):
                    if not 'targets' in data.keys():
                        data['targets'] = []
                    else:
                        if isinstance(data['targets'], list):
                            all_are_dct = True
                            for target in data['targets']:
                                if not isinstance(target, dict):
                                    all_are_dct = False
                            if not all_are_dct:
                                print(
                                    "cfg file error: some of the targets are/is not a dict"
                                )
                                return
                        else:
                            print("cfg file error: targets are not a list")
                            return
                    # more keys will follow here
                    # more ifs'
                else:
                    print(f"Wrong format of {self.filename}. "+
                        "Expected dict as the main object.")
                    raise
            else:
                ...
                # create structure
        else:
            ...
            # create file and basic structure


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