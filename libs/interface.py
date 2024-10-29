from time import monotonic


class Interface:
    def __init__(
        self,
        number: int,
        name: str,
        disabled: bool,
        running: bool,
        slave: bool,
        dynamic: bool,
        comment: str,
    ) -> None:
        self.number = number
        self.name = name
        self.disabled = disabled
        self.running = running
        self.slave = slave
        self.dynamic = dynamic
        self.comment = comment
        self.time_since_last_update: int | None = None

    def _set_time_since_last_update_now(self):
        current_time = int(monotonic())
        self.time_of_last_update = current_time

    def enought_time_passed(self, timeout: int = 20) -> bool:
        current_time = int(monotonic())
        if not self.time_of_last_update:
            self.time_of_last_update = current_time
            return True
        if current_time - self.time_of_last_update > timeout:
            self._set_time_since_last_update_now()
            return True
        return False
