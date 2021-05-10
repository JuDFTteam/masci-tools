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
import logging

Transformation = namedtuple('Transformation', ['name', 'args', 'kwargs'])
AttribTransformation = namedtuple('AttribTransformation', ['name', 'attrib_name', 'args', 'kwargs'])

logger = logging.getLogger(__name__)


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
            self._filename = self._file.name
        else:
            self._filename = self._file

        if not self._filename.endswith('.hdf'):
            logger.exception('Wrong File Type for %s: Got %s', self.__class__.__name__, self._filename)
            raise ValueError(f'Wrong File Type for {self.__class__.__name__}: Got {self._filename}')

        logger.info('Instantiated %s with file %s', self.__class__.__name__, self._filename)

        self._move_to_memory = move_to_memory
        self._h5_file = None

    def __enter__(self):
        self._h5_file = h5py.File(self._file, 'r')
        logger.debug('Opened h5py.File with id %s', self._h5_file.id)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._h5_file.close()
        logger.debug('Closed h5py.File with id %s', self._h5_file.id)

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

        logger.debug('Reading dataset from path %s', h5path)

        dset = self._h5_file.get(h5path)
        if dset is not None:
            return dset
        elif strict:
            logger.exception('HDF5 input file %s has no Dataset at %s.', self._file, h5path)
            raise ValueError(f'HDF5 input file {self._file} has no Dataset at {h5path}.')
        return None

    def _transform_dataset(self, transforms, dataset, attributes=None, dataset_name=None):
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

            logger.debug('Applying transformation %s to dataset %s of type %s', spec.name, dataset_name,
                         type(transformed_dset))

            try:
                transformed_dset = self._transforms[spec.name](transformed_dset, *args, **spec.kwargs)
            except Exception as err:
                logger.exception(str(err))
                raise

        return transformed_dset

    @staticmethod
    def _unpack_dataset(output_dict, dataset_name):
        """
        Unpack the entires of the dictionary dataset in the entry dataset_name into the
        output_dict

        :param output_dict: dict with the dataset entries
        :param dataset_name: key of the dataset to unpack into output_dict

        :returns: output_dict with the entries of dataset_name unpacked
        """

        logger.debug('Unpacking dict dataset %s after transformations', dataset_name)

        if not isinstance(output_dict[dataset_name], dict):
            raise ValueError(f'{dataset_name} cannot be unpacked: Got {type(output_dict[dataset_name])}')

        unpack_dict = output_dict.pop(dataset_name)

        if unpack_dict.keys() & output_dict.keys():
            raise ValueError('Unpacking would result in lost information: \n'
                             f"Intersection of keys: '{unpack_dict.keys().intersection(output_dict.keys())}'")

        return {**output_dict, **unpack_dict}

    def read(self, recipe=None):
        """Extracts datasets from HDF5 file, transforms them and puts all into a namedtuple.

        :param recipe: dict with the format given in :py:mod:`~masci_tools.io.parsers.hdf5.recipes`

        :returns: two dicts with the datasets/attributes read in and transformed according to the recipe
        """
        from itertools import chain
        from masci_tools.io.hdf5_util import read_hdf_simple

        logger.info('Started reading HDF file: %s', self._filename)

        if recipe is None:
            msg = 'Using the HDF5Reader without a recipe falling back to simple HDF reader'
            logging.warning(msg)
            warnings.warn(msg)
            res = read_hdf_simple(self._file)
            logger.info('Finished reading .hdf file')
            return res

        datasets = recipe.get('datasets', {})
        attributes = recipe.get('attributes', {})

        # remove entries whose key is an empty string
        h5paths = {item['h5path'] for item in chain(datasets.values(), attributes.values())}
        extracted_datasets = {h5path: self._read_dataset(h5path) for h5path in h5paths}

        output_attrs = {}
        for key, val in attributes.items():
            transforms = val.get('transforms', [])
            output_attrs[key] = self._transform_dataset(transforms, extracted_datasets[val['h5path']], dataset_name=key)
            if val.get('unpack_dict', False):
                try:
                    output_attrs = self._unpack_dataset(output_attrs, dataset_name=key)
                except Exception as err:
                    logger.exception(str(err))
                    raise

        output_data = {}
        for key, val in datasets.items():
            transforms = val.get('transforms', [])
            output_data[key] = self._transform_dataset(transforms,
                                                       extracted_datasets[val['h5path']],
                                                       attributes=output_attrs,
                                                       dataset_name=key)
            if val.get('unpack_dict', False):
                try:
                    output_data = self._unpack_dataset(output_data, dataset_name=key)
                except Exception as err:
                    logger.exception(str(err))
                    raise

        if self._move_to_memory:
            logger.debug('Moving remaining h5py.Datasets to memory')
            try:
                self._transforms['move_to_memory'](output_data)
                self._transforms['move_to_memory'](output_attrs)
            except Exception as err:
                logger.exception(str(err))
                raise

        logger.info('Finished reading HDF file: %s', self._filename)

        return output_data, output_attrs
