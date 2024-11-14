#!/usr/bin/env python3

"""Module containing the SortGroResidues class and the command line interface."""

import argparse
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.gro_lib.gro import Gro
from biobb_structure_utils.utils.common import _from_string_to_list


class SortGroResidues(BiobbObject):
    """
    | biobb_structure_utils SortGroResidues
    | Class to sort the selected residues from a GRO 3D structure.
    | Sorts the selected residues from a GRO 3D structure.

    Args:
        input_gro_path (str): Input GRO file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_1.gro>`_. Accepted formats: gro (edam:format_2033).
        output_gro_path (str): Output sorted GRO file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_aq4_md_sorted.gro>`_. Accepted formats: gro (edam:format_2033).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **residue_name_list** (*list*) - (["NA", "CL", "SOL"]) Ordered residue name list.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.sort_gro_residues import sort_gro_residues
            prop = {
                'residue_name_list': ['NA', 'CL', 'SOL']
            }
            sort_gro_residues(input_gro_path='/path/to/myInputStr.gro',
                            output_gro_path='/path/to/newStructure.gro',
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
        self, input_gro_path, output_gro_path, properties=None, **kwargs
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_gro_path": input_gro_path},
            "out": {"output_gro_path": output_gro_path},
        }

        # Properties specific for BB
        self.residue_name_list = _from_string_to_list(
            properties.get("residue_name_list", ["NA", "CL", "SOL"])
        )

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`SortGroResidues <utils.sort_gro_residues.SortGroResidues>` utils.sort_gro_residues.SortGroResidues object."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Business code
        in_gro = Gro()
        in_gro.read_gro_file(self.stage_io_dict["in"]["input_gro_path"])
        in_gro.sort_residues2(self.residue_name_list)
        in_gro.write_gro_file(self.stage_io_dict["out"]["output_gro_path"])
        self.return_code = 0
        ##########

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.append(self.stage_io_dict.get("unique_dir", ""))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def sort_gro_residues(
    input_gro_path: str,
    output_gro_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`SortGroResidues <utils.sort_gro_residues.SortGroResidues>` class and
    execute the :meth:`launch() <utils.sort_gro_residues.SortGroResidues.launch>` method."""

    return SortGroResidues(
        input_gro_path=input_gro_path,
        output_gro_path=output_gro_path,
        properties=properties,
        **kwargs,
    ).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Renumber atoms and residues from a 3D structure.",
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
        "-i", "--input_gro_path", required=True, help="Input GRO file name"
    )
    required_args.add_argument(
        "-o", "--output_gro_path", required=True, help="Output sorted GRO file name"
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    sort_gro_residues(
        input_gro_path=args.input_gro_path,
        output_gro_path=args.output_gro_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
