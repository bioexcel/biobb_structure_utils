import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_structure_utils",
    version="3.7.6",
    author="Biobb developers",
    author_email="pau.andrio@bsc.es",
    description="biobb_structure_utils is the Biobb module collection to perform basic manipulations on 3d structures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_structure_utils",
    project_urls={
        "Documentation": "http://biobb_structure_utils.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test',]),
    install_requires=['biobb_common==3.7.0', 'biobb_structure_checking==3.9.11'],
    python_requires='==3.7.*',
    entry_points={
        "console_scripts": [
            "cat_pdb = biobb_structure_utils.utils.cat_pdb:main",
            "extract_atoms = biobb_structure_utils.utils.extract_atoms:main",
            "extract_chain = biobb_structure_utils.utils.extract_chain:main",
            "extract_heteroatoms = biobb_structure_utils.utils.extract_heteroatoms:main",
            "extract_model = biobb_structure_utils.utils.extract_model:main",
            "extract_molecule = biobb_structure_utils.utils.extract_molecule:main",
            "remove_ligand = biobb_structure_utils.utils.remove_ligand:main",
            "remove_pdb_water = biobb_structure_utils.utils.remove_pdb_water:main",
            "renumber_structure = biobb_structure_utils.utils.renumber_structure:main",
            "sort_gro_residues = biobb_structure_utils.utils.sort_gro_residues:main",
            "str_check_add_hydrogens = biobb_structure_utils.utils.str_check_add_hydrogens:main",
            "structure_check = biobb_structure_utils.utils.structure_check:main"
        ]
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
