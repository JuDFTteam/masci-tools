"""
Tests of the hdf5_util functions
"""
import pytest
import h5py
from tempfile import TemporaryDirectory
import os
from pathlib import Path
from masci_tools.io.common_functions import convert_to_pystd


@pytest.fixture(name='hdf_file')
def hdf_file_fixture():
    """
    Create an example hdf file
    """
    with TemporaryDirectory() as td:
        testfilepath = os.fspath(Path(td) / 'mytestfile.hdf5')
        with h5py.File(testfilepath, 'w') as f:
            f.create_dataset('mydataset', (100,), dtype='i')
            g = f.create_group('subgroup')
            g.create_dataset('another_dataset', (50,), dtype='f')
            g.attrs['example_attribute'] = 'test'
            g.attrs['another_one'] = '10.0'
        yield testfilepath


def test_h5dump(hdf_file, capsys):
    """
    Test of h5dump
    """
    from masci_tools.io.hdf5_util import h5dump
    h5dump(hdf_file)
    captured = capsys.readouterr()
    assert captured.out.strip() == """mydataset: <class 'h5py._hl.dataset.Dataset'>
    Datatype: int32
    Shape: (100,)

subgroup: <class 'h5py._hl.group.Group'>
  Attributes:
    another_one: 10.0
    example_attribute: test

        another_dataset: <class 'h5py._hl.dataset.Dataset'>
             Datatype: float32
             Shape: (50,)"""
    assert captured.err == ''


def test_h5dump_group(hdf_file, capsys):
    """
    Test of h5dump with group argument
    """
    from masci_tools.io.hdf5_util import h5dump
    h5dump(hdf_file, group='/subgroup')
    captured = capsys.readouterr()
    assert captured.out.strip() == """Starting from path /subgroup
subgroup: <class 'h5py._hl.group.Group'>
   Attributes:
     another_one: 10.0
     example_attribute: test

This path contains:

another_dataset: <class 'h5py._hl.dataset.Dataset'>
    Datatype: float32
    Shape: (50,)"""
    assert captured.err == ''


def test_read_hdf_simple(hdf_file, data_regression):
    """
    Test of read_hdf_simple function
    """
    from masci_tools.io.hdf5_util import read_hdf_simple

    data, attributes = read_hdf_simple(hdf_file)

    data_regression.check({'data': convert_to_pystd(data), 'attributes': convert_to_pystd(attributes)})


def test_hdf5_reader_no_recipe(hdf_file, data_regression):
    """
    Test that the HDF5reader without recipe produces the same output as read_hdf_simple
    """
    from masci_tools.io.parsers.hdf5 import HDF5Reader

    with HDF5Reader(hdf_file) as h5reader:
        with pytest.warns(UserWarning):
            data, attributes = h5reader.read()

    data_regression.check({
        'data': convert_to_pystd(data),
        'attributes': convert_to_pystd(attributes)
    },
                          basename='test_read_hdf_simple')
