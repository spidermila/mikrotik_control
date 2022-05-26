from typing import List


class ACL:
    def __init__(self) -> None:
        self.items: List[ACL_Item] = []


class ACL_Item:
    def __init__(self) -> None:
        self.comment: str = ''
