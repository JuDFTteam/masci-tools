"""
Regression tests for the HDF5Reader class
"""
from masci_tools.io.common_functions import convert_to_pystd
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HDFTEST_DIR = os.path.join(CURRENT_DIR, 'files/hdf5_reader')


def test_hdf5_reader_bands(data_regression, test_file):
    """
    Tests of the bands recipe
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands

    with HDF5Reader(test_file('hdf5_reader/banddos_bands.hdf')) as reader:
        data, attrs = reader.read(recipe=FleurBands)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})


def test_hdf5_reader_spinpol_bands(data_regression, test_file):
    """
    Tests of the bands recipe
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands

    with HDF5Reader(test_file('hdf5_reader/banddos_spinpol_bands.hdf')) as reader:
        data, attrs = reader.read(recipe=FleurBands)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})


def test_hdf5_reader_dos(data_regression, test_file):
    """
    Tests of the dos recipe (also pass opened file handle)
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS

    with open(test_file('hdf5_reader/banddos_dos.hdf'), 'rb') as file:
        with HDF5Reader(file) as reader:
            data, attrs = reader.read(recipe=FleurDOS)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})


def test_hdf5_reader_spinpol_dos(data_regression, test_file):
    """
    Tests of the dos recipe (also pass opened file handle)
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS

    with HDF5Reader(test_file('hdf5_reader/banddos_spinpol_dos.hdf')) as reader:
        data, attrs = reader.read(recipe=FleurDOS)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})


def test_hdf5_reader_jdos(data_regression, test_file):
    """
    Tests of the dos recipe (also pass opened file handle)
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurJDOS

    with HDF5Reader(test_file('hdf5_reader/banddos_spinpol_dos.hdf')) as reader:
        data, attrs = reader.read(recipe=FleurJDOS)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})


def test_hdf5_reader_bands_specific_weight(data_regression, test_file):
    """
    Tests of the bands recipe
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import get_fleur_bands_specific_weights

    with HDF5Reader(test_file('hdf5_reader/banddos_bands.hdf')) as reader:
        data, attrs = reader.read(recipe=get_fleur_bands_specific_weights('MT:1d'))

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})
