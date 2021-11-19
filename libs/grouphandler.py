from typing import List
from typing import Optional

from libs.configuration import Configuration
from libs.group import Group


class GroupHandler:
    def __init__(
        self,
        config: Configuration,
    ) -> None:
        self.config = config
        self.groups: List[Group] = []

    def instantiate_groups(self):
        if len(self.config.targets) == 0:
            return
        for target in self.config.targets:
            if not self.group_by_name_exists(
                target['group'],
            ):
                self.groups.append(
                    Group(
                        target['group'],
                        self.config,
                    ),
                )

    def get_group_by_name(self, lookup_name: str) -> Optional[Group]:
        assert self.group_by_name_exists(lookup_name)
        for group in self.groups:
            if group.name == lookup_name:
                return group
        return None

    def group_by_name_exists(self, lookup_name: str) -> bool:
        for group in self.groups:
            if group.name == lookup_name:
                return True
        return False
