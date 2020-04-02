#!/usr/bin/env python3

"""Module containing the CatPDB class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_structure_utils.utils.common import *

class CatPDB():
    """Class to concat two PDB structures in a single PDB file.

    Args:
        input_structure1 (str): Input structure 1 file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cat_protein.pdb>`_. Accepted formats: pdb.
        input_structure2 (str): Input structure 2 file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/cat_ligand.pdb>`_. Accepted formats: pdb.
        output_structure_path (str): Output protein file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_cat_pdb.pdb>`_. Accepted formats: pdb.
        properties (dic):
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_structure1, input_structure2, 
                 output_structure_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_structure1 = str(input_structure1)
        self.input_structure2 = str(input_structure2)
        self.output_structure_path = str(output_structure_path)

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')
        self.properties = properties

        # Common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

    def check_data_params(self, out_log, err_log):
        """ Checks all the input/output paths and parameters """
        self.input_structure1 = check_input_path(self.input_structure1, out_log, self.__class__.__name__)
        self.input_structure2 = check_input_path(self.input_structure2, out_log, self.__class__.__name__)
        self.output_structure_path = check_output_path(self.output_structure_path, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self) -> int:
        """Remove ligand atoms from the structure."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        # check input/output paths and parameters
        self.check_data_params(out_log, err_log)

        # Check the properties
        fu.check_properties(self, self.properties)

        #Restart if needed
        if self.restart:
            output_file_list = [self.output_structure_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step,  out_log, self.global_log)
                return 0

        # concat both input files and save them into output file
        filenames = [self.input_structure1, self.input_structure2]
        with open(self.output_structure_path, 'w') as outfile:
            for fname in filenames:
                with open(fname) as infile:
                    for line in infile:
                        if not line.startswith("END"): outfile.write(line)

        fu.log('File %s created' % self.output_structure_path,  out_log, self.global_log)

        return 1

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Concat two PDB structures in a single PDB file.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i1', '--input_structure1', required=True, help="Input structure 1 file path. Accepted formats: pdb.")
    required_args.add_argument('-i2', '--input_structure2', required=True, help="Input structure 2 file path. Accepted formats: pdb.")
    required_args.add_argument('-o', '--output_structure_path', required=True, help="Output structure file path. Accepted formats: pdb.")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    CatPDB(input_structure1=args.input_structure1, input_structure2=args.input_structure2, 
           output_structure_path=args.output_structure_path, 
           properties=properties).launch()

if __name__ == '__main__':
    main()
