class Interface:
    def __init__(
        self,
        number: int,
        name: str,
        disabled: bool,
        running: bool,
        slave: bool,
        dynamic: bool,
        comment: str
    ) -> None:
        self.number = number
        self.name = name
        self.disabled = disabled
        self.running = running
        self.slave = slave
        self.dynamic = dynamic
        self.comment = comment