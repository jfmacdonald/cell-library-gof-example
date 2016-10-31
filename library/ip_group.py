'''
An IpGroup is a set of files with interesecting cell sets.
'''

from warnings   import warn
from .group      import Group

class IpGroup(Group):

    def type(self):
        return 'ipgroup'

    def add(self, component):
        if isinstance(component, IpGroup):
            warn("Can not add %s to an ipgroup" % repr(component), RuntimeWarning)
        else:
            self.__add__(component)

    def accept(self, visitor):
        if not visitor.visitIpGroup(self):
            return False
        parent = self.get_parent()
        if parent: 
            if not parent.accept(visitor): 
                return False
        return True

if __name__ == '__main__':
    pass
