# -*- coding: utf-8 -*-
r"""

This module contains all custom exceptions/errors for the hdf5 file interaction.
"""


class Hdf5_Exception(Exception):
    """Generic exception for hdf2mic"""
    pass


class Hdf5_InitArgError(Hdf5_Exception):
    """Raised when reader attributes are set without a context manager"""
    pass


class Hdf5_DatasetDimensionError(Hdf5_Exception):
    """
    Raised when a read-in HDF5 Dataset's dimension conflicts present data
    """
    pass


class Hdf5_DatasetNotFoundError(Hdf5_Exception):
    """
    Raised when a group path for a Dataset in a HDF5 file returns
    None (i.e., the file has no such Dataset)
    """
    pass
