#!/usr/bin/env python3

"""Module containing the StructureCheck class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher
from biobb_common.tools import file_utils as fu


class StructureCheck(BiobbObject):
    """
    | biobb_structure_utils StructureCheck
    | This class is a wrapper of the Structure Checking tool to generate summary checking results on a json file.
    | Wrapper for the `Structure Checking <https://github.com/bioexcel/biobb_structure_checking>`_ tool to generate summary checking results on a json file from a given structure and a list of features.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/2vgb.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        output_summary_path (str): Output summary checking results. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/summary.json>`_. Accepted formats: json (edam:format_3464).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **features** (*list*) - (None) Features to summarize. If None, all the features will be computed. Values: models (multiple molecules or coordinate sets in a single file), chains (multiple chains in a single file), altloc (atom alternative conformation given an alternate location indicator and occupancy), metals (metals present in the structure), ligands (heteroatoms present in the structure), chiral (to say that a structure is chiral is to say that its mirror image is not the same as it self), getss (detect SS bonds or disulfides), cistransbck (detact cis/trans backbone), backbone (detect backbone breaks), amide (detect too close amides), clashes (detect clashes).
            * **binary_path** (*string*) - ("check_structure") path to the check_structure application
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.structure_check import structure_check
            prop = {
                'features': ['models', 'chains', 'ligands']
            }
            structure_check(input_structure_path='/path/to/myInputStr.pdb',
                            output_summary_path='/path/to/newSummary.json',
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
        self, input_structure_path: str, output_summary_path: str, properties: Optional[dict] = None, **kwargs
    ) -> None:
        super().__init__(**locals())

        # Properties specific for BB
        self.features = fu.str_to_list(self.features)

    def run(self) -> None:
        """Execute the :class:`StructureCheck <utils.structure_check.StructureCheck>` utils.structure_check.StructureCheck object."""

        tmp_folder = None

        if not self.features or self.features is None or self.features == "None":
            fu.log(
                "No features provided, all features will be computed: %s"
                % "models, chains, altloc, metals, ligands, chiral, getss, cistransbck, backbone, amide, clashes",
                self.out_log,
            )

            self.cmd = [
                self.binary_path,
                "-i",
                self.stage_io_dict["in"]["input_structure_path"],
                "--json",
                self.stage_io_dict["out"]["output_summary_path"],
                "--check_only",
                "--non_interactive",
                "checkall",
            ]
        else:
            fu.log("Computing features: %s" % ", ".join(self.features), self.out_log)

            # create temporary folder
            tmp_folder = self.create_tmp_dir(log=True)

            command_list = tmp_folder + "/command_list.lst"

            with open(command_list, "w") as f:
                for item in self.features:
                    f.write("%s\n" % item)

            self.cmd = [
                self.binary_path,
                "-i",
                self.stage_io_dict["in"]["input_structure_path"],
                "--json",
                self.stage_io_dict["out"]["output_summary_path"],
                "--check_only",
                "--non_interactive",
                "command_list",
                "--list",
                self.staged_path(command_list),
            ]

        # Run Biobb block
        self.run_biobb()


structure_check = launcher(StructureCheck)

if __name__ == "__main__":
    StructureCheck.main()
