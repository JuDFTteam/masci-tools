"""
Regression tests for the HDF5Reader class
"""
from masci_tools.io.common_functions import convert_to_pystd
import os
import pytest

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


def test_hdf5_reader_fileobjects(test_file):
    """
    Test the opening and closing of the HDF5file with
    different inputs
    We don't test the output but we make sure that the read runs through
    """
    import h5py
    from pathlib import Path
    from masci_tools.io.parsers.hdf5 import HDF5Reader
    from masci_tools.io.parsers.hdf5.recipes import FleurBands
    TEST_FILE = test_file('hdf5_reader/banddos_bands.hdf')

    with HDF5Reader(Path(TEST_FILE)) as reader:
        assert isinstance(reader.file, h5py.File)
        reader.read(recipe=FleurBands)

    with HDF5Reader(os.fsencode(TEST_FILE)) as reader:
        assert isinstance(reader.file, h5py.File)
        reader.read(recipe=FleurBands)

    with open(TEST_FILE, 'rb') as file:
        with HDF5Reader(file) as reader:
            assert isinstance(reader.file, h5py.File)
            reader.read(recipe=FleurBands)

    class FileHandleNoName:
        """
        File handle with no filename
        """

        def __init__(self, handle) -> None:
            self._handle = handle

        def __getattr__(self, name):
            if name != 'name':
                return getattr(self._handle, name)
            raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {name!r}')

    with open(TEST_FILE, 'rb') as file:
        with HDF5Reader(FileHandleNoName(file)) as reader:
            assert isinstance(reader.file, h5py.File)
            assert reader.filename == 'UNKNOWN'
            reader.read(recipe=FleurBands)

    with open(TEST_FILE, 'rb') as file:
        with HDF5Reader(FileHandleNoName(file), filename='test.hdf5') as reader:
            assert isinstance(reader.file, h5py.File)
            assert reader.filename == 'test.hdf5'
            reader.read(recipe=FleurBands)

    class FileHandleNoBackwardsSeek:
        """
        File handle with no support for seek with whence=2
        """

        def __init__(self, handle) -> None:
            self._handle = handle

        def seek(self, target, whence=0):
            if whence == 2:
                raise NotImplementedError
            return self._handle(target, whence=whence)

        def __getattr__(self, name):
            return getattr(self._handle, name)

    with pytest.raises(NotImplementedError):
        with open(TEST_FILE, 'rb') as file:
            h5py.File(FileHandleNoBackwardsSeek(file), 'r')

    with open(TEST_FILE, 'rb') as file:
        with HDF5Reader(FileHandleNoBackwardsSeek(file)) as reader:
            assert isinstance(reader.file, h5py.File)
            reader.read(recipe=FleurBands)
