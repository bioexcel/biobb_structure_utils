from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.remove_ligand import remove_ligand


class TestRemoveLigandGro():
    def setup_class(self):
        fx.test_setup(self, 'remove_ligand_gro')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        remove_ligand(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_stucture_path'])
