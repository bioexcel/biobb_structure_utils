from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.structure_check import structure_check


class TestStructureCheck():
    def setup_class(self):
        fx.test_setup(self, 'structure_check')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_launch(self):
        structure_check(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_summary_path'])
