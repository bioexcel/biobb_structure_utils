# BioBB STRUCTURE Command Line Help
Generic usage:
```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```
-----------------


## Str_check_add_hydrogens
This class is a wrapper of the Structure Checking tool to add hydrogens to a 3D structure.
### Get help
Command:
```python
str_check_add_hydrogens -h
```
    usage: str_check_add_hydrogens [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_STRUCTURE_PATH
    
    Class to add hydrogens to a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_STRUCTURE_PATH, --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file path. Accepted formats: pdb.
      -o OUTPUT_STRUCTURE_PATH, --output_structure_path OUTPUT_STRUCTURE_PATH
                            Output structure file path. Accepted formats: pdb, pdbqt.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/str_no_H.pdb). Accepted formats: PDB
* **output_structure_path** (*string*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_str_H.pdbqt). Accepted formats: PDB, PDBQT
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **charges** (*boolean*): (False) Wether or not to add charges to the output file. If True the output is in PDBQT format..
* **mode** (*string*): (None) Selection mode. .
* **check_structure_path** (*string*): (check_structure) path to the check_structure application.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_str_check_add_hydrogens.yml)
```python
properties:
  charges: true
  mode: auto

```
#### Command line
```python
str_check_add_hydrogens --config config_str_check_add_hydrogens.yml --input_structure_path str_no_H.pdb --output_structure_path ref_str_H.pdbqt
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_str_check_add_hydrogens.json)
```python
{
  "properties": {
    "charges": true,
    "mode": "auto"
  }
}
```
#### Command line
```python
str_check_add_hydrogens --config config_str_check_add_hydrogens.json --input_structure_path str_no_H.pdb --output_structure_path ref_str_H.pdbqt
```

## Extract_heteroatoms
Class to extract hetero-atoms from a 3D structure using Biopython.
### Get help
Command:
```python
extract_heteroatoms -h
```
    usage: extract_heteroatoms [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_HETEROATOM_PATH
    
    Extract a list of heteroatoms from a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_STRUCTURE_PATH, --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file path. Accepted formats: pdb.
      -o OUTPUT_HETEROATOM_PATH, --output_heteroatom_path OUTPUT_HETEROATOM_PATH
                            Output heteroatom file path. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_heteroatom.pdb). Accepted formats: PDB
* **output_heteroatom_path** (*string*): Output heteroatom file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_heteroatom.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **heteroatoms** (*array*): (None) List of dictionaries with the name | res_id | chain | model of the heteroatoms to be extracted. Format: [{"name": "ZZ7", "res_id": "302", "chain": "B", "model": "1"}]. If empty, all the heteroatoms of the structure will be returned..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_heteroatoms.yml)
```python
properties:
  heteroatoms:
  - model: '1'
    name: TA1
  - name: ADP

```
#### Command line
```python
extract_heteroatoms --config config_extract_heteroatoms.yml --input_structure_path extract_heteroatom.pdb --output_heteroatom_path ref_extract_heteroatom.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_heteroatoms.json)
```python
{
  "properties": {
    "heteroatoms": [
      {
        "name": "TA1",
        "model": "1"
      },
      {
        "name": "ADP"
      }
    ]
  }
}
```
#### Command line
```python
extract_heteroatoms --config config_extract_heteroatoms.json --input_structure_path extract_heteroatom.pdb --output_heteroatom_path ref_extract_heteroatom.pdb
```

## Sort_gro_residues
Class to sort the selected residues from a GRO 3D structure.
### Get help
Command:
```python
sort_gro_residues -h
```
    usage: sort_gro_residues [-h] [-c CONFIG] -i INPUT_GRO_PATH -o OUTPUT_GRO_PATH
    
    Renumber atoms and residues from a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_GRO_PATH, --input_gro_path INPUT_GRO_PATH
                            Input GRO file name
      -o OUTPUT_GRO_PATH, --output_gro_path OUTPUT_GRO_PATH
                            Output sorted GRO file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_gro_path** (*string*): Input GRO file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_1.gro). Accepted formats: GRO
* **output_gro_path** (*string*): Output sorted GRO file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_aq4_md_sorted.gro). Accepted formats: GRO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **residue_name_list** (*array*): ([NA, CL, SOL]) Ordered residue name list..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_sort_gro_residues.yml)
```python
properties:
  residue_name_list:
  - NA
  - CL
  - SOL

```
#### Command line
```python
sort_gro_residues --config config_sort_gro_residues.yml --input_gro_path WT_aq4_md_1.gro --output_gro_path WT_aq4_md_sorted.gro
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_sort_gro_residues.json)
```python
{
  "properties": {
    "residue_name_list": [
      "NA",
      "CL",
      "SOL"
    ]
  }
}
```
#### Command line
```python
sort_gro_residues --config config_sort_gro_residues.json --input_gro_path WT_aq4_md_1.gro --output_gro_path WT_aq4_md_sorted.gro
```

## Extract_protein
This class is a wrapper of the Structure Checking tool to extract a protein from a 3D structure.
### Get help
Command:
```python
extract_protein -h
```
    usage: extract_protein [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_PROTEIN_PATH
    
    Extract a protein from a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_STRUCTURE_PATH, --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file path. Accepted formats: pdb.
      -o OUTPUT_PROTEIN_PATH, --output_protein_path OUTPUT_PROTEIN_PATH
                            Output heteroatom file path. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_protein.pdb). Accepted formats: PDB
* **output_protein_path** (*string*): Output protein file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_protein.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **check_structure_path** (*string*): (check_structure) path to the check_structure application.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_protein.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
extract_protein --config config_extract_protein.yml --input_structure_path extract_protein.pdb --output_protein_path ref_extract_protein.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_protein.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
extract_protein --config config_extract_protein.json --input_structure_path extract_protein.pdb --output_protein_path ref_extract_protein.pdb
```

## Extract_atoms
Class to extract atoms from a 3D structure.
### Get help
Command:
```python
extract_atoms -h
```
    usage: extract_atoms [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_STRUCTURE_PATH
    
    Remove the selected ligand atoms from a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_STRUCTURE_PATH, --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file name
      -o OUTPUT_STRUCTURE_PATH, --output_structure_path OUTPUT_STRUCTURE_PATH
                            Output structure file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/2vgb.pdb). Accepted formats: PDB, GRO
* **output_structure_path** (*string*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/OE2_atoms.pdb). Accepted formats: PDB, GRO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **regular_expression_pattern** (*string*): (^D) Python style regular expression matching the selected atom names..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_atoms.yml)
```python
properties:
  regular_expression_pattern: OE2

```
#### Command line
```python
extract_atoms --config config_extract_atoms.yml --input_structure_path 2vgb.pdb --output_structure_path OE2_atoms.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_atoms.json)
```python
{
  "properties": {
    "regular_expression_pattern": "OE2"
  }
}
```
#### Command line
```python
extract_atoms --config config_extract_atoms.json --input_structure_path 2vgb.pdb --output_structure_path OE2_atoms.pdb
```

## Renumber_structure
Class to renumber atomic indexes from a 3D structure.
### Get help
Command:
```python
renumber_structure -h
```
    usage: renumber_structure [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_STRUCTURE_PATH -j OUTPUT_MAPPING_JSON_PATH
    
    Renumber atoms and residues from a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_STRUCTURE_PATH, --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file name
      -o OUTPUT_STRUCTURE_PATH, --output_structure_path OUTPUT_STRUCTURE_PATH
                            Output structure file name
      -j OUTPUT_MAPPING_JSON_PATH, --output_mapping_json_path OUTPUT_MAPPING_JSON_PATH
                            Output mapping json file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cl3.noH.pdb). Accepted formats: PDB, GRO
* **output_structure_path** (*string*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/renum_cl3_noH.pdb). Accepted formats: PDB, GRO
* **output_mapping_json_path** (*string*): Output mapping json file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/cl3_output_mapping_json_path.json). Accepted formats: JSON
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **renumber_residues** (*boolean*): (True) Residue code of the ligand to be removed..
* **renumber_residues_per_chain** (*boolean*): (True) Restart residue enumeration every time a new chain is detected..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_renumber_structure.yml)
```python
properties:
  renumber_residues: true

```
#### Command line
```python
renumber_structure --config config_renumber_structure.yml --input_structure_path cl3.noH.pdb --output_structure_path renum_cl3_noH.pdb --output_mapping_json_path cl3_output_mapping_json_path.json
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_renumber_structure.json)
```python
{
  "properties": {
    "renumber_residues": true
  }
}
```
#### Command line
```python
renumber_structure --config config_renumber_structure.json --input_structure_path cl3.noH.pdb --output_structure_path renum_cl3_noH.pdb --output_mapping_json_path cl3_output_mapping_json_path.json
```

## Cat_pdb
Class to concat two PDB structures in a single PDB file.
### Get help
Command:
```python
cat_pdb -h
```
    usage: cat_pdb [-h] [-c CONFIG] -i1 INPUT_STRUCTURE1 -i2 INPUT_STRUCTURE2 -o OUTPUT_STRUCTURE_PATH
    
    Concat two PDB structures in a single PDB file.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i1 INPUT_STRUCTURE1, --input_structure1 INPUT_STRUCTURE1
                            Input structure 1 file path. Accepted formats: pdb.
      -i2 INPUT_STRUCTURE2, --input_structure2 INPUT_STRUCTURE2
                            Input structure 2 file path. Accepted formats: pdb.
      -o OUTPUT_STRUCTURE_PATH, --output_structure_path OUTPUT_STRUCTURE_PATH
                            Output structure file path. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure1** (*string*): Input structure 1 file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cat_protein.pdb). Accepted formats: PDB
* **input_structure2** (*string*): Input structure 2 file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cat_ligand.pdb). Accepted formats: PDB
* **output_structure_path** (*string*): Output protein file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_cat_pdb.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_cat_pdb.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
cat_pdb --config config_cat_pdb.yml --input_structure1 cat_protein.pdb --input_structure2 cat_ligand.pdb --output_structure_path ref_cat_pdb.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_cat_pdb.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
cat_pdb --config config_cat_pdb.json --input_structure1 cat_protein.pdb --input_structure2 cat_ligand.pdb --output_structure_path ref_cat_pdb.pdb
```

## Remove_pdb_water
This class is a wrapper of the Structure Checking tool to remove water molecules from PDB 3D structures.
### Get help
Command:
```python
remove_pdb_water -h
```
    usage: remove_pdb_water [-h] [-c CONFIG] -i INPUT_PDB_PATH -o OUTPUT_PDB_PATH
    
    Remove the water molecules from a PDB 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_PDB_PATH, --input_pdb_path INPUT_PDB_PATH
                            Input pdb file name
      -o OUTPUT_PDB_PATH, --output_pdb_path OUTPUT_PDB_PATH
                            Output pdb file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_pdb_path** (*string*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_WAT.pdb). Accepted formats: PDB
* **output_pdb_path** (*string*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_apo_no_wat.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **check_structure_path** (*string*): (check_structure) path to the check_structure application.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_remove_pdb_water.yml)
```python
properties:
  remove_tmp: true

```
#### Command line
```python
remove_pdb_water --config config_remove_pdb_water.yml --input_pdb_path WT_aq4_md_WAT.pdb --output_pdb_path WT_apo_no_wat.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_remove_pdb_water.json)
```python
{
  "properties": {
    "remove_tmp": true
  }
}
```
#### Command line
```python
remove_pdb_water --config config_remove_pdb_water.json --input_pdb_path WT_aq4_md_WAT.pdb --output_pdb_path WT_apo_no_wat.pdb
```

## Extract_model
This class is a wrapper of the Structure Checking tool to extract a model from a 3D structure.
### Get help
Command:
```python
extract_model -h
```
    usage: extract_model [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_STRUCTURE_PATH
    
    Extract a model from a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_STRUCTURE_PATH, --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file path. Accepted formats: pdb.
      -o OUTPUT_STRUCTURE_PATH, --output_structure_path OUTPUT_STRUCTURE_PATH
                            Output structure file path. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_model.pdb). Accepted formats: PDB
* **output_structure_path** (*string*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_model.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **models** (*array*): (None) List of models to be extracted from the input_structure_path file. If empty, all the models of the structure will be returned..
* **check_structure_path** (*string*): (check_structure) path to the check_structure application.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_model.yml)
```python
properties:
  models:
  - 1
  - 4

```
#### Command line
```python
extract_model --config config_extract_model.yml --input_structure_path extract_model.pdb --output_structure_path ref_extract_model.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_model.json)
```python
{
  "properties": {
    "models": [
      1,
      4
    ]
  }
}
```
#### Command line
```python
extract_model --config config_extract_model.json --input_structure_path extract_model.pdb --output_structure_path ref_extract_model.pdb
```

## Extract_chain
This class is a wrapper of the Structure Checking tool to extract a chain from a 3D structure.
### Get help
Command:
```python
extract_chain -h
```
    usage: extract_chain [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_STRUCTURE_PATH
    
    Extract a chain from a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_STRUCTURE_PATH, --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file path. Accepted formats: pdb.
      -o OUTPUT_STRUCTURE_PATH, --output_structure_path OUTPUT_STRUCTURE_PATH
                            Output structure file path. Accepted formats: pdb.
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_chain.pdb). Accepted formats: PDB
* **output_structure_path** (*string*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_chain.pdb). Accepted formats: PDB
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **chains** (*array*): (None) List of chains to be extracted from the input_structure_path file. If empty, all the chains of the structure will be returned..
* **check_structure_path** (*string*): (check_structure) path to the check_structure application.
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_chain.yml)
```python
properties:
  chains:
  - B
  - C

```
#### Command line
```python
extract_chain --config config_extract_chain.yml --input_structure_path extract_chain.pdb --output_structure_path ref_extract_chain.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_extract_chain.json)
```python
{
  "properties": {
    "chains": [
      "B",
      "C"
    ]
  }
}
```
#### Command line
```python
extract_chain --config config_extract_chain.json --input_structure_path extract_chain.pdb --output_structure_path ref_extract_chain.pdb
```

## Remove_ligand
Class to remove the selected ligand atoms from a 3D structure.
### Get help
Command:
```python
remove_ligand -h
```
    usage: remove_ligand [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_STRUCTURE_PATH
    
    Remove the selected ligand atoms from a 3D structure.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            This file can be a YAML file, JSON file or JSON string
    
    required arguments:
      -i INPUT_STRUCTURE_PATH, --input_structure_path INPUT_STRUCTURE_PATH
                            Input structure file name
      -o OUTPUT_STRUCTURE_PATH, --output_structure_path OUTPUT_STRUCTURE_PATH
                            Output structure file name
### I / O Arguments
Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:
* **input_structure_path** (*string*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_1.pdb). Accepted formats: PDB, GRO
* **output_structure_path** (*string*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_apo_md_1.pdb). Accepted formats: PDB, GRO
### Config
Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:
* **ligand** (*string*): (AQ4) Residue code of the ligand to be removed..
* **remove_tmp** (*boolean*): (True) Remove temporal files..
* **restart** (*boolean*): (False) Do not execute if output files exist..
### YAML
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_remove_ligand.yml)
```python
properties:
  ligand: AQ4

```
#### Command line
```python
remove_ligand --config config_remove_ligand.yml --input_structure_path WT_aq4_md_1.pdb --output_structure_path WT_apo_md_1.pdb
```
### JSON
#### [Common config file](https://github.com/bioexcel/biobb_structure_utils/blob/master/biobb_structure_utils/test/data/config/config_remove_ligand.json)
```python
{
  "properties": {
    "ligand": "AQ4"
  }
}
```
#### Command line
```python
remove_ligand --config config_remove_ligand.json --input_structure_path WT_aq4_md_1.pdb --output_structure_path WT_apo_md_1.pdb
```
