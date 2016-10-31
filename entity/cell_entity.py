from .entity import Entity, Dictionary
import os.path as path
import re

class CellEntity(Entity):
    '''
    entity:     cell
    cellname:   <<unique cell name>>
    attributes: <<attribute dictionary>>
    pins:       <<pin dictionary>>
    '''

    def __init__(self, cellname):
        self.__entity = Dictionary( { 
            'entity':       'cell',
            'attributes':   {},
            'pins':         {},
            } )
        self.__entity.cellname = cellname

    # cell name
    def get_cellname(self):
        return self.__entity.cellname

    # attribute interface
    # -- intrinsic attributes
    def get_attribute_names(self):
        return sorted(self.__entity.attributes.keys())

    def get_attribute_value(self, name):
        if name in self.__entity.attributes:
            return self.__entity.attributes[name]
        else:
            return None

    def set_attribute_value(self, name, value):
        self.__entity.attributes[name] = value
        return self

    # pin interface
    # -- a cell may have only one pin with a given name
    def get_pin_names(self):
        return sorted(self.__entity.pins.keys())

    def get_pin_attributes(self, name):
        if name in self.__entity.pins:
            return self.__entity.pins[name]
        else:
            return None

    def set_pin(self, name, attributes={}):
        if not isinstance( attributes, dict):
            return None
        self.__entity.pins[name] = attributes
        return self

    def set_pin_attribute(self, name, attribute_name, attribute_value):
        if name in self.__entity.pins:
            self.__entity.pins[name][attribute_name] = attribute_value
            return self
        else:
            return None

    # implement Entity abstractmethod
    def _dictionary(self):
        return self.__entity

if __name__ == '__main__':
    fe = CellEntity('test.lef')
    fe.set_attribute_value('VERSION', '5.7')
    fe.set_cell('nd2')
    fe.set_cell('an2')
    fe.set_cell('mx2')
    fe.set_group('stdcell', 'tsmc35u')
    print('\n')
    print('YAML')
    print(fe.get_yaml())
    print('JSON')
    print(fe.get_json())

