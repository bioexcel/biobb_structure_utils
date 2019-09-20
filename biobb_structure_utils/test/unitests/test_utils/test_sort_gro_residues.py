from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.sort_gro_residues import SortGroResidues


class TestSortGroResidues():
    def setUp(self):
        fx.test_setup(self, 'sort_gro_residues')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_launch(self):
        SortGroResidues(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_gro_path'])
        assert fx.equal(self.paths['output_gro_path'], self.paths['reference_output_gro_path'])
