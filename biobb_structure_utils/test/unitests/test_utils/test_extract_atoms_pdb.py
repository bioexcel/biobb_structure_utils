from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_atoms import extract_atoms


class TestExtractAtomsPDB():
    def setUp(self):
        fx.test_setup(self, 'extract_atoms')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        extract_atoms(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_stucture_path'])
