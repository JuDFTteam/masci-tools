"""
Tests of the inpxml converter
"""
import os
from pathlib import Path


def test_generate_conversion(file_regression, remove_conversion):
    """
    Test of the generate-conversion command
    """
    from masci_tools.tools.fleur_inpxml_converter import generate_inp_conversion
    from click.testing import CliRunner

    file_path = remove_conversion

    runner = CliRunner()
    input_string = 'y\ndensityofstates\nbanddos\nN\ny\nkpointlistselection\ndefault\nn\ny\nkpointcount\ny\nkpointmesh\nn\nTest Warning\nn\ny\nl_relax\n' + \
                   'l_relaxSQA\nn\nmagmom\nmove\n0\n1\ncreate\n0\nremove\n0-2\ncreate\n0\nY\nNAME\ndefault\nN\ny\nlatnam\nn\nTest Warning 2\nn'

    result = runner.invoke(generate_inp_conversion, ['0.31', '0.34'], input=input_string)
    print(result.output)

    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    with open(file_path, encoding='utf-8') as f:
        content = f.read()

    file_regression.check(content, extension='.json')


def test_convert_inpxml(tmp_path, test_file, file_regression):
    """
    Test of the generate-conversion command
    """
    from masci_tools.tools.fleur_inpxml_converter import convert_inpxml
    from click.testing import CliRunner

    runner = CliRunner()
    result = runner.invoke(
        convert_inpxml,
        [test_file('fleur/aiida_fleur/inpxml/FePt/inp.xml'), '0.34', '--output-file',
         os.fspath(tmp_path / 'inp.xml')])
    print(result.output)

    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    with open(tmp_path / 'inp.xml', encoding='utf-8') as f:
        content = f.read()

    file_regression.check(content, extension='.xml')
