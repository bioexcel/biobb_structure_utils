#!/usr/bin/env python3

"""Module containing the ExtractResidues class and the command line interface."""
from typing import Optional
from Bio.PDB.PDBParser import PDBParser
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu

from biobb_structure_utils.utils.common import (
    create_biopython_residue,
    create_output_file,
    create_residues_list,
    select_residues,
)


class ExtractResidues(BiobbObject):
    """
    | biobb_structure_utils ExtractResidues
    | Class to extract residues from a 3D structure using Biopython.
    | Extracts a list of residues from a 3D structure using Biopython.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_heteroatom.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        output_residues_path (str): Output residues file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_residues.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **residues** (*list*) - (None) List of comma separated res_id (will extract all residues that match the res_id) or list of dictionaries with the name | res_id  | chain | model of the residues to be extracted. Format: [{"name": "HIS", "res_id": "72", "chain": "A", "model": "1"}]. The res_id of a residue with an insertion code includes the code ("62A").
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.extract_residues import extract_residues
            prop = {
                'residues': [
                    {
                        'name': 'HIS',
                        'res_id': '72',
                        'chain': 'A',
                        'model': '1'
                    }
                ]
            }
            extract_residues(input_structure_path='/path/to/myStructure.pdb',
                             output_residues_path='/path/to/newResidues.pdb',
                             properties=prop)

    Info:
        * wrapped_software:
            * name: In house using Biopython
            * version: >=1.79
            * license: other
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self, input_structure_path: str, output_residues_path: str, properties: Optional[dict] = None, **kwargs
    ) -> None:
        super().__init__(**locals())

        # Properties specific for BB
        self.residues = fu.str_to_list(self.residues)

    def run(self) -> None:
        """Execute the :class:`ExtractResidues <utils.extract_residues.ExtractResidues>` utils.extract_residues.ExtractResidues object."""

        # Business code
        # get list of Residues from properties
        list_residues = create_residues_list(self.residues)

        # load input into BioPython structure
        structure = PDBParser(QUIET=True).get_structure(
            "structure", self.sandbox_file("input_structure_path")
        )

        # get desired residues
        new_structure = [create_biopython_residue(residue) for residue in select_residues(structure, list_residues)]

        # if not residues found in structure, raise exit
        if not new_structure:
            fu.log(
                self.__class__.__name__ + ": The residues given by user were not found in input structure",
                self.out_log,
            )
            raise SystemExit(
                self.__class__.__name__ + ": The residues given by user were not found in input structure"
            )

        create_output_file(
            2,
            self.sandbox_file("input_structure_path"),
            new_structure,
            self.sandbox_file("output_residues_path"),
            self.out_log,
        )

        self.return_code = 0


extract_residues = launcher(ExtractResidues)

if __name__ == "__main__":
    ExtractResidues.main()
