'''
A Component is a file or a group of files containing models for a set of cells.
Every component supports the method 'get_cells'.
'''

from abc        import ABCMeta, abstractmethod
from os.path    import exists, abspath
from warnings   import warn

class Component(metaclass=ABCMeta):

    def __init__(self, name):
        if exists(name):
            self.__name     = abspath(name)
        else:
            self.__name     = name
        self.__parent       = None
        self.__attribute    = {}

    def name(self):
        return self.__name

    def get_attribute_names(self):
        return sorted( self.__attribute.keys() )

    def get_attribute_value(self, name):
        if name in self.__attribute:
            return self.__attribute[name]
        else:
            return None

    def get_parent(self):
        return self.__parent

    def get_hierarchy(self):
        groups = []
        parent = self.get_parent()
        if not parent:
            return groups
        groups.append(parent)
        groups.extend(parent.get_hierarchy())
        return groups

    def set_attribute_value(self, name, value):
        self.__attribute[name] = value

    def is_file(self):
        return True

    @abstractmethod
    def type(self):
        'file or group type'
        pass

    @abstractmethod
    def get_members(self):
        pass

    @abstractmethod
    def add(self, component):
        'add component to group membership'
        pass

    @abstractmethod
    def remove(self, component):
        'remove component from group membership'
        pass

    @abstractmethod
    def get_cells(self):
        pass

    @abstractmethod
    def add_cell(self, cell):
        pass

    @abstractmethod
    def accept(self, visitor):
        'accept a visitor'
        pass

    def __join__(self, group):
        'join a group'
        if group.is_file():
            warn("Can't join a file (%s)" % group.name(), RuntimeWarning)
        else: 
            if self.__parent: 
                #print("leaving group %s" % self.__parent.name())
                group.remove(self.__parent)
            self.__parent = group

    def __disjoin__(self):
        'leave parent group'
        self.__parent = None

    def __str__(self):
        return '%s::%s' % (self.type(), self.name())

    def __hash__(self):
        'enable set operations'
        return hash( str(type(self)) + str(self) )

if __name__ == '__main__':
    pass
