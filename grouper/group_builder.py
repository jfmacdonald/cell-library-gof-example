
from library                    import *
from grouper.partitioner        import Partitioner
from grouper.grouper_template   import GrouperTemplate

class GroupBuilder(GrouperTemplate):


    def build_cornergroups(self):
        library = self.get_library()
        for file in library:
            library_name = file.get_attribute_value('library')
            if not library_name: continue
            cg = library.get_group(library_name,'cornergroup')
            if not cg:
                cg = CornerGroup(library_name)
                cg.set_attribute_value('library', library_name)
                library.add_component(cg)
            cg.add(file)

    def build_libgroups(self):
        library = self.get_library()
        partitioner = Partitioner()
        partitioner.add_library_components(
            library.get_groups('cornergroup') )
        partitioner.partition()
        for part in partitioner.get_partitions():
            names = set()
            for cg in part: names.add(cg.name())
            libgroup_name = self.digest(''.join(sorted(names)))
            lg = library.get_group(libgroup_name,'libgroup')
            if not lg:
                lg = LibGroup(libgroup_name)
                library.add_component(lg)
            for cg in part: lg.add(cg)

    def build_ipgroups(self):
        library = self.get_library()
        partitioner = Partitioner()
        partitioner.add_library_components(
            library.get_groups('libgroup') )
        freefiles = set()
        for file in library.get_files():
            if not file.get_parent(): freefiles.add(file)
        partitioner.add_library_components(freefiles)
        partitioner.partition()
        for part in partitioner.get_partitions():
            cells = set()
            for comp in part:
                for cell in comp.get_cells(): cells.add(cell)
            ipgroup_name = self.digest(''.join(sorted(cells)))
            ipg = library.get_group(ipgroup_name,'ipgroup')
            if not ipg:
                ipg = IpGroup(ipgroup_name)
                library.add_component(ipg)
            for comp in part:
                ipg.add(comp)

