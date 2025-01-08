# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.str_check_add_hydrogens import str_check_add_hydrogens


class TestStrCheckAddHydrogens():
    def setup_class(self):
        fx.test_setup(self, 'str_check_add_hydrogens')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_str_check_add_hydrogens(self):
        str_check_add_hydrogens(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        # assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_structure_path'], percent_tolerance=10)
