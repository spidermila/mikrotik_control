from typing import List


class ACL:
    def __init__(self) -> None:
        self.items: List[ACLItem] = []

    def additem(
            self,
            number: int,
            comment: str,
            macaddress: str,
            interface: str,
            action: str,
    ):
        self.items.append(
            ACLItem(
                number,
                comment,
                macaddress,
                interface,
                action,
            ),
        )


class ACLItem:
    def __init__(
        self,
        number: int = -1,
        comment: str = '',
        macaddress: str = '',
        interface: str = '',
        action: str = '',
    ) -> None:
        self.number = number
        self.comment = comment
        self.macaddress = macaddress
        self.interface = interface
        self.action = action
