from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_heteroatoms import extract_heteroatoms


class TestExtractHeteroAtoms():
    def setUp(self):
        fx.test_setup(self, 'extract_heteroatoms')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        extract_heteroatoms(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_heteroatom_path'])
        assert fx.equal_txt(self.paths['output_heteroatom_path'], self.paths['reference_output_heteroatom_path'])
