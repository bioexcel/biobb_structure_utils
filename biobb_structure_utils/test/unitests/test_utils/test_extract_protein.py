from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_protein import ExtractProtein


class TestExtractProtein():
    def setUp(self):
        fx.test_setup(self, 'extract_protein')

    def tearDown(self):
        pass
        fx.test_teardown(self)

    def test_launch(self):
        ExtractProtein(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_protein_path'])
        assert fx.equal(self.paths['output_protein_path'], self.paths['reference_output_protein_path'])
