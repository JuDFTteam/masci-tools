# -*- coding: utf-8 -*-
r"""his module contains all custom exceptions/errors for the hdf5 file interaction.
"""


class Hdf5_Exception(Exception):
    """Generic exception for hdf2mic"""
    pass


class Hdf5_DatasetNotFoundError(Hdf5_Exception):
    """
    Raised when a group path for a Dataset in a HDF5 file returns
    None (i.e., the file has no such Dataset)
    """
    pass
