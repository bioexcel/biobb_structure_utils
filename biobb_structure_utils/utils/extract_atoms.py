#!/usr/bin/env python3

"""Module containing the ExtractAtoms class and the command line interface."""

import argparse
import re
from pathlib import Path
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.gro_lib.gro import Gro
from biobb_structure_utils.utils.common import PDB_SERIAL_RECORDS


class ExtractAtoms(BiobbObject):
    """
    | biobb_structure_utils ExtractAtoms
    | Class to extract atoms from a 3D structure.
    | Extracts all atoms from a 3D structure that match a regular expression pattern.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/2vgb.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/OE2_atoms.pdb>`_. Accepted formats: pdb (edam:format_1476), gro (edam:format_2033).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **regular_expression_pattern** (*str*) - ("^D") Python style regular expression matching the selected atom names.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.extract_atoms import extract_atoms
            prop = {
                'regular_expression_pattern': '^D'
            }
            extract_atoms(input_structure_path='/path/to/myStructure.pdb',
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
        self.regular_expression_pattern = properties.get(
            "regular_expression_pattern", "^D"
        )

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`ExtractAtoms <utils.extract_atoms.ExtractAtoms>` utils.extract_atoms.ExtractAtoms object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Business code
        extension = Path(self.io_dict["in"]["input_structure_path"]).suffix.lower()
        if extension.lower() == ".gro":
            fu.log(
                "GRO format detected, extracting all atoms matching %s"
                % self.regular_expression_pattern,
                self.out_log,
            )
            gro_st = Gro()
            gro_st.read_gro_file(self.io_dict["in"]["input_structure_path"])
            gro_st.select_atoms(self.regular_expression_pattern)
            if gro_st.num_of_atoms:
                fu.log(
                    "%d atoms found writting GRO file" % gro_st.num_of_atoms,
                    self.out_log,
                    self.global_log,
                )
                gro_st.write_gro_file(self.io_dict["out"]["output_structure_path"])
            else:
                fu.log(
                    "No matching atoms found writting empty GRO file",
                    self.out_log,
                    self.global_log,
                )
                open(self.io_dict["out"]["output_structure_path"], "w").close()

        else:
            fu.log(
                "PDB format detected, extracting all atoms matching %s"
                % self.regular_expression_pattern,
                self.out_log,
            )
            # Direct aproach solution implemented to avoid the
            # issues presented in commit message (c92aab9604a6a31d13f4170ff47b231df0a588ef)
            # with the Biopython library
            atoms_match_cont = 0
            with open(
                self.io_dict["in"]["input_structure_path"], "r"
            ) as input_pdb, open(
                self.io_dict["out"]["output_structure_path"], "w"
            ) as output_pdb:
                for line in input_pdb:
                    record = line[:6].upper().strip()
                    if (
                        len(line) > 10 and record in PDB_SERIAL_RECORDS
                    ):  # Avoid MODEL, ENDMDL records and empty lines
                        pdb_atom_name = line[12:16].strip()
                        if re.search(self.regular_expression_pattern, pdb_atom_name):
                            atoms_match_cont += 1
                            output_pdb.write(line)
            if atoms_match_cont:
                fu.log(
                    "%d atoms found writting PDB file" % atoms_match_cont,
                    self.out_log,
                    self.global_log,
                )
            else:
                fu.log(
                    "No matching atoms found writting empty PDB file",
                    self.out_log,
                    self.global_log,
                )
        self.return_code = 0
        ##########

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.append(self.stage_io_dict.get("unique_dir", ""))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def extract_atoms(
    input_structure_path: str,
    output_structure_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`ExtractAtoms <utils.extract_atoms.ExtractAtoms>` class and
    execute the :meth:`launch() <utils.extract_atoms.ExtractAtoms.launch>` method."""

    return ExtractAtoms(
        input_structure_path=input_structure_path,
        output_structure_path=output_structure_path,
        properties=properties,
        **kwargs,
    ).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Remove the selected ligand atoms from a 3D structure.",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )
    parser.add_argument(
        "-c",
        "--config",
        required=False,
        help="This file can be a YAML file, JSON file or JSON string",
    )

    # Specific args of each building block
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-i", "--input_structure_path", required=True, help="Input structure file name"
    )
    required_args.add_argument(
        "-o",
        "--output_structure_path",
        required=True,
        help="Output structure file name",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    extract_atoms(
        input_structure_path=args.input_structure_path,
        output_structure_path=args.output_structure_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
