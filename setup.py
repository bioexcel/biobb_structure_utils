import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_structure_utils",
    version="2.0.0",
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
    install_requires=['biobb_common==2.0.1', 'biobb_structure_checking==1.0.6'],
    python_requires='==3.6.*',
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
