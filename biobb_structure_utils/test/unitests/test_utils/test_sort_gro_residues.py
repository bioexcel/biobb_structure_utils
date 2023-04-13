from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.sort_gro_residues import sort_gro_residues


class TestSortGroResidues():
    def setup_class(self):
        fx.test_setup(self, 'sort_gro_residues')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        sort_gro_residues(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.equal(self.paths['output_gro_path'], self.paths['reference_output_gro_path'])
