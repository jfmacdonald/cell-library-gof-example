'''
A File is a Component leaf.
'''

from .file import File

class LefFile(File):

    def type(self):
        return 'lef'

    def accept(self, visitor):
        if not visitor.visitLefFile(self):
            return False
        parent = self.get_parent()
        if parent: 
            if not parent.accept(visitor): 
                return False
        return True


if __name__ == '__main__':
     pass
