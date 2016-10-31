'''
A CornerGroup is a set of files with attribute 'library' matching other files in the group.
'''

from warnings   import warn
from .group     import Group
from .file      import File

class CornerGroup(Group):

    def type(self):
        return 'cornergroup'

    def add(self, component):
        if not isinstance(component, File):
            return False
        library = component.get_attribute_value('library')
        if not library: 
            return False
        mylibrary = self.get_attribute_value('library')
        if not mylibrary:
            self.set_attribute_value('library', library)
            mylibrary = library
        elif mylibrary != library:
            return False
        self.__add__(component)
        return True

    def accept(self, visitor):
        if not visitor.visitCornerGroup(self):
            return False
        parent = self.get_parent()
        if parent: 
            if not parent.accept(visitor):
                return False
        return True
