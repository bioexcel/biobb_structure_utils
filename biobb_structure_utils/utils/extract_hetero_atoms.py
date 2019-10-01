#!/usr/bin/env python3

"""Module containing the ExtractHeteroAtoms class and the command line interface."""

class ExtractHeteroAtoms():
    """Class to remove the selected ligand atoms from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path.
        output_structure_path (str): Output structure file path.
        properties (dic):
            * **regular_expression_pattern** (*str*) - ("^D") Python style regular expression matching the selected atom names.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            
    """

    def __init__(self, input_structure_path, output_structure_path, properties=None, **kwargs):
        properties = properties or {}


    def launch(self):
        """Remove ligand atoms from the structure."""
        

        return 0

def main():
    """Command line interface."""

    #Specific call of each building block
    ExtractHeteroAtoms(input_structure_path=args.input_structure_path, output_structure_path=args.output_structure_path, properties=properties).launch()

if __name__ == '__main__':
    main()
