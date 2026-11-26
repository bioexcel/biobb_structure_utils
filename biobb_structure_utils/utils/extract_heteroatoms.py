#!/usr/bin/env python3

"""Module containing the ExtractHeteroAtoms class and the command line interface."""
from typing import Optional
from Bio.PDB.PDBParser import PDBParser
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu

from biobb_structure_utils.utils.common import (
    _from_string_to_list,
    check_format_heteroatoms,
    create_biopython_residue,
    create_output_file,
    residue_value,
)


class ExtractHeteroAtoms(BiobbObject):
    """
    | biobb_structure_utils ExtractHeteroAtoms
    | Class to extract hetero-atoms from a 3D structure using Biopython.
    | Extracts a list of heteroatoms from a 3D structure using Biopython.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_heteroatom.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        output_heteroatom_path (str): Output heteroatom file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_heteroatom.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **heteroatoms** (*list*) - (None) List of dictionaries with the name | res_id | chain | model of the heteroatoms to be extracted. Format: [{"name": "ZZ7", "res_id": "302", "chain": "B", "model": "1"}]. The res_id of a residue with an insertion code includes the code ("62A"). If empty, all the heteroatoms of the structure will be returned.
            * **water** (*bool*) - (False) Add or not waters.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.extract_heteroatoms import extract_heteroatoms
            prop = {
                'heteroatoms': [
                    {
                        'name': 'ZZ7',
                        'res_id': '302',
                        'chain': 'B',
                        'model': '1'
                    }
                ]
            }
            extract_heteroatoms(input_structure_path='/path/to/myStructure.pdb',
                                output_heteroatom_path='/path/to/newHeteroatom.pdb',
                                properties=prop)

    Info:
        * wrapped_software:
            * name: In house using Biopython
            * version: >=1.76
            * license: other
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self, input_structure_path: str, output_heteroatom_path: str, properties: Optional[dict] = None, **kwargs
    ) -> None:
        super().__init__(**locals())

        # Properties specific for BB
        self.heteroatoms = _from_string_to_list(self.heteroatoms)

    def run(self) -> None:
        """Execute the :class:`ExtractHeteroAtoms <utils.extract_heteroatoms.ExtractHeteroAtoms>` utils.extract_heteroatoms.ExtractHeteroAtoms object."""

        # Business code
        # get list of heteroatoms from properties
        list_heteroatoms = check_format_heteroatoms(self.heteroatoms, self.out_log)

        # load input into BioPython structure
        structure = PDBParser(QUIET=True).get_structure(
            "structure", self.sandbox_file("input_structure_path")
        )

        new_structure = []
        # get desired heteroatoms
        for residue in structure.get_residues():
            r = create_biopython_residue(residue)
            if list_heteroatoms:
                for het in list_heteroatoms:
                    match = True
                    for code in het["code"]:
                        if het[code].strip() != residue_value(r, code).strip():
                            match = False
                            break

                    if match:
                        if not self.water and (
                            r["name"] == "HOH" or r["name"] == "SOL" or r["name"] == "WAT"
                        ):
                            pass
                        else:
                            new_structure.append(r)
            else:
                if not self.water and (
                    r["name"] == "HOH" or r["name"] == "SOL" or r["name"] == "WAT"
                ):
                    pass
                else:
                    new_structure.append(r)

        # if not heteroatoms found in structure, raise exit
        if not new_structure:
            fu.log(
                self.__class__.__name__ + ": The heteroatoms given by user were not found in input structure",
                self.out_log,
            )
            raise SystemExit(
                self.__class__.__name__ + ": The heteroatoms given by user were not found in input structure"
            )

        create_output_file(
            1,
            self.sandbox_file("input_structure_path"),
            new_structure,
            self.sandbox_file("output_heteroatom_path"),
            self.out_log,
        )

        self.return_code = 0


extract_heteroatoms = launcher(ExtractHeteroAtoms)

if __name__ == "__main__":
    ExtractHeteroAtoms.main()
