#!/usr/bin/env python3

"""Module containing the RemoveMolecules class and the command line interface."""
from typing import Optional
from Bio.PDB.PDBParser import PDBParser
from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu

from biobb_structure_utils.utils.common import (
    _from_string_to_list,
    create_biopython_residue,
    create_output_file,
    create_residues_list,
)


class RemoveMolecules(BiobbObject):
    """
    | biobb_structure_utils RemoveMolecules
    | Class to remove molecules from a 3D structure using Biopython.
    | Remove a list of molecules from a 3D structure using Biopython.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/2vgb.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        output_molecules_path (str): Output molcules file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_remove_molecules.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **molecules** (*list*) - (None) List of comma separated res_id (will remove all molecules that match the res_id) or list of dictionaries with the name | res_id  | chain | model of the molecules to be removed. Format: [{"name": "HIS", "res_id": "72", "chain": "A", "model": "1"}].
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.remove_molecules import remove_molecules
            prop = {
                'molecules': [
                    {
                        'name': 'HIS',
                        'res_id': '72',
                        'chain': 'A',
                        'model': '1'
                    }
                ]
            }
            remove_molecules(input_structure_path='/path/to/myStructure.pdb',
                             output_molecules_path='/path/to/newMolecules.pdb',
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
        self, input_structure_path: str, output_molecules_path: str, properties: Optional[dict] = None, **kwargs
    ) -> None:
        super().__init__(**locals())

        # Properties specific for BB
        self.molecules = _from_string_to_list(self.molecules)

    def run(self) -> None:
        """Execute the :class:`RemoveMolecules <utils.remove_molecules.RemoveMolecules>` utils.remove_molecules.RemoveMolecules object."""

        # Business code
        # get list of Residues from properties
        list_residues = create_residues_list(self.molecules, self.out_log)

        # load input into BioPython structure
        structure = PDBParser(QUIET=True).get_structure(
            "structure", self.stage_io_dict["in"]["input_structure_path"]
        )

        remove_structure = []
        whole_structure = []
        # get desired residues
        for residue in structure.get_residues():
            r = create_biopython_residue(residue)
            whole_structure.append(r)
            if list_residues:
                for res in list_residues:
                    match = True
                    for code in res["code"]:
                        if res[code].strip() != r[code].strip():
                            match = False
                            break
                    if match:
                        remove_structure.append(r)
            else:
                remove_structure.append(r)

        # if not residues found in structure, raise exit
        if not remove_structure:
            fu.log(
                self.__class__.__name__ + ": The residues given by user were not found in input structure",
                self.out_log,
            )
            raise SystemExit(
                self.__class__.__name__ + ": The residues given by user were not found in input structure"
            )

        # substract residues (remove_structure) from whole_structure
        new_structure = [x for x in whole_structure if x not in remove_structure]

        create_output_file(
            0,
            self.stage_io_dict["in"]["input_structure_path"],
            new_structure,
            self.stage_io_dict["out"]["output_molecules_path"],
            self.out_log,
        )

        self.return_code = 0


remove_molecules = launcher(RemoveMolecules)

if __name__ == "__main__":
    RemoveMolecules.main()
