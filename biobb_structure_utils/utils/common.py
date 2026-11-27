"""Common functions and constants for package biobb_structure_utils.utils"""

from collections.abc import Mapping

from biobb_common.tools import file_utils as fu

PDB_SERIAL_RECORDS = ["ANISOU", "HETATM", "ATOM", "TER"]


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
                curr_model = line.split()[1]
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
                res_id = line[22:26].strip()
                icode = line[26:27] or " "
                if curr_model != 0:
                    model = curr_model.strip()
                else:
                    model = "1"
                if chain == "":
                    chain = " "

                for nstr in residues:
                    if (
                        nstr["res_id"] == res_id and nstr["icode"] == icode and nstr["name"] == name and nstr["chain"] == chain and nstr["model"] == model
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
        # insertion code, " " if none
        "icode": residue.get_id()[2],
    }


def residue_value(residue, code):
    """Value of a create_biopython_residue() residue to compare with a selection of
    create_residues_list(): the res_id with its insertion code, if any ("62A")."""
    if code == "res_id":
        return residue["res_id"] + residue["icode"].strip()
    return residue[code]


def create_residues_list(residues):
    """Goes from a residues property (res_ids or dictionaries with name | res_id | chain | model)
    to the selections of select_residues(): dictionaries of strings."""
    if not residues:
        return None

    selections = []
    for residue in residues:
        if not isinstance(residue, Mapping):
            residue = {"res_id": residue}
        selection = {key: str(residue[key]).strip() for key in ("name", "res_id", "chain", "model") if key in residue}
        if not selection:
            raise ValueError(f"The residue selection {residue} has no name, res_id, chain or model")
        selections.append(selection)

    return selections


def select_residues(structure, selections):
    """Goes from a Biopython structure and the selections of create_residues_list() to the
    Biopython residues that match any of them (all the residues if there are no selections)."""
    selected = []
    for residue in structure.get_residues():
        values = create_biopython_residue(residue)
        if not selections or any(
            all(residue_value(values, key).strip() == value for key, value in selection.items())
            for selection in selections
        ):
            selected.append(residue)
    return selected
