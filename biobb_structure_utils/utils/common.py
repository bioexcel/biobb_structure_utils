"""Common functions and constants for package biobb_structure_utils.utils"""

from collections.abc import Mapping
from pathlib import Path, PurePath
from typing import Optional, Union

from biobb_common.tools import file_utils as fu

PDB_COORD_RECORDS = ["MODEL", "ANISOU", "HETATM", "ATOM", "TER", "ENDMDL"]
PDB_SERIAL_RECORDS = ["ANISOU", "HETATM", "ATOM", "TER"]
PDB_WATERS = ["SOL", "HOH", "WAT", "T3P"]


def check_input_path(path, out_log, classname):
    """Checks input file path"""
    if not Path(path).exists():
        fu.log(classname + ": Unexisting input file, exiting", out_log)
        raise SystemExit(classname + ": Unexisting input file")
    file_extension = PurePath(path).suffix
    if not is_valid_pdb(file_extension[1:]) and not is_valid_pdbqt(file_extension[1:]):
        fu.log(
            classname
            + ": Format %s in input file is not compatible" % file_extension[1:],
            out_log,
        )
        raise SystemExit(
            classname
            + ": Format %s in input file is not compatible" % file_extension[1:]
        )
    # if file input has no path, add cwd because execution is launched on tmp folder
    if PurePath(path).name == path or not PurePath(path).is_absolute():
        path = str(PurePath(Path.cwd()).joinpath(path))
    return path


def check_output_path(path, out_log, classname):
    """Checks output file path"""
    if PurePath(path).parent and not Path(PurePath(path).parent).exists():
        fu.log(classname + ": Unexisting output folder, exiting", out_log)
        raise SystemExit(classname + ": Unexisting output folder")
    file_extension = PurePath(path).suffix
    if not is_valid_pdb(file_extension[1:]) and not is_valid_pdbqt(file_extension[1:]):
        fu.log(
            classname
            + ": Format %s in output file is not compatible" % file_extension[1:],
            out_log,
        )
        raise SystemExit(
            classname
            + ": Format %s in output file is not compatible" % file_extension[1:]
        )
    return path


def check_output_path_pdbqt(path, out_log, classname):
    """Checks output file path"""
    if PurePath(path).parent and not Path(PurePath(path).parent).exists():
        fu.log(classname + ": Unexisting output folder, exiting", out_log)
        raise SystemExit(classname + ": Unexisting output folder")
    file_extension = PurePath(path).suffix
    if not is_valid_pdbqt(file_extension[1:]):
        fu.log(
            classname
            + ": Format %s in output file is not compatible" % file_extension[1:],
            out_log,
        )
        raise SystemExit(
            classname
            + ": Format %s in output file is not compatible" % file_extension[1:]
        )
    return path


def check_output_path_json(path, out_log, classname):
    """Checks output file path"""
    if PurePath(path).parent and not Path(PurePath(path).parent).exists():
        fu.log(classname + ": Unexisting output folder, exiting", out_log)
        raise SystemExit(classname + ": Unexisting output folder")
    file_extension = PurePath(path).suffix
    if not is_valid_json(file_extension[1:]):
        fu.log(
            classname
            + ": Format %s in output file is not compatible" % file_extension[1:],
            out_log,
        )
        raise SystemExit(
            classname
            + ": Format %s in output file is not compatible" % file_extension[1:]
        )
    return path


def is_valid_pdb(ext):
    """Checks if is a valid PDB file"""
    formats = ["pdb"]
    return ext in formats


def is_valid_pdbqt(ext):
    """Checks if is a valid PDB/PDBQT file"""
    formats = ["pdb", "pdbqt"]
    return ext in formats


def is_valid_json(ext):
    """Checks if is a valid JSON file"""
    formats = ["json"]
    return ext in formats


def check_output_end(structure, out_log):
    """if structure ends with END, remove last line"""
    lines_new = []
    with open(structure, "r") as f:
        lines = f.read().splitlines()
        for item in lines:
            # if not item.startswith('END'):
            if not item.strip() == "END":
                lines_new.append(item)
            else:
                fu.log("%s file ends with END, cleaning" % structure, out_log)

    with open(structure, "w") as f:
        for item in lines_new:
            f.write("%s\n" % item)


def create_output_file(type, input, residues, output, out_log):
    # parse PDB file and get residues line by line
    new_file_lines = []
    curr_model = 0
    with open(input) as infile:
        for line in infile:
            if line.startswith("MODEL   "):
                curr_model = line.rstrip()[-1]
                if int(curr_model) > 1:
                    new_file_lines.append("ENDMDL\n")
                new_file_lines.append("MODEL     " + "{:>4}".format(curr_model) + "\n")

            conditional_atoms = [
                (line.startswith("ATOM") or line.startswith("HETATM")),
                line.startswith("HETATM"),
                line.startswith("ATOM"),
            ]

            if conditional_atoms[type]:
                name = line[17:20].strip()
                chain = line[21:22].strip()
                res_id = line[22:27].strip()
                if curr_model != 0:
                    model = curr_model.strip()
                else:
                    model = "1"
                if chain == "":
                    chain = " "

                for nstr in residues:
                    if (
                        nstr["res_id"] == res_id
                        and nstr["name"] == name
                        and nstr["chain"] == chain
                        and nstr["model"] == model
                    ):
                        new_file_lines.append(line)

    if int(curr_model) > 0:
        new_file_lines.append("ENDMDL\n")

    fu.log("Writting pdb to: %s" % (output), out_log)

    # save new file with heteroatoms
    with open(output, "w") as outfile:
        for line in new_file_lines:
            outfile.write(line)


def create_biopython_residue(residue):
    return {
        "model": str(residue.get_parent().get_parent().get_id() + 1),
        "chain": residue.get_parent().get_id(),
        "name": residue.get_resname(),
        "res_id": str(residue.get_id()[1]),
    }


def create_residues_list(residues, out_log):
    """Check format of residues list"""
    if not residues:
        return None

    list_residues = []

    for residue in residues:
        d = residue
        code = []
        if isinstance(residue, Mapping):
            if "name" in residue:
                code.append("name")
            if "res_id" in residue:
                code.append("res_id")
            if "chain" in residue:
                code.append("chain")
            if "model" in residue:
                code.append("model")
        else:
            d = {"res_id": str(residue)}
            code.append("res_id")

        d["code"] = code
        list_residues.append(d)

    return list_residues


def check_format_heteroatoms(hets, out_log):
    """Check format of heteroatoms list"""
    if not hets:
        return 0

    listh = []

    for het in hets:
        d = het
        code = []
        if "name" in het:
            code.append("name")
        if "res_id" in het:
            code.append("res_id")
        if "chain" in het:
            code.append("chain")
        if "model" in het:
            code.append("model")

        d["code"] = code
        listh.append(d)

    return listh


# TODO: Move this function to biobb_common.tools.file_utils
def _from_string_to_list(input_data: Optional[Union[str, list[str]]]) -> list[str]:
    """
    Converts a string to a list, splitting by commas or spaces. If the input is already a list, returns it as is.
    Returns an empty list if input_data is None.

    Parameters:
        input_data (str, list, or None): The string, list, or None value to convert.

    Returns:
        list: A list of string elements or an empty list if input_data is None.
    """
    if input_data is None:
        return []

    if isinstance(input_data, list):
        # If input is already a list, return it
        return input_data

    # If input is a string, determine the delimiter based on presence of commas
    delimiter = "," if "," in input_data else " "
    items = input_data.split(delimiter)

    # Remove whitespace from each item and ignore empty strings
    processed_items = [item.strip() for item in items if item.strip()]

    return processed_items
