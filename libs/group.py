from libs.configuration import Configuration


class Group:
    def __init__(self, name: str, config: Configuration) -> None:
        self.name = name
        self.config = config
