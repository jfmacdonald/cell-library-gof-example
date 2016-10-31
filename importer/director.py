from os             import path
from warnings       import warn
from library        import Library
from .yml_importer  import YmlImporter
from .json_importer import JsonImporter

class ImportDirector:
    '''
    >>> boss = ImportDirector()
    >>> boss.import_from_file('foobar')
    None
    '''

    def __init__(self, lib=None):
        self.__library = lib if isinstance(lib, Library) else Library('imported')

    def import_from_file(self, filename):
        if not path.exists(filename):
            warn("No file "+filename, UserWarning)
            return None
        elif filename[-4:] == '.yml':
            builder = YmlImporter(self.__library)
        elif filename[-5:] == '.json':
            builder = JsonImporter(self.__library)
        else:
            warn("Don't know how to import from "+filename, UserWarning)
            return None
        builder.import_from_file(filename)
        return self.__library

