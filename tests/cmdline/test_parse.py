# -*- coding: utf-8 -*-
"""
Tests of the parse commands in the cli
"""
from pathlib import Path
import os
import pytest


def test_fleur_inp_file():
    """
    Test of the parse inp-file command
    """
    from masci_tools.cmdline.commands.parse import parse_inp_file
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_inp_file, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"comment": "Si bulk"' in result.output


def test_fleur_out_file():
    """
    Test of the parse out-file command
    """
    from masci_tools.cmdline.commands.parse import parse_out_file
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/out.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_out_file, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"sum_of_eigenvalues": -316.377' in result.output


def test_constants():
    """
    Test of the parse constants command
    """
    from masci_tools.cmdline.commands.parse import parse_constants
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_constants, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"Pi": 3.141592653' in result.output


def test_fleur_modes():
    """
    Test of the parse fleur-modes command
    """
    from masci_tools.cmdline.commands.parse import parse_fleur_modes
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_fleur_modes, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"bz_integration": "hist",' in result.output


def test_structure_data():
    """
    Test of the parse structure command
    """
    from masci_tools.cmdline.commands.parse import parse_structure_data
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_structure_data, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Info: Atoms found:' in result.output
    assert 'Si Si-1 [0.6787502783660522, 0.6787502783660522, 0.6787502783660522]' in result.output
    assert 'Info: Bravais matrix:' in result.output
    assert 'Info: Periodic boundary conditions [True, True, True]' in result.output


def test_cell():
    """
    Test of the parse cell command
    """
    from masci_tools.cmdline.commands.parse import parse_cell_data
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_cell_data, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '[[0.         2.71500111 2.71500111]' in result.output
    assert 'Info: Periodic boundary conditions [True, True, True]' in result.output


def test_parameter_data():
    """
    Test of the parse parameter command
    """
    from masci_tools.cmdline.commands.parse import parse_parameter_data
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_parameter_data, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"rmt": 2.17' in result.output
    assert '"xctyp": "pbe"' in result.output


def test_nkpts():
    """
    Test of the parse nkpts command
    """
    from masci_tools.cmdline.commands.parse import parse_nkpts
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_nkpts, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Info: Number of k-points: 2' in result.output


def test_kpoints():
    """
    Test of the parse kpoints command
    """
    from masci_tools.cmdline.commands.parse import parse_kpoints_data
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_kpoints_data, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Info: Bravais matrix:' in result.output
    assert 'Info: Periodic boundary conditions [True, True, True]' in result.output
    assert '[0.25, 0.25, 0.25]    w=2.0' in result.output


def test_symmetry():
    """
    Test of the parse symmetry command
    """
    from masci_tools.cmdline.commands.parse import parse_symmetry_information
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    result = runner.invoke(parse_symmetry_information, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Rotation:' in result.output
    assert 'Translation:' in result.output
    assert '[[ 0 -1  0]' in result.output


def test_relax_info():
    """
    Test of the parse relaxation command
    """
    from masci_tools.cmdline.commands.parse import parse_relaxation_data
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/GaAsMultiUForceXML/files/relax.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE)]
    with pytest.warns(UserWarning):
        result = runner.invoke(parse_relaxation_data, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"displacements": [' in result.output
    assert '0.0179807237' in result.output


def test_attrib():
    """
    Test of the parse attrib command
    """
    from masci_tools.cmdline.commands.parse import parse_attrib
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--name', 'kmax']
    result = runner.invoke(parse_attrib, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Value for attribute kmax: 3.5' in result.output

    args = [os.fspath(TEST_FILE), '--name', 'radius', '--contains', 'species', '-nc', 'Group']
    result = runner.invoke(parse_attrib, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Value for attribute radius: 2.17' in result.output


def test_text():
    """
    Test of the parse text command
    """
    from masci_tools.cmdline.commands.parse import parse_text
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--name', 'kpoint']
    result = runner.invoke(parse_text, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Text for tag kpoint: [[0.25, 0.25, 0.25], [0.25, 0.5, 0.5]]' in result.output

    args = [os.fspath(TEST_FILE), '--name', 'relPos', '--contains', 'Group', '--not-contains', 'species']
    result = runner.invoke(parse_text, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Text for tag relPos: [[0.125, 0.125, 0.125], [-0.125, -0.125, -0.125]]' in result.output


def test_all_attribs():
    """
    Test of the parse all-attribs command
    """
    from masci_tools.cmdline.commands.parse import parse_all_attribs
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--name', 'cutoffs']
    result = runner.invoke(parse_all_attribs, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"Gmax": 11.1,' in result.output

    args = [os.fspath(TEST_FILE), '--name', 'lo', '--contains', 'species', '-nc', 'Group', '--subtags']
    result = runner.invoke(parse_all_attribs, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"SCLO"' in result.output


def test_parent_attribs():
    """
    Test of the parse parent-attribs command
    """
    from masci_tools.cmdline.commands.parse import parse_parent_attribs
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--name', 'kpoint']
    result = runner.invoke(parse_parent_attribs, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"default"' in result.output

    args = [os.fspath(TEST_FILE), '--name', 'lo', '--contains', 'species', '-nc', 'Group']
    result = runner.invoke(parse_parent_attribs, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert '"Si-1",' in result.output


def test_tag_exists():
    """
    Test of the parse tag-exists command
    """
    from masci_tools.cmdline.commands.parse import parse_tag_exists
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--name', 'kpoint']
    result = runner.invoke(parse_tag_exists, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Tag kpoint: exists' in result.output

    args = [os.fspath(TEST_FILE), '--name', 'ldau', '--contains', 'species', '-nc', 'Group']
    result = runner.invoke(parse_tag_exists, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Tag ldau: does not exist' in result.output


def test_number_nodes():
    """
    Test of the parse number-nodes command
    """
    from masci_tools.cmdline.commands.parse import parse_number_nodes
    from click.testing import CliRunner

    TEST_FILE = Path('files/fleur/Max-R5/SiLOXML/files/inp.xml').resolve()
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--name', 'kpoint']
    result = runner.invoke(parse_number_nodes, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Tag kpoint: 2 times' in result.output

    args = [os.fspath(TEST_FILE), '--name', 'ldau', '--contains', 'species', '-nc', 'Group']
    result = runner.invoke(parse_number_nodes, args)

    print(result.output)
    assert result.exception is None, 'An unexpected exception occured: {result.exception}'
    assert 'Tag ldau: 0 times' in result.output
