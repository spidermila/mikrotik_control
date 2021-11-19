from device import Device
from typing import List
from typing import Optional
from group import Group

class Script:
    def __init__(
        self,
        name: str,
        devices: Optional[List[Device]],
        groups: Optional[List[Group]],
        scripts: Optional[List],
        actions: List[str]
    ) -> None:
        self.name = name
        self.devices = devices
        self.groups = groups
        self.scripts = scripts
        self.actions = actions
        