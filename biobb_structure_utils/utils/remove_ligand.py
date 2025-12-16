#!/usr/bin/env python3

"""Module containing the RemoveLigand class and the command line interface."""
from typing import Optional
from pathlib import Path
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.gro_lib.gro import Gro


class RemoveLigand(BiobbObject):
    """
    | biobb_structure_utils RemoveLigand
    | Class to remove the selected ligand atoms from a 3D structure.
    | Remove the selected ligand atoms from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_1.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_apo_md_1.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **ligand** (*str*) - ("AQ4") Residue code of the ligand to be removed.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.remove_ligand import remove_ligand
            prop = {
                'ligand': 'AQ4'
            }
            remove_ligand(input_structure_path='/path/to/myStructure.pdb',
                        output_structure_path='/path/to/newStructure.pdb',
                        properties=prop)

    Info:
        * wrapped_software:
            * name: In house
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self, input_structure_path, output_structure_path, properties=None, **kwargs
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure_path": input_structure_path},
            "out": {"output_structure_path": output_structure_path},
        }

        # Properties specific for BB
        self.ligand = properties.get("ligand", "AQ4")

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`RemoveLigand <utils.remove_ligand.RemoveLigand>` utils.remove_ligand.RemoveLigand object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Business code
        extension = Path(
            self.stage_io_dict["in"]["input_structure_path"]
        ).suffix.lower()
        if extension.lower() == ".gro":
            fu.log(
                "GRO format detected, removing all atoms from residues named %s"
                % self.ligand,
                self.out_log,
            )
            gro_st = Gro()
            gro_st.read_gro_file(self.stage_io_dict["in"]["input_structure_path"])
            gro_st.remove_residues([self.ligand])
            gro_st.write_gro_file(self.stage_io_dict["out"]["output_structure_path"])

        else:
            fu.log(
                "PDB format detected, removing all atoms from residues named %s"
                % self.ligand,
                self.out_log,
            )
            # Direct aproach solution implemented to avoid the issues
            # presented in commit message (c92aab9604a6a31d13f4170ff47b231df0a588ef)
            # with the Biopython library
            with open(
                self.stage_io_dict["in"]["input_structure_path"], "r"
            ) as input_pdb, open(
                self.stage_io_dict["out"]["output_structure_path"], "w"
            ) as output_pdb:
                for line in input_pdb:
                    if len(line) > 19 and self.ligand.lower() in line[17:20].lower():
                        continue
                    output_pdb.write(line)

        self.return_code = 0
        ##########

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def remove_ligand(
    input_structure_path: str,
    output_structure_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Create the :class:`RemoveLigand <utils.remove_ligand.RemoveLigand>` class and
    execute the :meth:`launch() <utils.remove_ligand.RemoveLigand.launch>` method."""
    return RemoveLigand(**dict(locals())).launch()


remove_ligand.__doc__ = RemoveLigand.__doc__
main = RemoveLigand.get_main(remove_ligand, "Remove the selected ligand atoms from a 3D structure.")

if __name__ == "__main__":
    main()
