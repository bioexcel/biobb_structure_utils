#!/usr/bin/env python3

"""Module containing the RemovePdbWater class and the command line interface."""

import argparse
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger


class RemovePdbWater(BiobbObject):
    """
    | biobb_structure_utils RemovePdbWater
    | This class is a wrapper of the Structure Checking tool to remove water molecules from PDB 3D structures.
    | Wrapper for the `Structure Checking <https://github.com/bioexcel/biobb_structure_checking>`_ tool to remove water molecules from PDB 3D structures.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_WAT.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_apo_no_wat.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **binary_path** (*string*) - ("check_structure") path to the check_structure application
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.remove_pdb_water import remove_pdb_water
            prop = { }
            remove_pdb_water(input_pdb_path='/path/to/myStructure.pdb',
                            output_pdb_path='/path/to/newStructure.pdb',
                            properties=prop)

    Info:
        * wrapped_software:
            * name: Structure Checking from MDWeb
            * version: >=3.0.3
            * license: Apache-2.0
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self, input_pdb_path, output_pdb_path, properties=None, **kwargs
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_pdb_path": input_pdb_path},
            "out": {"output_pdb_path": output_pdb_path},
        }

        # Properties specific for BB
        self.binary_path = properties.get("binary_path", "check_structure")

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`RemovePdbWater <utils.remove_pdb_water.RemovePdbWater>` utils.remove_pdb_water.RemovePdbWater object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        self.cmd = [
            self.binary_path,
            "-i",
            self.stage_io_dict["in"]["input_pdb_path"],
            "-o",
            self.stage_io_dict["out"]["output_pdb_path"],
            "--force_save",
            "water",
            "--remove",
            "yes",
        ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.append(self.stage_io_dict.get("unique_dir", ""))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def remove_pdb_water(
    input_pdb_path: str,
    output_pdb_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`RemovePdbWater <utils.remove_pdb_water.RemovePdbWater>` class and
    execute the :meth:`launch() <utils.remove_pdb_water.RemovePdbWater.launch>` method."""

    return RemovePdbWater(
        input_pdb_path=input_pdb_path,
        output_pdb_path=output_pdb_path,
        properties=properties,
        **kwargs,
    ).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Remove the water molecules from a PDB 3D structure.",
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
        "-i", "--input_pdb_path", required=True, help="Input pdb file name"
    )
    required_args.add_argument(
        "-o", "--output_pdb_path", required=True, help="Output pdb file name"
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    remove_pdb_water(
        input_pdb_path=args.input_pdb_path,
        output_pdb_path=args.output_pdb_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
