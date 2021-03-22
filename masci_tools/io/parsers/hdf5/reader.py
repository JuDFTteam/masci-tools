# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
#                                                                             #
###############################################################################
"""
This module contains a generic HDF5 reader
"""
import io
import h5py
from collections import namedtuple
import warnings

Transformation = namedtuple('Transformation', ['name', 'args', 'kwargs'])
AttribTransformation = namedtuple('AttribTransformation', ['name', 'attrib_name', 'args', 'kwargs'])


class HDF5Reader:
    """Class for reading in data from hdf5 files using a specified recipe

    :param file: filepath to hdf file or opened file handle (mode 'rb')
    :param move_to_memory: bool if True after reading and transforming the data
                           all leftover h5py.Datasets are moved into np.arrays

    The recipe is passed to the :py:meth:`HDF5Reader.read()` method and consists
    of a dict specifiying which attributes and datasets to read in and how to transform them

    Each attribute/dataset entry corresponds to one entry point in the given `.hdf` file
    Available transformations can either be found in :py:mod:`~masci_tools.io.parsers.hdf5.transforms`
    or can be defined by the user with the :py:func:`~masci_tools.io.parsers.hdf5.transforms.hdf5_transformation`
    decorator

    Basic Usage:

    .. code-block:: python

        from masci_tools.io.parsers.hdf5 import HDF5Reader
        import masci_tools.io.parsers.hdf5.recipes as recipes

        #This example shows the usage for producing data from a bandstructure calculation
        #in Fleur
        with HDF5Reader('/path/to/hdf/banddos.hdf') as h5reader:
            data, attributes = h5reader.read(recipe=recipes.FleurBands)
        print(data, attributes)

    """

    def __init__(self, file, move_to_memory=True):

        self._file = file

        if isinstance(self._file, io.IOBase):
            filename = self._file.name
        else:
            filename = self._file

        assert filename.endswith('.hdf'), f'Wrong File Type for {self.__class__}: Got {filename}'

        self._move_to_memory = move_to_memory
        self._h5_file = None

    def __enter__(self):
        self._h5_file = h5py.File(self._file, 'r')
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._h5_file.close()

    def _read_dataset(self, h5path, strict=True):
        """Return in the dataset specified by the given h5path

        :param h5path : str, HDF5 group path in file.
        :param strict : bool if no dataset is at the path and strcit is True raise Error
                        else return None

        :returns: h5py.Dataset or None

        :raises: ValueError if no dataset is at path and strict is True
        """
        if h5path in ('/', ''):
            if strict:
                return None
            else:
                pass

        dset = self._h5_file.get(h5path)
        if dset is not None:
            return dset
        elif strict:
            raise ValueError(f'HDF5 input file {self._file} has no Dataset at {h5path}.')
        return None

    def _transform_dataset(self, transforms, dataset, attributes=None):
        """
        Transforms the given dataset with the given list of tasks

        :param transforms: list of namedtuples defining the tasks to perform
        :param dataset: h5py.Dataset, on which to perform the operations
        :param attributes: dict of previously processed attributes.
                           Only available to the entries in the datasets
                           section of the recipe. This allows for operations with
                           the previously parsed attributes

        :returns: the dataset with all the transformations applied
        """
        transformed_dset = dataset
        for spec in transforms:

            args = spec.args
            if spec.name in self._attribute_transforms:
                if attributes is None:
                    raise ValueError('Attribute transform not allowed for attributes')
                attrib_value = attributes[spec.attrib_name]
                args = attrib_value, *args

            transformed_dset = self._transforms[spec.name](transformed_dset, *args, **spec.kwargs)

        return transformed_dset

    def read(self, recipe=None):
        """Extracts datasets from HDF5 file, transforms them and puts all into a namedtuple.

        :param recipe: dict with the format given in :py:mod:`~masci_tools.io.parsers.hdf5.recipes`

        :returns: two dicts with the datasets/attributes read in and transformed according to the recipe
        """
        from itertools import chain
        from masci_tools.io.hdf5_util import read_hdf_simple

        if recipe is None:
            warnings.warn('You are using the HDF5Reader without a recipe falling back to simple HDF reader')
            return read_hdf_simple(self._file)

        datasets = recipe.get('datasets', {})
        attributes = recipe.get('attributes', {})

        # remove entries whose key is an empty string
        h5paths = {item['h5path'] for item in chain(datasets.values(), attributes.values())}
        extracted_datasets = {h5path: self._read_dataset(h5path) for h5path in h5paths}

        output_attrs = {}
        for key, val in attributes.items():
            transforms = val.get('transforms', [])
            output_attrs[key] = self._transform_dataset(transforms, extracted_datasets[val['h5path']])
            if val.get('unpack_dict', False):
                if not isinstance(output_attrs[key], dict):
                    raise ValueError(f'{key} cannot be unpacked: Got {type(output_attrs[key])}')

                unpack_dict = output_attrs.pop(key)

                if unpack_dict.keys() & output_attrs.keys():
                    raise ValueError('Unpacking would result in lost information: \n'
                                     f"Intersection of keys: '{unpack_dict.keys().intersection(output_attrs.keys())}'")

                output_attrs = {**output_attrs, **unpack_dict}

        output_data = {}
        for key, val in datasets.items():
            transforms = val.get('transforms', [])
            output_data[key] = self._transform_dataset(transforms,
                                                       extracted_datasets[val['h5path']],
                                                       attributes=output_attrs)
            if val.get('unpack_dict', False):
                if not isinstance(output_data[key], dict):
                    raise ValueError(f'{key} cannot be unpacked: Got {type(output_data[key])}')

                unpack_dict = output_data.pop(key)
                if unpack_dict.keys() & output_data.keys():
                    raise ValueError('Unpacking would result in lost information: \n'
                                     f"Intersection of keys: '{unpack_dict.keys().intersection(output_data.keys())}'")

                output_data = {**output_data, **unpack_dict}

        if self._move_to_memory:
            self._transforms['move_to_memory'](output_data)
            self._transforms['move_to_memory'](output_attrs)

        return output_data, output_attrs
