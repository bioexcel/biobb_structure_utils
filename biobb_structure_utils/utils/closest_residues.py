#!/usr/bin/env python3

"""Module containing the ClosestResidues class and the command line interface."""

import argparse
from typing import Optional

import Bio.PDB
from biobb_common.configuration import settings
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger

from biobb_structure_utils.utils.common import (
    _from_string_to_list,
    check_input_path,
    check_output_path,
    create_biopython_residue,
    create_output_file,
    create_residues_list,
)


class ClosestResidues(BiobbObject):
    """
    | biobb_structure_utils ClosestResidues
    | Class to search closest residues from a 3D structure using Biopython.
    | Return all residues that have at least one atom within radius of center from a list of given residues.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/2vgb.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        output_residues_path (str): Output molcules file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_closest_residues.pdb>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **residues** (*list*) - (None) List of comma separated res_id or list of dictionaries with the name | res_id  | chain | model of the residues to find the closest neighbours. Format: [{"name": "HIS", "res_id": "72", "chain": "A", "model": "1"}].
            * **radius** (*float*) - (5) Distance in Ångströms to neighbours of the given list of residues.
            * **preserve_target** (*bool*) - (True) Whether or not to preserve the target residues in the output structure.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.closest_residues import closest_residues
            prop = {
                'residues': [
                    {
                        'name': 'HIS',
                        'res_id': '72',
                        'chain': 'A',
                        'model': '1'
                    }
                ],
                'radius': 5,
                'preserve_target': False
            }
            closest_residues(input_structure_path='/path/to/myStructure.pdb',
                             output_residues_path='/path/to/newResidues.pdb',
                             properties=prop)

    Info:
        * wrapped_software:
            * name: In house using Biopython
            * version: >=1.79
            * license: other
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl

    """

    def __init__(
        self, input_structure_path, output_residues_path, properties=None, **kwargs
    ) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_structure_path": input_structure_path},
            "out": {"output_residues_path": output_residues_path},
        }

        # Properties specific for BB
        self.residues = _from_string_to_list(properties.get("residues", []))
        self.radius = properties.get("radius", 5)
        self.preserve_target = properties.get("preserve_target", True)
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`ClosestResidues <utils.closest_residues.ClosestResidues>` utils.closest_residues.ClosestResidues object."""

        self.io_dict["in"]["input_structure_path"] = check_input_path(
            self.io_dict["in"]["input_structure_path"],
            self.out_log,
            self.__class__.__name__,
        )
        self.io_dict["out"]["output_residues_path"] = check_output_path(
            self.io_dict["out"]["output_residues_path"],
            self.out_log,
            self.__class__.__name__,
        )

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Business code
        # get list of Residues from properties
        list_residues = create_residues_list(self.residues, self.out_log)

        # load input into BioPython structure
        structure = Bio.PDB.PDBParser(QUIET=True).get_structure(
            "structure", self.stage_io_dict["in"]["input_structure_path"]
        )

        str_residues = []
        # format selected residues
        for residue in structure.get_residues():
            r = create_biopython_residue(residue)
            if list_residues:
                for res in list_residues:
                    match = True
                    for code in res["code"]:
                        if res[code].strip() != r[code].strip():
                            match = False
                            break
                    if match:
                        str_residues.append(r)
            else:
                str_residues.append(r)

        # get target residues in BioPython format
        target_residues = []
        for sr in str_residues:
            # try for residues, if exception, try as HETATM
            try:
                target_residues.append(
                    structure[int(sr["model"]) - 1][sr["chain"]][int(sr["res_id"])]
                )
            except KeyError:
                target_residues.append(
                    structure[int(sr["model"]) - 1][sr["chain"]][
                        "H_" + sr["name"], int(sr["res_id"]), " "
                    ]
                )
            except Exception:
                fu.log(
                    self.__class__.__name__ + ": Unable to find residue %s",
                    sr["res_id"],
                    self.out_log,
                )

        # get all atoms from target_residues
        target_atoms = Bio.PDB.Selection.unfold_entities(target_residues, "A")
        # get all atoms of input structure
        all_atoms = Bio.PDB.Selection.unfold_entities(structure, "A")
        # generate NeighborSearch object
        ns = Bio.PDB.NeighborSearch(all_atoms)
        # set comprehension list
        nearby_residues = {
            res
            for center_atom in target_atoms
            for res in ns.search(center_atom.coord, self.radius, "R")
        }

        # format nearby residues to pure python objects
        neighbor_residues = []
        for residue in nearby_residues:
            r = create_biopython_residue(residue)
            neighbor_residues.append(r)

        # if preserve_target == False, don't add the residues of self.residues to the final structure
        if not self.preserve_target:
            neighbor_residues = [x for x in neighbor_residues if x not in str_residues]

        fu.log("Found %d nearby residues" % len(neighbor_residues), self.out_log)

        if len(neighbor_residues) == 0:
            fu.log(
                self.__class__.__name__ + ": No neighbour residues found, exiting",
                self.out_log,
            )
            raise SystemExit(
                self.__class__.__name__ + ": No neighbour residues found, exiting"
            )

        create_output_file(
            0,
            self.stage_io_dict["in"]["input_structure_path"],
            neighbor_residues,
            self.stage_io_dict["out"]["output_residues_path"],
            self.out_log,
        )

        self.return_code = 0

        # Copy files to host
        self.copy_to_host()

        # Remove temporal files
        self.tmp_files.append(self.stage_io_dict.get("unique_dir", ""))
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def closest_residues(
    input_structure_path: str,
    output_residues_path: str,
    properties: Optional[dict] = None,
    **kwargs,
) -> int:
    """Execute the :class:`ClosestResidues <utils.closest_residues.ClosestResidues>` class and
    execute the :meth:`launch() <utils.closest_residues.ClosestResidues.launch>` method."""

    return ClosestResidues(
        input_structure_path=input_structure_path,
        output_residues_path=output_residues_path,
        properties=properties,
        **kwargs,
    ).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(
        description="Search closest residues to a list of given residues.",
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
        "--output_residues_path",
        required=True,
        help="Output residues file path. Accepted formats: pdb.",
    )

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    closest_residues(
        input_structure_path=args.input_structure_path,
        output_residues_path=args.output_residues_path,
        properties=properties,
    )


if __name__ == "__main__":
    main()
