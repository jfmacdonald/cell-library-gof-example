#!/usr/bin/env python3

import entity.cell_entity
import entity.entity
import entity.file_entity
import importer.director
import importer.yml_importer
import importer.json_importer
import exporter.director
import exporter.yml_exporter
import library.component
import library.corner_group
import library.ctl_file
import library.db_file
import library.file
import library.gds_file
import library.group
import library.ip_group
import library.lef_file
import library.lib_file
import library.lib_group
import grouper.group_builder
import grouper.group_re_builder


input_json      = "Fixtures/pgate.in.json"
output_yaml     = "Fixtures/pgate.out.yml"
input_yaml      = "Fixtures/pgate.in.yml"
output_json     = "Fixtures/pgate.out.json"
rebuilt_json    = "Fixtures/pgate.rebuilt.json"

import_director = importer.director.ImportDirector()
print("Reading " + input_json)
library = import_director.import_from_file(input_json)
# for component in library: print("Imported %s::%s" % (component.type(), component.name()))

export_director = exporter.director.ExportDirector(library)
print("Writing " + output_yaml)
export_director.export_to_file(output_yaml)
print("")

import_director = importer.director.ImportDirector()
print("Reading " + input_yaml)
library = import_director.import_from_file(output_yaml)
# for component in library: print("Imported %s::%s" % (component.type(), component.name()))

export_director = exporter.director.ExportDirector(library)
print("Writing " + output_json)
export_director.export_to_file(output_json)
print("")

print("Rebuilding groups . . . ")
group_rebuilder = grouper.group_re_builder.GroupReBuilder(library)
group_rebuilder.build_groups()
print("Writing " + rebuilt_json)
export_director.export_to_file(rebuilt_json)

