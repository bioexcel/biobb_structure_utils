from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.remove_pdb_water import remove_pdb_water


class TestRemovePDBWater():
    def setUp(self):
        fx.test_setup(self, 'remove_pdb_water')

    def tearDown(self):
        #fx.test_teardown(self)
        pass

    def test_launch(self):
        remove_pdb_water(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pdb_path'])
        assert fx.equal(self.paths['output_pdb_path'], self.paths['reference_output_pdb_path'])
