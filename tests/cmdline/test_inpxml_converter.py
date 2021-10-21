# -*- coding: utf-8 -*-
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
    input_string = 'y\ndensityofstates\nbanddos\nN\ny\nkpointlistselection\ndefault\nn\ny\nl_relax\n' + \
                   'l_relaxSQA\nn\nmagmom\nmove\n0\n1\ncreate\n0\nremove\n0-2\ncreate\n0\nY\nNAME\ndefault\nN'

    result = runner.invoke(generate_inp_conversion, ['0.31', '0.34'], input=input_string)
    print(result.output)

    with open(file_path, 'r', encoding='utf-8') as f:
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

    with open(tmp_path / 'inp.xml', 'r', encoding='utf-8') as f:
        content = f.read()

    file_regression.check(content, extension='.xml')
