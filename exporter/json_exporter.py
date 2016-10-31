from os             import path
from hashlib        import md5
from warnings       import warn
from json           import dump
from library        import File, Group
from .exporter      import Exporter

def _digest(thing):
    return md5(str(thing).encode('utf-8')).hexdigest()

class JsonExporter(Exporter):

    def __init__(self, library):
        super().__init__(library)
        self.__dict = {}
        self.__ok   = False

    def export_to_file(self, stream):
        if not stream or stream.closed:
            return False
        self.__dict     = { 
                'file'      : {},
                'group'     : {},
                'reference' : { 'path': {}, 'cellset': {} },
                }
        for component in self.get_library():
            component.accept(self)
        dump(self.__dict, stream, indent=2)
        return True

    def visitDbFile(self, file):
        self._file_to_dict(file)

    def visitCtlFile(self, file):
        self._file_to_dict(file)

    def visitGdsFile(self, file):
        self._file_to_dict(file)

    def visitLefFile(self, file):
        self._file_to_dict(file)

    def visitLibFile(self, file):
        self._file_to_dict(file)

    def visitLibGroup(self, group):
        pass

    def visitCornerGroup(self, group):
        pass

    def visitIpGroup(self, group):
        pass

    def _file_to_dict(self, file):
        filename    = file.name()
        filetype    = file.type()
        basename    = path.basename(filename)
        pathname    = path.dirname(filename)
        cells       = sorted( file.get_cells() )
        fdigest     = _digest(filename)
        pdigest     = _digest(pathname)
        cdigest     = _digest( ''.join(cells) )
        if pdigest not in self.__dict['reference']['path']:
            self.__dict['reference']['path'][pdigest] = pathname
        if filetype not in self.__dict['file']:
            self.__dict['file'][filetype] = {}
        self.__dict['file'][filetype][fdigest] = {}
        fd        = self.__dict['file'][filetype][fdigest]
        fd['name'] = basename
        fd['path'] = pdigest
        fd['type'] = filetype
        fd['attribute'] = {}
        for name in file.get_attribute_names():
            fd['attribute'][name] = file.get_attribute_value(name)
        fd['cellset']   = cdigest
        if cdigest not in self.__dict['reference']['cellset']:
            self.__dict['reference']['cellset'][cdigest] = cells
        fd['member'] = {}
        parent = file.get_parent()
        if parent:
            fd['member'] = { parent.type() : parent.name() }
            self._group_to_dict(parent)

    def _group_to_dict(self, group):
        groupname   = group.name()
        grouptype   = group.type()
        if grouptype not in self.__dict['group']:
            self.__dict['group'][grouptype] = {}
        self.__dict['group'][grouptype][groupname] = {}
        gd = self.__dict['group'][grouptype][groupname]
        gd['name'] = groupname
        gd['type'] = grouptype
        gd['attribute'] = {}
        for name in group.get_attribute_names():
            gd['attribute'][name] = group.get_attribute_value(name)
        cells = sorted( group.get_cells() )
        cdigest     = _digest( ''.join(cells) )
        gd['cellset']   = cdigest
        if cdigest not in self.__dict['reference']:
            self.__dict['reference']['cellset'][cdigest] = cells
        gd['group']     = {}
        gd['file']      = {}
        for component in group.get_members():
            cname = component.name()
            ctype = component.type()
            if isinstance(component, File):
                cdigest = _digest(cname)
                gd['file'][cdigest] = ctype
            else:
                gd['group'][cname]  = ctype
        gd['member']    = {}
        parent = group.get_parent()
        if parent:
            gd['member'] = { parent.type() : parent.name() }
            self._group_to_dict(parent)

