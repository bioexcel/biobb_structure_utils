#!/usr/bin/env python3

"""Module containing the ExtractModel class and the command line interface."""

import argparse
import shutil
from typing import Optional

from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.utils.common import check_input_path, check_output_path


class ExtractModel(BiobbObject):
    """
    | biobb_structure_utils ExtractModel
    | This class is a wrapper of the Structure Checking tool to extract a model from a 3D structure.
    | Wrapper for the `Structure Checking <https://github.com/bioexcel/biobb_structure_checking>`_ tool to extract a model from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_model.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_model.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **models** (*list*) - (None) List of models to be extracted from the input_structure_path file. If empty, all the models of the structure will be returned.
            * **binary_path** (*string*) - ("check_structure") path to the check_structure application
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.extract_model import extract_model
            prop = {
                'models': [ 1, 2, 3 ]
            }
            extract_model(input_structure_path='/path/to/myStructure.pdb',
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
        self.models = properties.get("models", [])
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`ExtractModel <utils.extract_model.ExtractModel>` utils.extract_model.ExtractModel object."""

        self.io_dict["in"]["input_structure_path"] = check_input_path(
            self.io_dict["in"]["input_structure_path"],
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

        # check if user has passed models properly
        models = check_format_models(self.models, self.out_log)

        if models == "All":
            shutil.copyfile(
                self.io_dict["in"]["input_structure_path"],
                self.io_dict["out"]["output_structure_path"],
            )

            return 0
        else:
            # create temporary folder
            tmp_folder = fu.create_unique_dir()
            fu.log("Creating %s temporary folder" % tmp_folder, self.out_log)

            filenames = []

            for model in models:
                tmp_file = tmp_folder + "/model" + str(model) + ".pdb"

                self.cmd = [
                    self.binary_path,
                    "-i",
                    self.stage_io_dict["in"]["input_structure_path"],
                    "-o",
                    tmp_file,
                    "--force_save",
                    "models",
                    "--select",
                    str(model),
                ]

                # Run Biobb block
                self.run_biobb()

                filenames.append(tmp_file)

            # concat tmp_file and save them into output file
            with open(self.io_dict["out"]["output_structure_path"], "w") as outfile:
                for i, fname in enumerate(filenames):
                    with open(fname) as infile:
                        outfile.write("MODEL     " + "{:>4}".format(str(i + 1)) + "\n")
                        for line in infile:
                            if not line.startswith("END"):
                                outfile.write(line)
                            else:
                                outfile.write("ENDMDL\n")

            # Copy files to host
            self.copy_to_host()

            # Remove temporal files
            self.tmp_files.extend(
                [self.stage_io_dict.get("unique_dir", ""), tmp_folder]
            )
            self.remove_tmp_files()

            self.check_arguments(output_files_created=True, raise_exception=False)

            return self.return_code


def check_format_models(models, out_log):
    """Check format of models list"""
    if not models:
        fu.log("Empty models parameter, all models will be returned.", out_log)
        return "All"

    if not isinstance(models, list):
        fu.log(
            "Incorrect format of models parameter, all models will be returned.",
            out_log,
        )
        return "All"

    return models


def extract_model(
    input_structure_path: str,
    output_structure_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`ExtractModel <utils.extract_model.ExtractModel>` class and
    execute the :meth:`launch() <utils.extract_model.ExtractModel.launch>` method."""

    return ExtractModel(
        input_structure_path=input_structure_path,
        output_structure_path=output_structure_path,
        properties=properties,
        **kwargs,
    ).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Extract a model from a 3D structure.",
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
        help="Output structure file path. Accepted formats: pdb.",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    extract_model(
        input_structure_path=args.input_structure_path,
        output_structure_path=args.output_structure_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
