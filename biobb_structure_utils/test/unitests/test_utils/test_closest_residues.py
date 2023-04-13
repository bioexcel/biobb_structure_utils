from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.closest_residues import closest_residues


class TestClosestResidues():
    def setup_class(self):
        fx.test_setup(self, 'closest_residues')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        closest_residues(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_residues_path'])
        assert fx.equal(self.paths['output_residues_path'], self.paths['reference_output_residues_path'])
