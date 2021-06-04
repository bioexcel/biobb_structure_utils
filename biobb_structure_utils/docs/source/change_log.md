# Biobb Structure Utils changelog

## What's new in version [3.5.3](https://github.com/bioexcel/biobb_structure_utils/releases/tag/v3.5.3)?
In version 3.5.3 the tool extract_protein has been renamed to extract_molecule

### New features

* Tool extract_protein renamed to extract_molecule

## What's new in version [3.5.2](https://github.com/bioexcel/biobb_structure_utils/releases/tag/v3.5.2)?
In version 3.5.2 the dependency biobb_structure_checking has been updated to 3.7.3 version. New tool for checking structures.

### New features

* Update to biobb_structure_checking 3.7.3 
* New StructureCheck tool

## What's new in version [3.5.1](https://github.com/bioexcel/biobb_structure_utils/releases/tag/v3.5.1)?
In version 3.5.1 the dependency biobb_structure_checking has been updated to 3.5.3 version. 

### New features

* Update to biobb_structure_checking 3.5.3 

## What's new in version [3.5.0](https://github.com/bioexcel/biobb_structure_utils/releases/tag/v3.5.0)?
In version 3.5.0 the dependency biobb_common has been updated to 3.5.1 version. Also, there has been implemented the new version of docstrings, therefore the JSON Schemas have been modified.

### New features

* Update to biobb_common 3.5.1 (general)
* Update to Biopython 1.78 (general)
* New extended and improved JSON schemas (Galaxy and CWL-compliant) (general)

### Other changes

* New docstrings

## What's new in version [3.0.1](https://github.com/bioexcel/biobb_structure_utils/releases/tag/v3.0.1)?
In version 3.0.1 the dependency biobb_common has been updated to 3.0.1 version. New tool for adding hydrogens to a 3D structure.

### New features

* Update to biobb_common 3.0.1
* New StrCheckAddHydrogens tool

### Other changes

* Bug fixes in CatPDB
* Bug fixes in ExtractChain
* Bug fixes in ExtractHeteroAtoms
* Bug fixes in ExtractModel
* Bug fixes in ExtractProtein
* Bug fixes in RemovePdbWater

## What's new in version [3.0.0](https://github.com/bioexcel/biobb_structure_utils/releases/tag/v3.0.0)?
In version 3.0.0 Python has been updated to version 3.7 and Biopython to version 1.76. Big changes in the documentation style and content. Finally a new conda installation recipe has been introduced.

### New features

* Update to Python 3.7 (general)
* Update to Biopython 1.76 (general)
* New conda installer (installation)
* Adding type hinting for easier usage (API)
* Deprecating os.path in favour of pathlib.path (modules)
* New command line documentation (documentation)

### Other changes

* New documentation styles (documentation)