# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_structure_utils.utils.extract_residues import extract_residues


class TestExtractResidues:
    def setup_class(self):
        fx.test_setup(self, 'extract_residues')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_launch(self):
        extract_residues(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_residues_path'])
        assert fx.equal_txt(self.paths['output_residues_path'], self.paths['reference_output_residues_path'])
