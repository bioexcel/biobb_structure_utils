#!/usr/bin/env python3

"""Module containing the RemovePdbWater class and the command line interface."""
import argparse
import Bio.PDB
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_structure_utils.utils.common import *


class RemovePdbWater:
    """Class to remove water molecules from PDB 3D structures.

    Args:
        input_pdb_path (str): Input PDB file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_WAT.pdb>`_. Accepted formats: pdb.
        output_pdb_path (str): Output PDB file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_apo_no_wat.pdb>`_. Accepted formats: pdb.
        properties (dic):
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    """

    def __init__(self, input_pdb_path, 
                 output_pdb_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_pdb_path = str(input_pdb_path)
        self.output_pdb_path = str(output_pdb_path)

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')

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
        """Remove water molecules."""
        tmp_files = []

        # Get local loggers from @launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        cmd = [self.check_structure_path,
               '-i', self.input_pdb_path,
               '-o', self.output_pdb_path,
               '--force_save',
               'water', '--remove', 'yes']

        returncode: int = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        if self.remove_tmp:
            fu.rm_file_list(tmp_files)

        return returncode


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Remove the water molecules from a PDB 3D structure.",
                                     formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_pdb_path', required=True, help="Input pdb file name")
    required_args.add_argument('-o', '--output_pdb_path', required=True, help="Output pdb file name")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    # Specific call of each building block
    RemovePdbWater(input_pdb_path=args.input_pdb_path, output_pdb_path=args.output_pdb_path,
                   properties=properties).launch()


if __name__ == '__main__':
    main()
