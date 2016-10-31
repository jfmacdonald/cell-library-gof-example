from os                     import path
from warnings               import warn
from library                import Library
from .yml_exporter          import YmlExporter
from .json_exporter         import JsonExporter

class ExportDirector:

    def __init__(self, library):
        self.__library = library

    def export_to_file(self, filename):
        if filename[-4:] == '.yml':
            exporter = YmlExporter(self.__library)
        elif filename[-5:] == '.json':
            exporter = JsonExporter(self.__library)
        else:
            warn("Don't know how to export to "+filename, UserWarning)
            return False
        try:
            stream = open(filename, 'w')
        except Exception as msg:
            warn("Can't write " + filename)
            if stream and not stream.closed: stream.close()
            return False
        status = exporter.export_to_file(stream)
        stream.close()
        return status

