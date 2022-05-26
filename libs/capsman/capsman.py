from libs.capsman.acl import ACL


class Capsman:
    def __init__(self) -> None:
        self.acl = ACL()
        self.status_known: bool = False
        self.enabled: bool = False
