#!/usr/bin/env python3

"""Module containing the ExtractModel class and the command line interface."""
import shutil
from typing import Optional
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu


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

    def run(self) -> None:
        """Execute the :class:`ExtractModel <utils.extract_model.ExtractModel>` utils.extract_model.ExtractModel object."""

        # check if user has passed models properly
        models = check_format_models(self.models, self.out_log)

        if models == "All":
            shutil.copyfile(
                self.sandbox_file("input_structure_path"),
                self.sandbox_file("output_structure_path"),
            )
        else:
            # create temporary folder
            tmp_folder = fu.create_unique_dir()
            fu.log("Creating %s temporary folder" % tmp_folder, self.out_log)
            self.tmp_files.append(tmp_folder)

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
            with open(self.sandbox_file("output_structure_path"), "w") as outfile:
                for i, fname in enumerate(filenames):
                    with open(fname) as infile:
                        outfile.write("MODEL     " + "{:>4}".format(str(i + 1)) + "\n")
                        for line in infile:
                            if not line.startswith("END"):
                                outfile.write(line)
                            else:
                                outfile.write("ENDMDL\n")


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
    """Create the :class:`ExtractModel <utils.extract_model.ExtractModel>` class and
    execute the :meth:`launch() <utils.extract_model.ExtractModel.launch>` method."""
    return ExtractModel(**dict(locals())).launch()


extract_model.__doc__ = ExtractModel.__doc__
main = ExtractModel.get_main(extract_model, "Extract a model from a 3D structure.")

if __name__ == "__main__":
    main()
