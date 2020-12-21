#!/usr/bin/env python3

"""Module containing the ExtractChain class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_structure_utils.utils.common import *

class ExtractChain():
    """
    | biobb_structure_utils ExtractAtoms
    | This class is a wrapper of the Structure Checking tool to extract a chain from a 3D structure.
    | Wrapper for the `Structure Checking <https://github.com/bioexcel/biobb_structure_checking>`_ tool to extract a chain from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_chain.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_chain.pdb>`_. Accepted formats: pdb (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **chains** (*list*) - (None) List of chains to be extracted from the input_structure_path file. If empty, all the chains of the structure will be returned.
            * **check_structure_path** (*string*) - ("check_structure") path to the check_structure application
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.extract_chain import extract_chain
            prop = { 
                'chains': [ 'A', 'B' ] 
            }
            extract_chain(input_structure_path='/path/to/myStructure.pdb, 
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

    def __init__(self, input_structure_path, output_structure_path, 
                properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = str(input_structure_path)
        self.output_structure_path = str(output_structure_path)

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')
        self.chains = properties.get('chains', [])
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
        self.input_structure_path = check_input_path(self.input_structure_path, out_log, self.__class__.__name__)
        self.output_structure_path = check_output_path(self.output_structure_path, out_log, self.__class__.__name__)

    def check_format_chains(self, chains, out_log):
        """ Check format of chains list """
        if not chains:
            fu.log('Empty chains parameter, all chains will be returned.',  out_log, self.global_log)
            return 'All'
        
        if not isinstance(chains, list):
            fu.log('Incorrect format of chains parameter, all chains will be returned.',  out_log, self.global_log)
            return 'All'

        return ','.join(chains)


    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`ExtractChain <utils.extract_chain.ExtractChain>` utils.extract_chain.ExtractChain object."""
    
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

        # check if user has passed chains properly
        chains = self.check_format_chains(self.chains, out_log)

        # run command line
        cmd = [self.check_structure_path,
               '-i', self.input_structure_path,
               '-o', self.output_structure_path,
               '--force_save',
               'chains', '--select', chains]

        returncode: int = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        return returncode

def extract_chain(input_structure_path: str, output_structure_path: str, properties: dict = None, **kwargs) -> None:
    """Execute the :class:`ExtractChain <utils.extract_chain.ExtractChain>` class and
    execute the :meth:`launch() <utils.extract_chain.ExtractChain.launch>` method."""

    return ExtractChain(input_structure_path=input_structure_path, 
                    output_structure_path=output_structure_path,
                    properties=properties).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Extract a chain from a 3D structure.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_structure_path', required=True, help="Input structure file path. Accepted formats: pdb.")
    required_args.add_argument('-o', '--output_structure_path', required=True, help="Output structure file path. Accepted formats: pdb.")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    ExtractChain(input_structure_path=args.input_structure_path, 
                output_structure_path=args.output_structure_path, 
                properties=properties).launch()

if __name__ == '__main__':
    main()