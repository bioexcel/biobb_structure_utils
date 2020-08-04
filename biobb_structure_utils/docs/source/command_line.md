# BioBB Structure Utils Command Line Help

Generic usage:


```python
biobb_command [-h] --config CONFIG --input_file(s) <input_file(s)> --output_file <output_file>
```

-----------------

## Add hydrogens

Class to add hydrogens to a 3D structure.

### Get help

Command:


```python
add_hydrogens -h
```


```python
usage: add_hydrogens [-h] [-c CONFIG] -i INPUT_STRUCTURE_PATH -o OUTPUT_STRUCTURE_PATH

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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/str_no_H.pdb). Accepted formats: pdb.
* **output_structure_path** (*str*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_str_H.pdbqt). Accepted formats: pdb, pdbqt.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **charges** (*bool*) - (False) Wether or not to add charges to the output file. It must be True if output is a PDBQT.
* **mode** (*string*) - (None) Selection mode. Values: auto, list, ph, int, int_his
* **check_structure_path** (*string*) - ("check_structure") path to the check_structure application
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### Command line


```python
add_hydrogens --input_structure_path data/input/structure_no_H.pdb --output_structure_path data/output/structure_H.pdb
```

## Cat PDB

Class to concat two PDB structures in a single PDB file.

### Get help

Command:


```python
cat_pdb -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure1** (*str*): Input structure 1 file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cat_protein.pdb). Accepted formats: pdb.
* **input_structure2** (*str*): Input structure 2 file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cat_ligand.pdb). Accepted formats: pdb.
* **output_structure_path** (*str*): Output protein file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_cat_pdb.pdb). Accepted formats: pdb.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### Command line


```python
cat_pdb --input_structure1 data/input/cat_protein.pdb --input_structure2 data/input/cat_ligand.pdb --output_structure_path data/output/output.cat.pdb
```

## Extract Atoms

Class to extract atoms from a 3D structure.

### Get help

Command:


```python
extract_atoms -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/2vgb.pdb). Accepted formats: pdb, gro.
* **output_structure_path** (*str*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/OE2_atoms.pdb). Accepted formats: pdb, gro.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **regular_expression_pattern** (*str*) - ("^D") Python style regular expression matching the selected atom names.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### YAML file config

extract_atoms.yml


```python
properties:
  regular_expression_pattern: OE2
```


```python
extract_atoms --config data/conf/extract_atoms.yml --input_structure_path data/input/2vgb.pdb --output_structure_path data/output/output.extat.pdb
```

### JSON file config

extract_atoms.json


```python
{
  "properties": {
    "regular_expression_pattern": "OE2"
  }
}
```

Command:


```python
extract_atoms --config data/conf/extract_atoms.json --input_structure_path data/input/2vgb.pdb --output_structure_path data/output/output.extat.pdb
```

## Extract Chain

Class to extract a chain from a 3D structure.

### Get help

Command:


```python
extract_chain -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_chain.pdb). Accepted formats: pdb.
* **output_structure_path** (*str*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_chain.pdb). Accepted formats: pdb.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **chains** (*list*) - (None) List of chains to be extracted from the input_structure_path file. If empty, all the chains of the structure will be returned.
* **check_structure_path** (*string*) - ("check_structure") path to the check_structure application
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### YAML file config

extract_chain.yml


```python
properties:
  chains: [B,C]
```


```python
extract_chain --config data/conf/extract_chain.yml --input_structure_path data/input/extract_chain.pdb --output_structure_path data/output/output.extch.pdb
```

### JSON file config

extract_chain.json


```python
{
  "properties": {
    "chains": ["B","C"]
  }
}
```

Command:


```python
extract_chain --config data/conf/extract_chain.json --input_structure_path data/input/extract_chain.pdb --output_structure_path data/output/output.extch.pdb
```

## Extract Heteroatoms

Class to extract hetero-atoms from a 3D structure.

### Get help

Command:


```python
extract_heteroatoms -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_heteroatom.pdb). Accepted formats: pdb.
* **output_heteroatom_path** (*str*): Output heteroatom file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_heteroatom.pdb). Accepted formats: pdb.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **heteroatoms** (*list*) - (None) List of dictionaries with the name | res_id | chain | model of the heteroatoms to be extracted. Format: [{"name": "ZZ7", "res_id": "302", "chain": "B", "model": "1"}]. If empty, all the heteroatoms of the structure will be returned.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### YAML file config

extract_heteroatoms.yml


```python
properties:
  heteroatoms: [{
    "name": "TA1",
    "model": "1"
  },
  {
    "name": "ADP"
  }]
```


```python
extract_heteroatoms --config data/conf/extract_heteroatoms.yml --input_structure_path data/input/extract_heteroatom.pdb --output_heteroatom_path data/output/output.exthet.pdb
```

### JSON file config

extract_heteroatoms.json


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

Command:


```python
extract_heteroatoms --config data/conf/extract_heteroatoms.json --input_structure_path data/input/extract_heteroatom.pdb --output_heteroatom_path data/output/output.exthet.pdb
```

## Extract Model

Class to extract a model from a 3D structure.

### Get help

Command:


```python
extract_model -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_model.pdb). Accepted formats: pdb.
* **output_structure_path** (*str*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_model.pdb). Accepted formats: pdb.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **models** (*list*) - (None) List of models to be extracted from the input_structure_path file. If empty, all the models of the structure will be returned.
* **check_structure_path** (*string*) - ("check_structure") path to the check_structure application
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### YAML file config

extract_model.yml


```python
properties:
  models: [1,4]
```


```python
extract_model --config data/conf/extract_model.yml --input_structure_path data/input/extract_model.pdb --output_structure_path data/output/output.extmod.pdb
```

### JSON file config

extract_model.json


```python
{
  "properties": {
    "models": [1,4]
  }
}
```

Command:


```python
extract_model --config data/conf/extract_model.json --input_structure_path data/input/extract_model.pdb --output_structure_path data/output/output.extmod.pdb
```

## Extract Protein

Class to extract a protein from a 3D structure.

### Get help

Command:


```python
extract_protein -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_protein.pdb). Accepted formats: pdb.
* **output_protein_path** (*str*): Output protein file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_protein.pdb). Accepted formats: pdb.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **check_structure_path** (*string*) - ("check_structure") path to the check_structure application
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### Command line


```python
extract_protein --input_structure_path data/input/extract_protein.pdb --output_protein_path data/output/output.extprot.pdb
```

## Remove Ligand

Class to remove the selected ligand atoms from a 3D structure.

### Get help

Command:


```python
remove_ligand -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_1.pdb). Accepted formats: pdb, gro.
* **output_structure_path** (*str*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_apo_md_1.pdb). Accepted formats: pdb, gro.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **ligand** (*str*) - ("AQ4") Residue code of the ligand to be removed.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### YAML file config

remove_ligand.yml


```python
properties:
  ligand: 'AQ4'
```


```python
remove_ligand --config data/conf/remove_ligand.yml --input_structure_path data/input/WT_aq4_md_1.pdb --output_structure_path data/output/output.remlig.pdb
```

### JSON file config

remove_ligand.json


```python
{
  "properties": {
    "ligand": "AQ4"
  }
}
```

Command:


```python
remove_ligand --config data/conf/remove_ligand.json --input_structure_path data/input/WT_aq4_md_1.pdb --output_structure_path data/output/output.remlig.pdb
```

## Remove PDB Water

Class to remove water molecules from PDB 3D structures.

### Get help

Command:


```python
remove_pdb_water -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_pdb_path** (*str*): Input PDB file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_WAT.pdb). Accepted formats: pdb.
* **output_pdb_path** (*str*): Output PDB file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_apo_no_wat.pdb). Accepted formats: pdb.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **check_structure_path** (*string*) - ("check_structure") path to the check_structure application
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### Command line


```python
remove_pdb_water --input_pdb_path data/input/WT_aq4_md_WAT.pdb --output_pdb_path data/output/output.remwat.pdb
```

## Renumber Structure

Class to renumber atomic indexes from a 3D structure.

### Get help

Command:


```python
renumber_structure -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_structure_path** (*str*): Input structure file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cl3.noH.pdb). Accepted formats: pdb, gro.
* **output_structure_path** (*str*): Output structure file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/renum_cl3_noH.pdb). Accepted formats: pdb, gro.
* **output_mapping_json_path** (*str*): Output mapping json file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/cl3_output_mapping_json_path.json). Accepted formats: json.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **renumber_residues** (*bool*) - (True) Residue code of the ligand to be removed.
* **renumber_residues_per_chain** (*bool*) - (True) Restart residue enumeration every time a new chain is detected.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### Command line


```python
renumber_structure --input_structure_path data/input/cl3.noH.pdb --output_mapping_json_path data/output/output.renstr.json --output_structure_path data/output/output.renstr.pdb
```

## Sort GRO Residues

Class to sort the selected residues from a GRO 3D structure.

### Get help

Command:


```python
sort_gro_residues -h
```


```python
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
```

### I / O Arguments

Syntax: input_argument (datatype) : Definition

Config input / output arguments for this building block:

* **input_gro_path** (*str*): Input GRO file path. File type: input. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_1.gro). Accepted formats: gro.
* **output_gro_path** (*str*): Output sorted GRO file path. File type: output. [Sample file](https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_aq4_md_sorted.gro). Accepted formats: gro.

### Config

Syntax: input_parameter (datatype) - (default_value) Definition

Config parameters for this building block:

* **residue_name_list** (*list*) - (["NA", "CL", "SOL"]) Ordered residue name list.
* **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
* **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

### YAML file config

sort_gro_residues.yml


```python
properties:
  residue_name_list: ['NA', 'CL', 'SOL']
```


```python
sort_gro_residues --config data/conf/sort_gro_residues.yml --input_gro_path data/input/WT_aq4_md_1.gro --output_gro_path data/output/output.sortgro.gro
```

### JSON file config

sort_gro_residues.json


```python
{
  "properties": {
    "residue_name_list": ["NA", "CL", "SOL"]
  }
}
```

Command:


```python
sort_gro_residues --config data/conf/sort_gro_residues.json --input_gro_path data/input/WT_aq4_md_1.gro --output_gro_path data/output/output.sortgro.gro
```
