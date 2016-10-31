'''
A File is a Component leaf.
'''

from .file import File

class LibFile(File):

    def type(self):
        return 'lib'

    def accept(self, visitor):
        if not visitor.visitLibFile(self):
            return False
        parent = self.get_parent()
        if parent: 
            if not parent.accept(visitor): 
                return False
        return True


if __name__ == '__main__':
     pass
