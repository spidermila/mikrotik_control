from typing import List

from libs.configuration import Configuration
from libs.device import Device


class DeviceHandler:
    def __init__(
        self,
        config: Configuration,
    ) -> None:
        self.config = config
        self.devices: List[Device] = []

    def instantiate_devices(self):
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
                    self.config,
                ),
            )
