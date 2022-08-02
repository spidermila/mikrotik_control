from typing import List

from lib.interface import Interface


class DHCPServer:
    def __init__(self) -> None:
        self.items = List[DHCPServerItem]
        self.leases = Leases()


class DHCPServerItem:
    def __init__(
        self,
        number: int,
        name: str,
        interface: Interface,
        address_pool: str,  # implement class later
        lease_time: str,  # implement class later
    ) -> None:
        self.number = number
        self.name = name
        self.interface = interface
        self.address_pool = address_pool
        self.lease_time = lease_time


class Leases:
    def __init__(self) -> None:
        self.items = List[LeasesItem]


class LeasesItem:
    def __init__(self):
        pass
