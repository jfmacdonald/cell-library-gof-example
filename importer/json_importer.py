from os             import path
from warnings       import warn
from json           import load
from .importer      import Importer
from entity         import FileEntity

class JsonImporter(Importer):

    def __init__(self, library):
        super().__init__(library)
        self.__data = {}

    def import_from_file(self, filename):
        if not path.exists(filename):
            warn("No file "+filename, UserWarning)
            return False
        try:
            with open(filename,'r') as f:
                self.__data = load(f)
        except Exception as msg:
            warn("%s: can't read %s" % (msg, filename), UserWarning)
            return False
        if not 'file' in self.__data:
            warn("No files in %s" % (filename))
            return False
        for filetype in self.__data['file']:
            for filekey in self.__data['file'][filetype]:
                entity = self._get_file_entity(filetype, filekey)
                if entity: self._import_file_entity(entity)
        return True

    def _get_file_entity(self, filetype, filekey):
        try:
            doc = self.__data['file'][filetype][filekey]
            basename = doc['name']
            pathkey  = doc['path']
            filetype = doc['type']
            pathname = self.__data['reference']['path'][pathkey]
        except Exception as msg:
            warn("%s: invalid entry file.%s.%s" % (msg, filetype, filekey))
            return None
        filename = path.join(pathname,basename)
        entity   = FileEntity(filename, filetype)
        if 'attribute' in doc:
            for name in doc['attribute']:
                entity.set_attribute( name, doc['attribute'][name])
        if 'cellset' in doc:
            cellset = doc['cellset']
            try:
                cells = self.__data['reference']['cellset'][cellset]
                if isinstance(cells, list):
                    for cellname in cells: entity.set_cell(cellname)
                elif isinstance(cells, str):
                    entity.set_cell(cells)
            except KeyError:
                warn("Invalid cellset entry in file.%s.%s" % (msg, filetype, filekey))
        if 'member' in doc:
            groups = {}
            for group_type in doc['member']:
                group_name = doc['member'][group_type]
                groups.update( self._get_hierarchical_groups( group_type, group_name) )
            for group_type in groups:
                entity.set_group( group_type, groups[group_type])
        return entity

    def _get_hierarchical_groups(self, group_type, group_name):
        dictionary = { group_type: group_name }
        try:
            group = self.__data['group'][group_type][group_name]
            for gpname in group['member']:
                gptype = group['member'][gpname]
                dictionary.update( self._get_hierarchical_groups(gptype, gpname) )
        except Exception:
            pass
        return dictionary

