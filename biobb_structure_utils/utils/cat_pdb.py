#!/usr/bin/env python3

"""Module containing the CatPDB class and the command line interface."""

import argparse
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.utils.common import check_input_path, check_output_path


class CatPDB(BiobbObject):
    """
    | biobb_structure_utils CatPDB
    | Class to concat two PDB structures in a single PDB file.
    | Class to concat two PDB structures in a single PDB file.

    Args:
        input_structure1 (str): Input structure 1 file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cat_protein.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        input_structure2 (str): Input structure 2 file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cat_ligand.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        output_structure_path (str): Output protein file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_cat_pdb.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.cat_pdb import cat_pdb
            prop = { }
            cat_pdb(input_structure1='/path/to/myInputStr1.pdb',
                    input_structure2='/path/to/myInputStr2.pdb',
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
        self,
        input_structure1,
        input_structure2,
        output_structure_path,
        properties=None,
        **kwargs,
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {
                "input_structure1": input_structure1,
                "input_structure2": input_structure2,
            },
            "out": {"output_structure_path": output_structure_path},
        }

        # Properties specific for BB
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`CatPDB <utils.cat_pdb.CatPDB>` utils.cat_pdb.CatPDB object."""

        self.io_dict["in"]["input_structure1"] = check_input_path(
            self.io_dict["in"]["input_structure1"],
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["in"]["input_structure2"] = check_input_path(
            self.io_dict["in"]["input_structure2"],
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["out"]["output_structure_path"] = check_output_path(
            self.io_dict["out"]["output_structure_path"],
            self.out_log,
            self.__class__.__name__,
        )

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Business code
        filenames = [
            self.io_dict["in"]["input_structure1"],
            self.io_dict["in"]["input_structure2"],
        ]
        # check if self.input_structure1 and self.input_structure2 end with newline
        newline = [False, False]
        for idx, fname in enumerate(filenames):
            with open(fname, "rb") as fh:
                fh.seek(-2, 2)
                last = fh.readlines()[-1].decode()
                newline[idx] = "\n" in last

        # concat both input files and save them into output file
        with open(self.io_dict["out"]["output_structure_path"], "w") as outfile:
            for idx, fname in enumerate(filenames):
                with open(fname) as infile:
                    for line in infile:
                        if not line.startswith("END"):
                            outfile.write(line)
                    # if not ends in newline, add it
                    if not newline[idx]:
                        outfile.write("\n")
        self.return_code = 0

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.append(self.stage_io_dict.get("unique_dir", ""))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def cat_pdb(
    input_structure1: str,
    input_structure2: str,
    output_structure_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`CatPDB <utils.cat_pdb.CatPDB>` class and
    execute the :meth:`launch() <utils.cat_pdb.CatPDB.launch>` method."""

    return CatPDB(
        input_structure1=input_structure1,
        input_structure2=input_structure2,
        output_structure_path=output_structure_path,
        properties=properties,
        **kwargs,
    ).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Concat two PDB structures in a single PDB file.",
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
        "-i1",
        "--input_structure1",
        required=True,
        help="Input structure 1 file path. Accepted formats: pdb.",
    )
    required_args.add_argument(
        "-i2",
        "--input_structure2",
        required=True,
        help="Input structure 2 file path. Accepted formats: pdb.",
    )
    required_args.add_argument(
        "-o",
        "--output_structure_path",
        required=True,
        help="Output structure file path. Accepted formats: pdb.",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    cat_pdb(
        input_structure1=args.input_structure1,
        input_structure2=args.input_structure2,
        output_structure_path=args.output_structure_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
