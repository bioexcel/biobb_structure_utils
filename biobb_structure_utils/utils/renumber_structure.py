#!/usr/bin/env python3

"""Module containing the RenumberStructure class and the command line interface."""
import os
import json
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_structure_utils.gro_lib.gro import Gro
from biobb_structure_utils.utils.common import *


class RenumberStructure:
    """Class to renumber atomic indexes from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cl3.noH.pdb>`_. Accepted formats: pdb, gro.
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/renum_cl3_noH.pdb>`_. Accepted formats: pdb, gro.
        output_mapping_json_path (str): Output mapping json file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/cl3_output_mapping_json_path.json>`_. Accepted formats: json.
        properties (dic):
            | - **renumber_residues** (*bool*) - (True) Residue code of the ligand to be removed.
            | - **renumber_residues_per_chain** (*bool*) - (True) Restart residue enumeration every time a new chain is detected.
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_structure_path, 
                 output_structure_path, output_mapping_json_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = str(input_structure_path)
        self.output_structure_path = str(output_structure_path)
        self.output_mapping_json_path = str(output_mapping_json_path)

        # Properties specific for BB
        self.renumber_residues = properties.get('renumber_residues', True)
        self.renumber_residues_per_chain = properties.get('renumber_residues_per_chain', True)

        # Common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # Check the properties
        fu.check_properties(self, properties)

    @launchlogger
    def launch(self) -> int:
        """renumber atoms in the structure."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # Restart if needed
        if self.restart:
            output_file_list = [self.output_structure_path, self.output_mapping_json_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        extension = Path(self.input_structure_path).suffix.lower()
        if extension.lower() == '.gro':
            fu.log('GRO format detected, reenumerating atoms', out_log)
            gro_st = Gro()
            gro_st.read_gro_file(self.input_structure_path)
            residue_mapping, atom_mapping = gro_st.renumber_atoms(renumber_residues=self.renumber_residues, renumber_residues_per_chain=self.renumber_residues_per_chain)
            gro_st.write_gro_file(self.output_structure_path)

        else:
            fu.log('PDB format detected, reenumerating atoms', out_log)
            atom_mapping = {}
            atom_count = 0
            residue_mapping = {}
            residue_count = 0
            with open(self.input_structure_path, "r") as input_pdb, open(self.output_structure_path, "w") as output_pdb:
                for line in input_pdb:
                    record = line[:6].upper().strip()
                    if len(line) > 10 and record in PDB_SERIAL_RECORDS:  # Avoid MODEL, ENDMDL records and empty lines
                        # Renumbering atoms
                        pdb_atom_number = line[6:11].strip()
                        if not atom_mapping.get(pdb_atom_number): # ANISOU records should have the same numeration as ATOM records
                            atom_count += 1
                            atom_mapping[pdb_atom_number] = str(atom_count)
                        line = line[:6]+'{: >5d}'.format(atom_count)+line[11:]
                        # Renumbering residues
                        if self.renumber_residues:
                            chain = line[21]
                            pdb_residue_number = line[22:26].strip()
                            if not residue_mapping.get(chain):
                                residue_mapping[chain] = {}
                                if self.renumber_residues_per_chain:
                                    residue_count = 0
                            if not residue_mapping[chain].get(pdb_residue_number):
                                residue_count += 1
                                residue_mapping[chain][pdb_residue_number] = str(residue_count)
                            line = line[:22] + '{: >4d}'.format(residue_count) + line[26:]
                    output_pdb.write(line)

        with open(self.output_mapping_json_path, "w") as output_json:
            output_json.write(json.dumps({'residues': residue_mapping, 'atoms': atom_mapping}))

        if self.remove_tmp:
            fu.rm_file_list(tmp_files)

        return 0

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Renumber atoms and residues from a 3D structure.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_structure_path', required=True, help="Input structure file name")
    required_args.add_argument('-o', '--output_structure_path', required=True, help="Output structure file name")
    required_args.add_argument('-j', '--output_mapping_json_path', required=True, help="Output mapping json file name")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    RenumberStructure(input_structure_path=args.input_structure_path, output_structure_path=args.output_structure_path, 
                      output_mapping_json_path=args.output_mapping_json_path, 
                      properties=properties).launch()

if __name__ == '__main__':
    main()
