# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.remove_molecules import remove_molecules


class TestRemoveMolecules:
    def setup_class(self):
        fx.test_setup(self, 'remove_molecules')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        remove_molecules(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_molecules_path'])
        assert fx.equal_txt(self.paths['output_molecules_path'], self.paths['reference_output_molecules_path'])
