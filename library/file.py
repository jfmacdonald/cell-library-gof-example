'''
A File is a Component leaf.
'''
from abc import ABCMeta
from .component import Component

class File(Component,metaclass=ABCMeta):

    def __init__(self, name):
        super().__init__(name)
        self.__cells = set()
    
    def get_members(self):
        return set()

    def get_cells(self):
        return self.__cells

    def add_cell(self, cell):
        self.__cells.add(cell)

    def add(self, component):
        pass

    def remove(self, component):
        pass

if __name__ == '__main__':
    pass
