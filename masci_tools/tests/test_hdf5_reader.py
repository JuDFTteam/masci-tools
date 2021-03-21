# -*- coding: utf-8 -*-
"""
Regression tests for the HDF5Reader class
"""
from masci_tools.io.common_functions import convert_to_pystd
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HDFTEST_DIR = os.path.join(CURRENT_DIR, 'files/hdf5_reader')


def test_hdf5_reader_bands(data_regression):
    """
    Tests of the bands recipe
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_bands.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as reader:
        data, attrs = reader.read(recipe=FleurBands)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})


def test_hdf5_reader_dos(data_regression):
    """
    Tests of the dos recipe (also pass opened file handle)
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_dos.hdf')

    with open(TEST_BANDDOS_FILE, 'rb') as file:
        with HDF5Reader(file) as reader:
            data, attrs = reader.read(recipe=FleurDOS)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})


def test_hdf5_reader_spinpol_dos(data_regression):
    """
    Tests of the dos recipe (also pass opened file handle)
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurDOS

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as reader:
        data, attrs = reader.read(recipe=FleurDOS)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})


def test_hdf5_reader_jdos(data_regression):
    """
    Tests of the dos recipe (also pass opened file handle)
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurJDOS

    TEST_BANDDOS_FILE = os.path.join(HDFTEST_DIR, 'banddos_spinpol_dos.hdf')

    with HDF5Reader(TEST_BANDDOS_FILE) as reader:
        data, attrs = reader.read(recipe=FleurJDOS)

    data_regression.check({'datasets': convert_to_pystd(data), 'attributes': convert_to_pystd(attrs)})
