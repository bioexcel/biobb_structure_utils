from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.structure_check import structure_check


class TestStructureCheck():
    def setUp(self):
        fx.test_setup(self, 'structure_check')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        structure_check(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_summary_path'])
        assert fx.equal(self.paths['output_summary_path'], self.paths['reference_output_summary_path'])
