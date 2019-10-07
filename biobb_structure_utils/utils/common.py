""" Common functions and constants for package biobb_structure_utils.utils """
from pathlib import Path, PurePath
import re, sys
from biobb_common.tools import file_utils as fu

PDB_COORD_RECORDS = ['MODEL', 'ANISOU', 'HETATM', 'ATOM', 'TER', 'ENDMDL']
PDB_SERIAL_RECORDS = ['ANISOU', 'HETATM', 'ATOM', 'TER']
PDB_WATERS = ['SOL', 'HOH', 'WAT', 'T3P']

def check_input_path(path, out_log, classname):
	""" Checks input file path """ 
	if not Path(path).exists():
		fu.log(classname + ': Unexisting input file, exiting', out_log)
		raise SystemExit(classname + ': Unexisting input file')
	file_extension = PurePath(path).suffix
	if not is_valid_pdb(file_extension[1:]):
		fu.log(classname + ': Format %s in input file is not compatible' % file_extension[1:], out_log)
		raise SystemExit(classname + ': Format %s in input file is not compatible' % file_extension[1:])
	# if file input has no path, add cwd because execution is launched on tmp folder
	if(PurePath(path).name == path or not PurePath(path).is_absolute()):
		path = str(PurePath(Path.cwd()).joinpath(path))
	return path

def check_output_path(path, out_log, classname):
	""" Checks output file path """ 
	if PurePath(path).parent and not Path(PurePath(path).parent).exists():
		fu.log(classname + ': Unexisting output folder, exiting', out_log)
		raise SystemExit(classname + ': Unexisting output folder')
	file_extension = PurePath(path).suffix
	if not is_valid_pdb(file_extension[1:]):
		fu.log(classname + ': Format %s in output file is not compatible' % file_extension[1:], out_log)
		raise SystemExit(classname + ': Format %s in output file is not compatible' % file_extension[1:])
	return path


def is_valid_pdb(ext):
	""" Checks if is a valid PDB file """
	formats = ['pdb']
	return ext in formats
