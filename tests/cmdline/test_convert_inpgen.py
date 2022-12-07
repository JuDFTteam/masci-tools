"""
Tests of the commands in the convert-inpgen command of the masci-tools cli
"""
import os
import pytest

try:
    import pymatgen
    from pymatgen.io.fleur import FleurInput
except ImportError:
    pymatgen = None

try:
    import ase_fleur
except ImportError:
    ase_fleur = None


@pytest.mark.skipif(not pymatgen, reason='pymatgen or pymatgen-io-fleur are not installed')
def test_pymatgen_converter(file_regression, test_file):
    """
    Test of the convert-inpgen command using the pymatgen converter
    """
    from masci_tools.cmdline.commands.convert_inpgen import convert_inpgen
    from click.testing import CliRunner

    TEST_FILE = test_file('fleur/Max-R5/SiLOXML/files/inp.xml')
    runner = CliRunner()
    args = [TEST_FILE, 'inpgen.in', '--converter', 'pymatgen']
    with runner.isolated_filesystem():
        result = runner.invoke(convert_inpgen, args)

        print(result.output)
        assert result.exception is None, f'An unexpected exception occurred: {result.exception}'

        assert os.path.isfile('inpgen.in')

        with open('inpgen.in', encoding='utf-8') as file:
            content = file.read()

    file_regression.check(content, basename='test_convert_inpgen')


@pytest.mark.skipif(not pymatgen, reason='pymatgen or pymatgen-io-fleur are not installed')
def test_pymatgen_converter_cif(file_regression, test_file):
    """
    Test of the convert-inpgen command using the pymatgen converter
    """
    from masci_tools.cmdline.commands.convert_inpgen import convert_inpgen
    from click.testing import CliRunner

    TEST_FILE = test_file('cif_files/Si.cif')
    runner = CliRunner()
    args = [TEST_FILE, 'inpgen.in', '--converter', 'pymatgen']
    with runner.isolated_filesystem():
        result = runner.invoke(convert_inpgen, args)

        print(result.output)
        assert result.exception is None, f'An unexpected exception occurred: {result.exception}'

        assert os.path.isfile('inpgen.in')

        with open('inpgen.in', encoding='utf-8') as file:
            content = file.read()

    file_regression.check(content, basename='test_convert_inpgen_cif')


@pytest.mark.skipif(not ase_fleur, reason='ase-fleur is not installed')
def test_ase_converter(file_regression, test_file):
    """
    Test of the convert-inpgen command using the ase converter
    """
    from masci_tools.cmdline.commands.convert_inpgen import convert_inpgen
    from click.testing import CliRunner

    TEST_FILE = test_file('fleur/Max-R5/SiLOXML/files/inp.xml')
    runner = CliRunner()
    args = [TEST_FILE, 'inpgen.in', '--converter', 'ase']
    with runner.isolated_filesystem():
        result = runner.invoke(convert_inpgen, args)

        print(result.output)
        assert result.exception is None, f'An unexpected exception occurred: {result.exception}'

        assert os.path.isfile('inpgen.in')

        with open('inpgen.in', encoding='utf-8') as file:
            content = file.read()

    file_regression.check(content, basename='test_convert_inpgen_ase')
