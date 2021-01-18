from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.structure_check import StructureCheck


class TestStructureCheck():
    def setUp(self):
        fx.test_setup(self, 'structure_check')

    def tearDown(self):
        pass
        fx.test_teardown(self)

    def test_launch(self):
        StructureCheck(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_summary_path'])
        assert fx.equal(self.paths['output_summary_path'], self.paths['reference_output_summary_path'])
