
# Representing a Cell Library: A Software Design Pattern Project

```
John MacDonald
3/18/15
```

Software design patterns, as described in the iconic text _Design Patterns:
Elements of Reusable Object-Oriented Software_ by Gamma, Helm, Johnson, and
Vlissides (often called the Gang of Four or simply &ldquo;GoF,&rdquo; are not recipies but
guidelines for creating reusable software that often require adaptation to the
problem at hand. To that end, examples that do more than regurgitate those in
the book.

In this project, software design patterns are applied in a system for managing
cell libraries used in the design of integrated circuits. We first address the
questions of what is a cell and what is meant by a library of cells, then
describe the purpose and function of the software.

## Integrated Circuit Cell Libraries

Integrated circuits are designed hierarchically. Transistors, diodes, resistors,
and other devices lie at the base of the design and are components integrated
into a chip cut from a single semiconductor crystal. These devices are connected
by wires patterned from metal layers deposited on the semiconductor base. A
complex integrated circuit, such as in the cell phone in your pocket, may
contain a billion or more of such base devices. This is too many things to
design all at once, so design teams create small circuits to perform
well-defined functions from the base devices, then more complex circuits using
those as components. Such a component we call a _cell_. 

But a cell is an abstraction. Rather than work with actual devices, design
engineers work with various sorts of models of devices, cells, and more complex
circuits. These models are represented in files of various formats, each format
serving its specific purpose.  Files, then, are the concrete entities that
design engineers work with to create a chip design. Whatever the format or
purpose, each model file contains a representation of one or more cells.

A cell library, then, is a library of model files. For a given design task, the
correct set of files must be selected and used for that task. Managing that
selection process is the responsibility of the cell library. A primary library
manangement function is to find the consistent set of files that model a
particular set of cells.

## Project Description

The software provides a means for transforming the representation of a library
of model files from one format to another. Here we deal with two formats: a JSON
format and a YAML format. In addition to translating the library represenation,
the software provides methods for grouping files that have cells—or rather, cell
models—in common.

The system works with the following model types:

Model           | Description
-----------     | --------------------------------------------------
lef             | An abstracted representation of cell physical structure.
gds             | A detailed representation of cell physical structure.
lib             | A model of cell electrical and performance characteristics given its operating conditions—temperature and supply voltage—and fabrication variance. Each lib model file has a ‘library’ attribute—a string that identifies it and its operating conditions. A set of operating conditions is termed a “corner.”
db              | A compiled form of the lib model.


We identify the following file groups:

Group           | Description
--------------  | --------------------------------------------------
cornergroup     | A group of files with the same “library” attribute. (In the set described here, this should be one lib file and one db file.)
libgroup        | A group defined by the collection of cornergroups modeling the same set of cells. All file cell sets intersect.
ipgroup         | A group defined by the collection of libgroups, lef, and gds files that model the same set of cells.


## Program Description
The project is implemented using Python 3.4 with several modules spread over a 
handful of packages:

Module                              | Descriptions
--------------                      | --------------------------------------------------
test.py                             | Top-level executable script 
library/component.py                | An abstraction of a library component: a file or a group
library/file.py                     | Abstract class representing a file
library/db_file.py                  | Concrete class representing a “db” file
library/gds_file.py                 | Concrete class representing a “gds” file
library/lef_file.py                 | Concrete class representing a “lef” file
library/lib_file.py                 | Concrete class representing a “lib” file
library/group.py                    | Abstract class representing a group of files
library/ip_group.py                 | Concrete class representing an ipgroup
library/lib_group.py                | Concrete class representing a libgroup
library/corner_group.py             | A concrete class representing a cornergroup
library/library.py                  | A concrete class represeting a collection of components
entity/entity.py                    | A storable data representation
entity/file_entity.py               | File storable representation
entity/cell_entity.py               | Cell storable representation (not used)
importer/director.py                | Import director class
importer/importer.py                | Abstract importer
importer/json_importer.py           | Concrete JSON importer
importer/yml_importer.py            | Concrete YAML importer
exporter/director.py                | Export director class
exporter/exporter.py                | Abstract exporter
exporter/json_exporter.py           | Concrete JSON exporter
exporter/yml_exporter.py            | Concrete YAML exporter
grouper/grouper_template.py         | Abstract group builder template
grouper/group_builder.py            | A concrete group builder (default)
grouper/group_re_builder.py         | A concrete modification of group_buildler
grouper/partitioner.py              | a class implementing the partitioning algorithm
yaml/*                              | PyYAML, available from pyyaml.org 


## Design Patterns

The project applies following software design patterns, described in :

### Composite
Both files and file groups represent a set of cells. The collection forms a tree structure 
with files at the leaf level. Participants are `Component`, in library/component.py, `File` 
(Leaf), in library/file.py, and `Group` (Composite), in library/group.py. 

To avoid problems importing and exporting, a separate flat file-entity class structure is 
used to avoid problems with references to objects that may not be in memory.

### Iterator
The `__iter__()` and `__next__()` functions in the `Library` class
(library/library.py) implement the Python iterator protocol. This is so simple
in Python it almost comes for free.

### Builder
The importer package applies the Builder pattern. The `ImportDirector` class
(importer/director.py) plays the role of Director, and the abstract `Importer` class 
(importer/importer.py) and its concrete subclasses are Builders. This differs from the 
GoF examples in that the same complex object (a Library) is constructed from different 
sources.

### Visitor
The Visitor pattern is applied in the exporter.  This is much like the importer,
in that the `ExportDirector` class provides the context and plays a role similar
to the Director in the builder pattern. But here we already have objects; the
intent is to export them. The `Export` abstract class (exporter/exporter.py)
acts as Node Visitor with concrete classes `JsonExporter` and `YmlExporter`
calling `accept()` on library components and receiving call backs to their visit
routines to construct the appropriate export data structures.

### Template Method
The grouper package applies the Template Method. The `GrouperTemplate` class 
provides the template routine build_groups, which calls `build_cornergroups()`, 
`build_libgroups()`, and `build_ipgroups()` in turn. Its derived `GroupBuilder` class provides a 
basic concrete implementation and is further derived to `GroupReBuilder`, which modifies 
one of its primitive routines. These are simply meant to be representative. In practice, a 
variety of special circumstances will call for special methods, and the Template Method 
works great for that.

## Test Case
The “Fixtures” directory contains JSON and YAML representations of a small (fictitious) 
sample library. The test script produces the following output:

```
Reading Fixtures/pgate.in.json
Writing Fixtures/pgate.out.yml

Reading Fixtures/pgate.in.yml
Writing Fixtures/pgate.out.json

Rebuilding groups . . . 
Writing Fixtures/pgate.rebuilt.json
```

## Reference

Gamma, Erich, Richard Helm, Ralph Johnson, and John Vlissides. _Design Patterns:
Elements of Reusabel Object-Oriented Software_, New York: Addison-Wesley, 1994.

