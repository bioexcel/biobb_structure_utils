from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.str_check_add_hydrogens import StrCheckAddHydrogens


class TestStrCheckAddHydrogens():
    def setUp(self):
        fx.test_setup(self, 'str_check_add_hydrogens')

    def tearDown(self):
        pass
        fx.test_teardown(self)

    def test_str_check_add_hydrogens(self):
        StrCheckAddHydrogens(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_structure_path'])
