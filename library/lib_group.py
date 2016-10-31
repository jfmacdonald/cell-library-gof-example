'''
A LibGroup is defined as the set of timing model files with intersecting cell sets.
These files all have an attribute 'library', a string with format "libgroup_name_corner_name".
'''

from warnings       import warn
from .group         import Group
from .corner_group  import CornerGroup
from .lib_file      import LibFile
from .ctl_file      import CtlFile
from .db_file       import DbFile

ok_type = (LibFile, CtlFile, DbFile, CornerGroup)

class LibGroup(Group):

    def type(self):
        return 'libgroup'

    def add(self, component):
        if not isinstance(component, ok_type):
            warn("Can not add %s to a libgroup" % repr(component), RuntimeWarning)
        else:
            self.__add__(component)

    def accept(self, visitor):
        if not visitor.visitLibGroup(self):
            return False
        parent = self.get_parent()
        if parent: 
            if not parent.accept(visitor): 
                return False
        return True

if __name__ == '__main__':
    pass
