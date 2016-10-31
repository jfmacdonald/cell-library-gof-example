from os             import path
from .component     import Component
from .file          import File
from .group         import Group
from .lef_file      import LefFile
from .lib_file      import LibFile
from .db_file       import DbFile
from .gds_file      import GdsFile
from .corner_group  import CornerGroup
from .lib_group     import LibGroup
from .ip_group      import IpGroup

class Library:

    def __init__(self, name):
        self.__name         = name
        self.__components   = set()
        self.__iter         = iter(self.__components)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_files(self, file_type=''):
        files = { c for c in self.__components if isinstance(c,File) }
        if file_type:
            return { c for c in files if c.type() == file_type }
        else:
            return files

    def get_file(self, file_name, file_type):
        for f in self.get_files(file_type):
            if f.name() == path.abspath(file_name): 
                return f
        return None

    def get_groups(self, group_type=''):
        groups = { c for c in self.__components if isinstance(c,Group) }
        if group_type:
            return { c for c in groups if c.type() == group_type }
        else:
            return groups

    def get_group(self, group_name, group_type):
        for g in self.get_groups(group_type):
            if g.name() == group_name:
                return g
        return None

    def add_component(self, component):
        self.__components.add(component)

    def __iter__(self):
        self.__iter = iter(self.__components)
        return self.__iter

    def __next__(self):
        return self.__iter.__next__()

