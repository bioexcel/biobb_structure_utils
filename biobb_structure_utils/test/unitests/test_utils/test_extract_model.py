from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_model import ExtractModel


class TestExtractModel():
    def setUp(self):
        fx.test_setup(self, 'extract_model')

    def tearDown(self):
        pass
        fx.test_teardown(self)

    def test_launch(self):
        ExtractModel(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_structure_path'])
