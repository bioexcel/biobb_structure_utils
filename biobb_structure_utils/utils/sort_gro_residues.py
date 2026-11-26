#!/usr/bin/env python3

"""Module containing the SortGroResidues class and the command line interface."""

from typing import Optional

from biobb_common.generic.biobb_object import BiobbObject, launcher

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
        self, input_gro_path: str, output_gro_path: str, properties: Optional[dict] = None, **kwargs
    ) -> None:
        super().__init__(**locals())

        # Properties specific for BB
        self.residue_name_list = _from_string_to_list(
            self.residue_name_list
        )

    def run(self) -> None:
        """Execute the :class:`SortGroResidues <utils.sort_gro_residues.SortGroResidues>` utils.sort_gro_residues.SortGroResidues object."""

        # Business code
        in_gro = Gro()
        in_gro.read_gro_file(self.sandbox_file("input_gro_path"))
        in_gro.sort_residues2(self.residue_name_list)
        in_gro.write_gro_file(self.sandbox_file("output_gro_path"))
        self.return_code = 0
        ##########


sort_gro_residues = launcher(SortGroResidues)

if __name__ == "__main__":
    SortGroResidues.main()
