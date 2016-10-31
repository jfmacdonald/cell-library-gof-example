from abc            import ABCMeta, abstractmethod
from os             import path
from warnings       import warn
from library        import *

class Importer(metaclass=ABCMeta):

    def __init__(self, library):
        self.__library  = library
        self.__imported = set()

    @abstractmethod
    def import_from_file(self, filename):
        pass

    def _add_imported(self, component):
        self.__imported.add(component)

    def _get_imported(self):
        return self.__imported

    def _import_file_entity(self, file_entity):
        filename = file_entity.get_filename()
        filetype = file_entity.get_filetype()
        try:
            assert filetype, "No filetype for " + filename
            classname   = filetype.capitalize() + 'File'
            file        = eval(classname)(filename)
        except Exception as msg:
            warn("File type '%s' not supported: %s" % (filetype, msg))
            return False
        for name in file_entity.get_attribute_names():
            file.set_attribute_value( name, file_entity.get_attribute_value(name))
        for name in file_entity.get_cell_names():
            file.add_cell(name)
        self.__library.add_component(file)
        groups = []
        hierarchy_types     = ['CornerGroup', 'LibGroup', 'IpGroup']
        for group_type in hierarchy_types:
            group_name = file_entity.get_group_name(group_type.lower())
            if not group_name: continue
            group = self.__library.get_group(group_name, group_type.lower())
            if not group:
                group = eval(group_type)(group_name)
                self.__library.add_component(group)
            groups.append(group)
        if groups:
            groups.reverse()
            group = groups.pop()
            group.add(file)
            while groups:
                if group.get_parent(): break
                next_group = groups.pop()
                next_group.add(group)
                group = next_group
        return True

