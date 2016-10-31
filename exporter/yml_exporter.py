from warnings       import warn
from yaml           import load_all
from os             import path
from .exporter      import Exporter
from library        import *
from entity         import FileEntity

class YmlExporter(Exporter):

    def __init__(self, library):
        super().__init__(library)
        self.__stream = None
        self.__ok     = False

    def export_to_file(self, stream):
        if not stream or stream.closed:
            return False
        self.__ok       = True
        self.__stream   = stream
        for component in self.get_library():
            if not component.accept(self): 
                self.__ok = False
        self.__stream.close()
        return self.__ok

    def visitDbFile(self, file):
        entity = self._file_entity(file)
        return self._export(entity)

    def visitCtlFile(self, file):
        entity = self._file_entity(file)
        return self._export(entity)

    def visitGdsFile(self, file):
        entity = self._file_entity(file)
        return self._export(entity)

    def visitLefFile(self, file):
        entity = self._file_entity(file)
        return self._export(entity)

    def visitLibFile(self, file):
        entity = self._file_entity(file)
        return self._export(entity)

    def visitLibGroup(self, group):
        return True

    def visitCornerGroup(self, group):
        return True

    def visitIpGroup(self, group):
        return True

    def _file_entity(self, file):
        filename    = file.name()
        filetype    = file.type()
        entity      = FileEntity(filename, filetype)
        for name in file.get_attribute_names():
            entity.set_attribute( name, file.get_attribute_value(name))
        for cell in file.get_cells():
            entity.set_cell(str(cell))
        for group in file.get_hierarchy():
            entity.set_group( group.type(), group.name() )
        return entity
    
    def _export(self, file_entity):
        try: 
            self.__stream.write('---\n')
            self.__stream.write(file_entity.get_yaml())
            return True
        except Exception as msg:
            filename = file_entity.get_filename()
            warn("Write failed: %s" % filename)
            return False

