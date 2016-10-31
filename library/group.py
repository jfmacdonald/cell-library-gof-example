'''
A Group is a Component composite.
'''

from abc        import ABCMeta
from .component  import Component

class Group(Component,metaclass=ABCMeta):

    def __init__(self, name):
        super().__init__(name)
        self.__members = set()

    def get_members(self):
        return self.__members

    def remove(self, component):
        if component:
            component.__disjoin__()
            self.__members.discard(component)

    def get_cells(self):
        cells = set()
        for component in self.__members:
            cells |= component.get_cells()
        return cells

    def add_cell(self,cell):
        pass

    def is_file(self):
        return False

    def __add__(self, component):
        component.__join__(self)
        self.__members.add(component)

if __name__ == '__main__':
    pass
