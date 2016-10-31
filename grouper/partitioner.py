
from hashlib         import md5 

def digest(arg):
    digest_string = str(arg)
    return md5(digest_string.encode('utf-8')).hexdigest()

class Partitioner:

    def __init__(self):
        'index cell sets and component sets by md5digest of cell set names'
        self.__cells        = {}
        self.__comps        = {}
        self.__connected    = {}


    def reset(self):
        'start over'
        self.__connected  = {}
        self.__cells      = {}
        self.__comps      = {}

    def add_library_components(self, components):
        'add components for partitioning'
        for component in components:
            cells = sorted(component.get_cells())
            string = ''.join(cells)
            key = digest(string)
            if key not in self.__cells:
                self.__cells[key] = set(cells)
            if key not in self.__comps:
                self.__comps[key] = set()
            self.__comps[key].add(component)
        return len(self.__comps.keys())

    def partition(self):
        'connect components that share a cell and partition the graph'
        #
        # non-recursive depth-first search
        # to find connected cellset digest
        # u and v are digests
        #
        visited = set()
        for key in self.__cells:
            if key in visited: continue
            self.__connected[key] = set()
            stack = [key]
            while len(stack):
                u = stack.pop()
                if u in visited: continue
                visited.add(u)
                u_cells  = self.__cells[u]
                if len(u_cells):
                    self.__connected[key].add(u)
                for v in self.__cells:
                    if v == u: continue
                    v_cells = self.__cells[v]
                    if len(v_cells & u_cells): stack.append(v)
        return len(self.__connected)


    def get_partitions(self):
        '''
        Returns a list of components sets, where the components in each
        set share one or more components and the components in different
        sets do not. Each set represents a partition.
        '''
        sets = []
        for key in self.__connected:
            keys = self.__connected[key]
            keys.add(key)
            components = self._get_components_with_keys(keys)
            sets.append(components)
        return sets

    def _get_components_with_keys(self, keys=[]):
        myset = set()
        if not len(keys):
            for key in self.__comps:
                for component in self.__comps[key]:
                    myset.add(component)
        else:
            for key in keys:
                if key in self.__comps:
                    for component in self.__comps[key]:
                        myset.add(component)
        return myset

    def _get_cells_with_key(self, key):
        if key in self.__cells:
            return self.__cells[key]
        else:
            return set()

    def _get_cellset_keys(self):
        return [key for key in self.__cells]

    def _get_component_set_keys(self):
        return [key for key in self.__comps]

if __name__ == '__main__':
    pass

