#!/usr/bin/env python3

"""Module containing the StrCheckAddHydrogens class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_structure_utils.utils.common import *

class StrCheckAddHydrogens():
    """
    | biobb_structure_utils StrCheckAddHydrogens
    | This class is a wrapper of the Structure Checking tool to add hydrogens to a 3D structure.
    | Wrapper for the `Structure Checking <https://github.com/bioexcel/biobb_structure_checking>`_ tool to add hydrogens to a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/str_no_H.pdb>`_. Accepted formats: pdb (edam:format_1476).
        output_structure_path (str): Output structure file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_str_H.pdbqt>`_. Accepted formats: pdb (edam:format_1476), pdbqt (edam:format_1476).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **charges** (*bool*) - (False) Wether or not to add charges to the output file. If True the output is in PDBQT format.
            * **mode** (*string*) - (None) Selection mode. Values: auto, list, ph, int, int_his
            * **check_structure_path** (*string*) - ("check_structure") path to the check_structure application
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_structure_utils.utils.str_check_add_hydrogens import str_check_add_hydrogens
            prop = { 
                'charges': False, 
                'mode': 'auto'
            }
            str_check_add_hydrogens(input_structure_path='/path/to/myInputStr.pdb, 
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

    def __init__(self, input_structure_path, 
                 output_structure_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = str(input_structure_path)
        self.output_structure_path = str(output_structure_path)

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')
        self.charges = properties.get('charges', False)
        self.mode = properties.get('mode', None)
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
        self.output_structure_path = check_output_path_pdbqt(self.output_structure_path, out_log, self.__class__.__name__)

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`StrCheckAddHydrogens <utils.str_check_add_hydrogens.StrCheckAddHydrogens>` utils.str_check_add_hydrogens.StrCheckAddHydrogens object."""
        
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

        # check_structure -i receptor_no_wat.pdb -o prep_receptor.pdbqt add_hydrogen --add_charges --add_mode auto 

        # run command line
        cmd = [self.check_structure_path,
               '-i', self.input_structure_path,
               '-o', self.output_structure_path,
               '--force_save',
               'add_hydrogen']

        if self.charges:
            cmd.append('--add_charges')

        if self.mode:
            cmd.extend(['--add_mode', self.mode])
        else:
            cmd.extend(['--add_mode', 'None'])

        returncode: int = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()

        return returncode

def str_check_add_hydrogens(input_structure_path: str, output_structure_path: str, properties: dict = None, **kwargs) -> None:
    """Execute the :class:`StrCheckAddHydrogens <utils.str_check_add_hydrogens.StrCheckAddHydrogens>` class and
    execute the :meth:`launch() <utils.str_check_add_hydrogens.StrCheckAddHydrogens.launch>` method."""

    return StrCheckAddHydrogens(input_structure_path=input_structure_path, 
                                output_structure_path=output_structure_path,
                                properties=properties).launch()

def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Class to add hydrogens to a 3D structure.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_structure_path', required=True, help="Input structure file path. Accepted formats: pdb.")
    required_args.add_argument('-o', '--output_structure_path', required=True, help="Output structure file path. Accepted formats: pdb, pdbqt.")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    StrCheckAddHydrogens(input_structure_path=args.input_structure_path, 
                        output_structure_path=args.output_structure_path, 
                        properties=properties).launch()

if __name__ == '__main__':
    main()
