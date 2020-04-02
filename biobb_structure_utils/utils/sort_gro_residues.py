#!/usr/bin/env python3

"""Module containing the SortGroResidues class and the command line interface."""
import os
import json
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_structure_utils.gro_lib.gro import Gro
from biobb_structure_utils.utils.common import *


class SortGroResidues():
    """Class to sort the selected residues from a GRO 3D structure.

    Args:
        input_gro_path (str): Input GRO file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/WT_aq4_md_1.gro>`_. Accepted formats: gro.
        output_gro_path (str): Output sorted GRO file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/WT_aq4_md_sorted.gro>`_. Accepted formats: gro.
        properties (dic):
            | - **residue_name_list** (*list*) - (["NA", "CL", "SOL"]) Ordered residue name list.
            | - **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            | - **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_gro_path, 
                 output_gro_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_gro_path = str(input_gro_path)
        self.output_gro_path = str(output_gro_path)

        # Properties specific for BB
        self.residue_name_list = properties.get('residue_name_list', ["NA", "CL", "SOL"])

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
        """Sort residues in GRO structure."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        #Restart if needed
        if self.restart:
            output_file_list = [self.output_gro_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

        in_gro = Gro()
        in_gro.read_gro_file(self.input_gro_path)
        in_gro.sort_residues2(self.residue_name_list)
        in_gro.write_gro_file(self.output_gro_path)

        if self.remove_tmp:
            fu.rm_file_list(tmp_files)

        return 0

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Renumber atoms and residues from a 3D structure.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_gro_path', required=True, help="Input GRO file name")
    required_args.add_argument('-o', '--output_gro_path', required=True, help="Output sorted GRO file name")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    SortGroResidues(input_gro_path=args.input_gro_path, output_gro_path=args.output_gro_path, 
                    properties=properties).launch()

if __name__ == '__main__':
    main()
