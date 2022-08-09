"""
Test of the plot commands in the cli

Here we do not test the actual content of the plot but only that the
commands work without error
"""
from pathlib import Path
import os
import pytest


def test_fleur_dos():
    """
    Test of the fleur-dos routine without options
    """
    from masci_tools.cmdline.commands.plot import plot_fleur_banddos_dos
    from click.testing import CliRunner

    TEST_FILE = Path(__file__).parent.resolve() / Path('../files/hdf5_reader/banddos_dos.hdf')
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--save']
    with runner.isolated_filesystem():
        result = runner.invoke(plot_fleur_banddos_dos, args)

        print(result.output)
        assert result.exception is None, f'An unexpected exception occurred: {result.exception}'
        assert os.path.isfile('dos_plot.png')


def test_fleur_dos_recipe():
    """
    Test of the fleur-dos routine with options
    """
    from masci_tools.cmdline.commands.plot import plot_fleur_banddos_dos
    from click.testing import CliRunner

    TEST_FILE = Path(__file__).parent.resolve() / Path('../files/hdf5_reader/banddos_spinpol_dos.hdf')
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--save', '--recipe', 'FleurJDOS', '--l_resolved', 'all', '--interstitial', 'False']
    with runner.isolated_filesystem():
        with pytest.warns(UserWarning):
            result = runner.invoke(plot_fleur_banddos_dos, args)

        print(result.output)
        assert result.exception is None, f'An unexpected exception occurred: {result.exception}'
        assert os.path.isfile('dos_plot.png')


def test_fleur_bands():
    """
    Test of the fleur-bands routine without options
    """
    from masci_tools.cmdline.commands.plot import plot_fleur_banddos_bands
    from click.testing import CliRunner

    TEST_FILE = Path(__file__).parent.resolve() / Path('../files/hdf5_reader/banddos_bands.hdf')
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--save']
    with runner.isolated_filesystem():
        result = runner.invoke(plot_fleur_banddos_bands, args)

        print(result.output)
        assert result.exception is None, f'An unexpected exception occurred: {result.exception}'
        assert os.path.isfile('bandstructure.png')


def test_fleur_bands_recipe():
    """
    Test of the fleur-bands routine with options
    """
    from masci_tools.cmdline.commands.plot import plot_fleur_banddos_bands
    from click.testing import CliRunner

    TEST_FILE = Path(__file__).parent.resolve() / Path('../files/hdf5_reader/banddos_bands.hdf')
    runner = CliRunner()
    args = [os.fspath(TEST_FILE), '--save', '--weight', 'MT:1s']
    with runner.isolated_filesystem():
        result = runner.invoke(plot_fleur_banddos_bands, args)

        print(result.output)
        assert result.exception is None, f'An unexpected exception occurred: {result.exception}'
        assert os.path.isfile('bandstructure.png')
