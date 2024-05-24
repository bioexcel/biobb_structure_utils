from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_model import extract_model


class TestExtractModel():
    def setup_class(self):
        fx.test_setup(self, 'extract_model')

    def teardown_class(self):
        # fx.test_teardown(self)
        pass

    def test_launch(self):
        extract_model(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_structure_path'])
