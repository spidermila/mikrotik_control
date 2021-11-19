# import io
from pathlib import Path
from typing import List

from libs.script import Script

try:
    import yaml
except(NameError, ModuleNotFoundError):
    import sys
    print('PyYAML is needed for this program.')
    raise ImportError((
        'PyYAML is needed for this program.\n'
        f'Install it: {sys.executable} -m pip install PyYAML',
    ))


class ScriptHandler:
    def __init__(self, filename: str = 'scripts.yaml') -> None:
        self.filename = filename
        self.scripts_from_file: list = []
        self.scripts: List[Script] = []

    def load_scripts(self) -> None:
        if Path(self.filename).is_file():
            with open(self.filename, 'r') as stream:
                try:
                    data = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        else:
            print(f"File {self.filename} doesn't exist.")
            raise
        self.scripts_from_file = data['scripts']

    def instantiate_scripts(self) -> None:
        for entry in self.scripts_from_file:
            self.scripts.append(
                Script(
                    entry['name'],
                    entry['devices'],
                    entry['groups'],
                    entry['scripts'],
                    entry['actions'],
                ),
            )
