from grouper.group_builder import GroupBuilder

class GroupReBuilder(GroupBuilder):

    def build_cornergroups(self):
        self._clear_groups()
        super().build_cornergroups()

    def _clear_groups(self):
        for group in self.get_library().get_groups():
            members = list(group.get_members())
            for comp in members:
                group.remove(comp)

