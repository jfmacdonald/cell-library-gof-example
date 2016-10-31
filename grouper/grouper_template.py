

from abc                    import ABCMeta, abstractmethod
from library                import *

class GrouperTemplate(metaclass=ABCMeta):

    count = 0

    def __init__(self, library):
        self.__library = library

    def get_library(self):
        return self.__library

    def build_groups(self):
        self.build_cornergroups()
        self.build_libgroups()
        self.build_ipgroups()

    @abstractmethod
    def build_cornergroups(self):
        pass

    @abstractmethod
    def build_libgroups(self):
        pass

    @abstractmethod
    def build_ipgroups(self):
        pass

    @classmethod
    def count(cls):
        cls.count += 1
        return cls.count

    @classmethod
    def digest(cls, arg):
        from hashlib import md5 
        digest_string = str(arg)
        return md5(digest_string.encode('utf-8')).hexdigest()

    @classmethod
    def prefix(cls, names):
        if not len(names): return  ''
        prefix  = names.pop()
        if not len(names): return prefix
        for name in names:
            l = min([len(name),len(prefix)])
            for n in range(l):
                if name[n] != prefix[n]:
                    prefix = prefix[:n]
                    break
        return prefix

