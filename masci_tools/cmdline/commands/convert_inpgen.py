"""
CLI commands for converting common structure definition formats to fleur inpgen files
"""
from .root import cli
import click

from pathlib import Path
import os

from masci_tools.cmdline.utils import echo

try:
    import pymatgen
    from pymatgen.core import Structure
except ImportError:
    pymatgen = None

try:
    import ase
    from ase.io import read, write
except ImportError:
    ase = None


@cli.command('convert-inpgen')
@click.argument('input-file', type=click.Path(exists=True, path_type=Path, resolve_path=True))
@click.argument('output-file', type=click.Path(path_type=Path, resolve_path=True))
@click.option('-c',
              '--converter',
              type=click.Choice(['ase', 'pymatgen']),
              help='Which library is used to read in the given file format',
              default='pymatgen')
def convert_inpgen(input_file, output_file, converter):
    """Convert the given file to an fleur inpgen file
    """

    input_file = os.fspath(input_file)
    output_file = os.fspath(output_file)

    if converter == 'ase':
        if ase is None:
            echo.echo_critical('ase is not installed. Please install the packages ase and ase-fleur')

        atoms = read(input_file)
        write(output_file, atoms, format='fleur-inpgen')
    elif converter == 'pymatgen':
        if pymatgen is None:
            echo.echo_critical('pymatgen is not installed. Please install the packages pymatgen and pymatgen-io-fleur')

        struc = Structure.from_file(os.fspath(input_file))
        struc.to(output_file, fmt='fleur-inpgen')
