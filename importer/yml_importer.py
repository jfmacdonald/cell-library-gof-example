from warnings       import warn
from yaml           import load_all
from os             import path
from .importer      import Importer
from entity         import FileEntity

class YmlImporter(Importer):

    def import_from_file(self, filename):
        if not path.exists(filename):
            warn("No file "+filename, UserWarning)
            return False
        try:
            with open(filename,'r') as f:
                docs = load_all(f)
                for doc in docs:
                    try:
                        filename = doc['filename']
                    except Exception:
                        continue
                    filetype = doc['filetype'] if 'filetype' in doc else ''
                    entity = FileEntity(filename, filetype)
                    for name in ['attribute', 'cell', 'group']:
                        setter  = 'entity.set_' + name
                        table   = {}
                        if name in doc:
                            table = doc[name]
                        elif name + 's' in doc:
                            table = doc[name+'s']
                        for entry in table:
                            eval(setter)(entry, table[entry])
                        self._import_file_entity(entity)
        except Exception as msg:
            warn("%s: can't import %s" % (msg, filename))
            return False
        return True



                        


                

