from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.renumber_structure import RenumberStructure


class TestRenumberStructureGRO():
    def setUp(self):
        fx.test_setup(self, 'renumber_structure_gro')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_launch(self):
        RenumberStructure(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_stucture_path'])
        assert fx.not_empty(self.paths['output_mapping_json_path'])
        assert fx.equal(self.paths['output_mapping_json_path'], self.paths['reference_output_mapping_json_path'])
