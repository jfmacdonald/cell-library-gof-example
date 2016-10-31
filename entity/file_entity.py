from   .entity import Entity, Dictionary
import os.path as path
import re

class FileEntity(Entity):
    '''
    entity:     file
    filename:   <<normalized, absolute file path>>
    filetype:   <<file type in { LEF, GDS, LIB, . . .}>>
    attributes: <<attribute dictionary>>
    cells:      <<cell entity dictionary>>
    groups:     <<group membership dictionary>>
    '''

    def __init__(self, filename, filetype=None):
        self.__entity = Dictionary( { 
            'entity':       'file',
            'attributes':   {},
            'cells':        {},
            'groups':       {},
            } )
        self.__entity.filename = path.abspath(filename)
        if not filetype:
            (root, ext) = path.splitext(filename)
            filetype = ext.lstrip('.')
        self.__entity.filetype = filetype.upper()

    # file name, type are read only
    def get_filename(self):
        return self.__entity.filename

    def get_filetype(self):
        return self.__entity.filetype

    # attribute interface
    # -- intrinsic file attributes
    def get_attribute_names(self):
        return sorted(self.__entity.attributes.keys())

    def get_attribute_value(self, name):
        if name in self.__entity.attributes:
            return self.__entity.attributes[name]
        else:
            return None

    def set_attribute(self, name, value):
        self.__entity.attributes[name] = value
        return self

    # cell interface
    # -- a file may have only one cell with a given name
    def get_cell_names(self):
        return sorted(self.__entity.cells.keys())

    def get_cell_entity(self, name):
        if name in self.__entity.cells:
            return self.__entity.cells[name]
        else:
            return None

    def set_cell(self, name, cell_entity={}):
        self.__entity.cells[name] = cell_entity
        return self

    # group membership interface
    # -- a file may be a member of only one group of a given type
    def get_group_types(self):
        return sorted(self.__entity.groups.keys())

    def get_group_name(self, group_type):
        if group_type in self.__entity.groups:
            return self.__entity.groups[group_type]
        else:
            return None

    def set_group(self, group_type, group_name):
        self.__entity.groups[group_type] = group_name

    # implement Entity abstractmethod
    def _dictionary(self):
        return self.__entity

if __name__ == '__main__':
    fe = FileEntity('test.lef')
    fe.set_attribute('VERSION', '5.7')
    fe.set_cell('nd2')
    fe.set_cell('an2')
    fe.set_cell('mx2')
    fe.set_group('stdcell', 'tsmc35u')
    print('\n')
    print('YAML')
    print(fe.get_yaml())
    print('JSON')
    print(fe.get_json())

