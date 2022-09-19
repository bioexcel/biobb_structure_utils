from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.renumber_structure import renumber_structure


class TestRenumberStructureGRO():
    def setup_class(self):
        fx.test_setup(self, 'renumber_structure_gro')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        renumber_structure(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['reference_output_stucture_path'])
        assert fx.not_empty(self.paths['output_mapping_json_path'])
        assert fx.equal(self.paths['output_mapping_json_path'], self.paths['reference_output_mapping_json_path'])
