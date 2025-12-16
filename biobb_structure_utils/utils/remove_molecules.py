#!/usr/bin/env python3

"""Module containing the RemoveMolecules class and the command line interface."""
from typing import Optional
from Bio.PDB.PDBParser import PDBParser
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.utils.common import (
    _from_string_to_list,
    check_input_path,
    check_output_path,
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
        self, input_structure_path, output_molecules_path, properties=None, **kwargs
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure_path": input_structure_path},
            "out": {"output_molecules_path": output_molecules_path},
        }

        # Properties specific for BB
        self.molecules = _from_string_to_list(properties.get("molecules", []))
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`RemoveMolecules <utils.remove_molecules.RemoveMolecules>` utils.remove_molecules.RemoveMolecules object."""

        self.io_dict["in"]["input_structure_path"] = check_input_path(
            self.io_dict["in"]["input_structure_path"],
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["out"]["output_molecules_path"] = check_output_path(
            self.io_dict["out"]["output_molecules_path"],
            self.out_log,
            self.__class__.__name__,
        )

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

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

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def remove_molecules(
    input_structure_path: str,
    output_molecules_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create the :class:`RemoveMolecules <utils.remove_molecules.RemoveMolecules>` class and
    execute the :meth:`launch() <utils.remove_molecules.RemoveMolecules.launch>` method."""
    return RemoveMolecules(**dict(locals())).launch()


remove_molecules.__doc__ = RemoveMolecules.__doc__
main = RemoveMolecules.get_main(remove_molecules, "Removes a list of molecules from a 3D structure.")

if __name__ == "__main__":
    main()
