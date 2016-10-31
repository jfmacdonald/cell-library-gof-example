'''
A File is a Component leaf.
'''

from .file import File

class GdsFile(File):

    def type(self):
        return 'gds'

    def accept(self, visitor):
        if not visitor.visitGdsFile(self):
            return False
        parent = self.get_parent()
        if parent: 
            if not parent.accept(visitor): 
                return False
        return True

if __name__ == '__main__':
     pass
