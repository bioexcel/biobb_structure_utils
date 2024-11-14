#!/usr/bin/env python3

"""Module containing the ExtractMolecule class and the command line interface."""

import argparse
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.utils.common import (
    _from_string_to_list,
    check_input_path,
    check_output_path,
)


class ExtractMolecule(BiobbObject):
    """
    | biobb_structure_utils ExtractMolecule
    | This class is a wrapper of the Structure Checking tool to extract a molecule from a 3D structure.
    | Wrapper for the `Structure Checking <https://github.com/bioexcel/biobb_structure_checking>`_ tool to extract a molecule from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_molecule.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        output_molecule_path (str): Output molecule file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_molecule.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **molecule_type** (*string*) - ("all") type of molecule to be extracted. If all, only waters and ligands will be removed from the original structure. Values: all, protein, na, dna, rna, chains.
            * **chains** (*list*) - (None) if chains selected in **molecule_type**, specify them here, e.g: ["A", "C", "N"].
            * **binary_path** (*string*) - ("check_structure") path to the check_structure application
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.extract_molecule import extract_molecule
            prop = {
                'molecule_type': 'chains',
                'chains': ['A', 'N', 'F']
            }
            extract_molecule(input_structure_path='/path/to/myStructure.pdb',
                            output_molecule_path='/path/to/newMolecule.pdb',
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
        self, input_structure_path, output_molecule_path, properties=None, **kwargs
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure_path": input_structure_path},
            "out": {"output_molecule_path": output_molecule_path},
        }

        # Properties specific for BB
        self.molecule_type = properties.get("molecule_type", "all")
        self.chains = _from_string_to_list(properties.get("chains", []))
        self.binary_path = properties.get("binary_path", "check_structure")
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    def create_command_list(self, command_list_path):
        """Creates a command list file as a input for structure checking"""
        instructions_list = ["ligands --remove All", "water --remove Yes"]

        if self.molecule_type != "all":
            if self.molecule_type == "chains":
                instructions_list.append("chains --select " + ",".join(self.chains))
            else:
                instructions_list.append("chains --select " + self.molecule_type)

        with open(command_list_path, "w") as clp:
            for line in instructions_list:
                clp.write(line.strip() + "\n")

        return command_list_path

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`ExtractMolecule <utils.extract_molecule.ExtractMolecule>` utils.extract_molecule.ExtractMolecule object."""

        self.io_dict["in"]["input_structure_path"] = check_input_path(
            self.io_dict["in"]["input_structure_path"],
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["out"]["output_molecule_path"] = check_output_path(
            self.io_dict["out"]["output_molecule_path"],
            self.out_log,
            self.__class__.__name__,
        )

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # create temporary folder
        tmp_folder = fu.create_unique_dir()
        fu.log("Creating %s temporary folder" % tmp_folder, self.out_log)

        # create command list file
        command_list_file = self.create_command_list(tmp_folder + "/extract_prot.lst")

        # run command line
        self.cmd = [
            self.binary_path,
            "-i",
            self.io_dict["in"]["input_structure_path"],
            "-o",
            self.io_dict["out"]["output_molecule_path"],
            "--force_save",
            "--non_interactive",
            "command_list",
            "--list",
            command_list_file,
        ]

        # Run Biobb block
        self.run_biobb()

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.extend([self.stage_io_dict.get("unique_dir", ""), tmp_folder])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def extract_molecule(
    input_structure_path: str,
    output_molecule_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`ExtractMolecule <utils.extract_molecule.ExtractMolecule>` class and
    execute the :meth:`launch() <utils.extract_molecule.ExtractMolecule.launch>` method."""

    return ExtractMolecule(
        input_structure_path=input_structure_path,
        output_molecule_path=output_molecule_path,
        properties=properties,
        **kwargs,
    ).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Extract a molecule from a 3D structure.",
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
        "--output_molecule_path",
        required=True,
        help="Output heteroatom file path. Accepted formats: pdb.",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    extract_molecule(
        input_structure_path=args.input_structure_path,
        output_molecule_path=args.output_molecule_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
