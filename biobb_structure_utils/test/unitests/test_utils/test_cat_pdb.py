# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.cat_pdb import cat_pdb


class TestCatPDB():
    def setup_class(self):
        fx.test_setup(self, 'cat_pdb')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        cat_pdb(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_structure_path'])
