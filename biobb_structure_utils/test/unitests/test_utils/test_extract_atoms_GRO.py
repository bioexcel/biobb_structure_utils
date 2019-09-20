from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_atoms import ExtractAtoms


class TestExtractAtomsGRO():
    def setUp(self):
        fx.test_setup(self, 'extract_atoms_gro')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_launch(self):
        ExtractAtoms(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_stucture_path'])
