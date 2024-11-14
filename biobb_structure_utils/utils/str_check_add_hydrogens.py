#!/usr/bin/env python3

"""Module containing the StrCheckAddHydrogens class and the command line interface."""

import argparse
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.utils.common import (
    check_input_path,
    check_output_end,
    check_output_path_pdbqt,
)


class StrCheckAddHydrogens(BiobbObject):
    """
    | biobb_structure_utils StrCheckAddHydrogens
    | This class is a wrapper of the Structure Checking tool to add hydrogens to a 3D structure.
    | Wrapper for the `Structure Checking <https://github.com/bioexcel/biobb_structure_checking>`_ tool to add hydrogens to a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/str_no_H.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_str_H.pdbqt>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **charges** (*bool*) - (False) Whether or not to add charges to the output file. If True the output is in PDBQT format.
            * **mode** (*string*) - (auto) Selection mode. Values: auto, list, ph
            * **ph** (*float*) - (7.4) [0~14|0.1] Add hydrogens appropriate for pH. Only in case mode ph selected.
            * **list** (*string*) - ("") List of residues to modify separated by commas (i.e HISA234HID,HISB33HIE). Only in case mode list selected.
            * **keep_canonical_resnames** (*bool*) - (False) Whether or not keep canonical residue names
            * **binary_path** (*string*) - ("check_structure") path to the check_structure application
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.str_check_add_hydrogens import str_check_add_hydrogens
            prop = {
                'charges': False,
                'mode': 'auto'
            }
            str_check_add_hydrogens(input_structure_path='/path/to/myInputStr.pdb',
                                    output_structure_path='/path/to/newStructure.pdb',
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
        self.binary_path = properties.get("binary_path", "check_structure")
        self.charges = properties.get("charges", False)
        self.mode = properties.get("mode", "auto")
        self.ph = properties.get("ph", 7.4)
        self.list = properties.get("list", "")
        self.keep_canonical_resnames = properties.get("keep_canonical_resnames", False)
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`StrCheckAddHydrogens <utils.str_check_add_hydrogens.StrCheckAddHydrogens>` utils.str_check_add_hydrogens.StrCheckAddHydrogens object."""

        self.io_dict["in"]["input_structure_path"] = check_input_path(
            self.io_dict["in"]["input_structure_path"],
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["out"]["output_structure_path"] = check_output_path_pdbqt(
            self.io_dict["out"]["output_structure_path"],
            self.out_log,
            self.__class__.__name__,
        )

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        self.cmd = [
            self.binary_path,
            "-i",
            self.stage_io_dict["in"]["input_structure_path"],
            "-o",
            self.stage_io_dict["out"]["output_structure_path"],
            "--non_interactive",
            "--force_save",
        ]

        if self.keep_canonical_resnames:
            self.cmd.append("--keep_canonical_resnames")

        self.cmd.extend(["command_list", "--list", "'add_hydrogen"])

        if self.charges:
            self.cmd.append("--add_charges")
            self.cmd.append("ADT")

        if self.mode:
            self.cmd.extend(["--add_mode", self.mode])
            if self.mode == "ph":
                self.cmd.extend(["--pH", self.ph])
            if self.mode == "list":
                self.cmd.extend(["--list", self.list])
        else:
            self.cmd.extend(["--add_mode", "None"])

        self.cmd.append("'")
        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        check_output_end(self.io_dict["out"]["output_structure_path"], self.out_log)

        # Remove temporal files
        self.tmp_files.append(self.stage_io_dict.get("unique_dir", ""))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def str_check_add_hydrogens(
    input_structure_path: str,
    output_structure_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`StrCheckAddHydrogens <utils.str_check_add_hydrogens.StrCheckAddHydrogens>` class and
    execute the :meth:`launch() <utils.str_check_add_hydrogens.StrCheckAddHydrogens.launch>` method."""

    return StrCheckAddHydrogens(
        input_structure_path=input_structure_path,
        output_structure_path=output_structure_path,
        properties=properties,
        **kwargs,
    ).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Class to add hydrogens to a 3D structure.",
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
        "-i",
        "--input_structure_path",
        required=True,
        help="Input structure file path. Accepted formats: pdb.",
    )
    required_args.add_argument(
        "-o",
        "--output_structure_path",
        required=True,
        help="Output structure file path. Accepted formats: pdb, pdbqt.",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    str_check_add_hydrogens(
        input_structure_path=args.input_structure_path,
        output_structure_path=args.output_structure_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
