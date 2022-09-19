from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_molecule import extract_molecule


class TestExtractMolecule():
    def setup_class(self):
        fx.test_setup(self, 'extract_molecule')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        extract_molecule(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_molecule_path'])
        assert fx.equal(self.paths['output_molecule_path'], self.paths['reference_output_molecule_path'])
