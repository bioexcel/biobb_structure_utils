#!/usr/bin/env python3

"""Module containing the ExtractHeteroAtoms class and the command line interface."""
import argparse
from biobb_common.configuration import settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from Bio import BiopythonWarning
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.PDBIO import PDBIO
from biobb_structure_utils.utils.common import *

class ExtractHeteroAtoms():
    """Class to extract hetero-atoms from a 3D structure.

    Args:
        input_structure_path (str): Input structure file path. File type: input. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/data/utils/extract_heteroatom.pdb>`_. Accepted formats: pdb.
        output_heteroatom_path (str): Output heteroatom file path. File type: output. `Sample file <https://github.com/bioexcel/biobb_structure_utils/raw/master/biobb_structure_utils/test/reference/utils/ref_extract_heteroatom.pdb>`_. Accepted formats: pdb.
        properties (dic):
            * **heteroatoms** (*list*) - (None) List of dictionaries with the name | res_id | chain | model of the heteroatoms to be extracted. Format: [{"name": "ZZ7", "res_id": "302", "chain": "B", "model": "1"}]. If empty, all the heteroatoms of the structure will be returned.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
    """

    def __init__(self, input_structure_path, 
                 output_heteroatom_path, properties=None, **kwargs) -> None:
        properties = properties or {}

        # Input/Output files
        self.input_structure_path = str(input_structure_path)
        self.output_heteroatom_path = str(output_heteroatom_path)

        # Properties specific for BB
        self.check_structure_path = properties.get('check_structure_path', 'check_structure')
        self.heteroatoms = properties.get('heteroatoms', [])
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
        self.output_heteroatom_path = check_output_path(self.output_heteroatom_path, out_log, self.__class__.__name__)

    def check_format_heteroatoms(self, hets, out_log):
        """ Check format of heteroatoms list """
        if not hets:
            return 0
        
        listh = []

        for het in hets:
            d = het
            code = []
            if 'name' in het: code.append('name')
            if 'res_id' in het: code.append('res_id')
            if 'chain' in het: code.append('chain')
            if 'model' in het: code.append('model')

            d['code'] = code
            listh.append(d)

        return listh


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

        # get list of heteroatoms from porperties
        list_heteroatoms = self.check_format_heteroatoms(self.heteroatoms, out_log)

        # load input into BioPython structure
        structure = PDBParser(QUIET = True).get_structure('structure', self.input_structure_path)

        # if empty list of heteroatoms, raise exit
        if not list_heteroatoms:
            fu.log('Empty list of heteroatoms or incorrect format', out_log)
            raise SystemExit('Empty list of heteroatoms or incorrect format')

        new_structure = []

        # get desired heteroatoms
        for residue in structure.get_residues():

            r = {
                'model': str(residue.get_parent().get_parent().get_id() + 1),
                'chain': residue.get_parent().get_id(),
                'name': residue.get_resname(),
                'res_id': str(residue.get_id()[1])
            }

            
            for het in list_heteroatoms:
                match = True
                for code in het['code']:
                    if het[code].strip() != r[code].strip():
                        match = False
                        break

                if(match): 
                    new_structure.append(r)

        # if not heteroatoms found in structure, raise exit
        if not new_structure:
            fu.log('The heteroatoms given by user were not found in input structure', out_log)
            raise SystemExit('The heteroatoms given by user were not found in input structure')

        # parse PDB file and get heteroatoms line by line
        new_file_lines = []
        curr_model = 0
        with open(self.input_structure_path) as infile:
            for line in infile:
                if line.startswith("MODEL   "): 
                    curr_model = line.rstrip()[-1]
                    if(int(curr_model) > 1): new_file_lines.append('ENDMDL\n')
                    new_file_lines.append('MODEL     ' +  "{:>4}".format(curr_model) + '\n')
                if line.startswith("HETATM"): 
                    name = line[17:20].strip()
                    chain = line[21:22].strip()
                    res_id = line[23:27].strip()
                    if curr_model != 0: model = curr_model.strip()
                    else: model = "1"

                    for nstr in new_structure:
                        if nstr['res_id'] == res_id and nstr['name'] == name and  nstr['chain'] == chain and nstr['model'] == model:
                            new_file_lines.append(line)

        if(int(curr_model) > 0): new_file_lines.append('ENDMDL\n')

        # save new file with heteroatoms
        with open(self.output_heteroatom_path, 'w') as outfile:
            for line in new_file_lines:
                outfile.write(line)

        fu.log('File %s created' % self.output_heteroatom_path,  out_log, self.global_log)

        return 0

def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Extract a list of heteroatoms from a 3D structure.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('-c', '--config', required=False, help="This file can be a YAML file, JSON file or JSON string")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--input_structure_path', required=True, help="Input structure file path. Accepted formats: pdb.")
    required_args.add_argument('-o', '--output_heteroatom_path', required=True, help="Output heteroatom file path. Accepted formats: pdb.")

    args = parser.parse_args()
    config = args.config if args.config else None
    properties = settings.ConfReader(config=config).get_prop_dic()

    #Specific call of each building block
    ExtractHeteroAtoms(input_structure_path=args.input_structure_path, output_heteroatom_path=args.output_heteroatom_path, properties=properties).launch()

if __name__ == '__main__':
    main()
