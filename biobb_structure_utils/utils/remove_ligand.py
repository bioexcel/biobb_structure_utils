#!/usr/bin/env python3

"""Module containing the RemoveLigand class and the command line interface."""
import argparse
import Bio.PDB
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_structure_utils.gro_lib.gro import Gro
from biobb_structure_utils.utils.common import *

class RemoveLigand():
    """Class to remove the selected ligand atoms from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_1.pdb>`_. Accepted formats: pdb, gro.
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_apo_md_1.pdb>`_. Accepted formats: pdb, gro.
        properties (dic):
            | - **ligand** (*str*) - ("AQ4") Residue code of the ligand to be removed.
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    """

    def __init__(self, input_structure_path, 
                 output_structure_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = str(input_structure_path)
        self.output_structure_path = str(output_structure_path)

        # Properties specific for BB
        self.ligand = properties.get('ligand', 'AQ4')

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
        """Remove ligand atoms from the structure."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        #Restart if needed
        if self.restart:
            output_file_list = [self.output_structure_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step,  out_log, self.global_log)
                return 0

        extension = Path(self.input_structure_path).suffix.lower()
        if extension.lower() == '.gro':
            fu.log('GRO format detected, removing all atoms from residues named %s' % self.ligand, out_log)
            gro_st = Gro()
            gro_st.read_gro_file(self.input_structure_path)
            gro_st.remove_residues([self.ligand])
            gro_st.write_gro_file(self.output_structure_path)

        else:
            fu.log('PDB format detected, removing all atoms from residues named %s' % self.ligand, out_log)
            # Direct aproach solution implemented to avoid the issues presented in commit message (c92aab9604a6a31d13f4170ff47b231df0a588ef)
            # with the Biopython library
            with open(self.input_structure_path, "r") as input_pdb, open(self.output_structure_path, "w") as output_pdb:
                for line in input_pdb:
                    if len(line) > 19 and self.ligand.lower() in line[17:20].lower():
                        continue
                    output_pdb.write(line)


        if self.remove_tmp:
            fu.rm_file_list(tmp_files)

        return 0

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Remove the selected ligand atoms from a 3D structure.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_structure_path', required=True, help="Input structure file name")
    required_args.add_argument('-o', '--output_structure_path', required=True, help="Output structure file name")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    RemoveLigand(input_structure_path=args.input_structure_path, output_structure_path=args.output_structure_path, 
                 properties=properties).launch()

if __name__ == '__main__':
    main()
