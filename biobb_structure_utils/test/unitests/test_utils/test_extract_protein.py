from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_protein import extract_protein


class TestExtractProtein():
    def setUp(self):
        fx.test_setup(self, 'extract_protein')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        extract_protein(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_protein_path'])
        assert fx.equal(self.paths['output_protein_path'], self.paths['reference_output_protein_path'])
