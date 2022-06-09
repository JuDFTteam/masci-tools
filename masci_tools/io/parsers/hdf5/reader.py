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
from __future__ import annotations

import tempfile
import shutil
import os
from types import TracebackType
import h5py
import warnings
import logging
from pathlib import Path
from typing import IO, Callable, NamedTuple, Any, cast
from masci_tools.util.typing import FileLike
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict


class Transformation(NamedTuple):
    name: str
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}


class AttribTransformation(NamedTuple):
    name: str
    attrib_name: str
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}


class HDF5Transformation(TypedDict, total=False):
    h5path: str  #This should strictly be marked as required when it's possible
    transforms: list[Transformation | AttribTransformation]
    unpack_dict: bool
    description: str


class HDF5LimitedTransformation(TypedDict, total=False):
    h5path: str  #This should strictly be marked as required when it's possible
    transforms: list[Transformation]
    unpack_dict: bool
    description: str


class HDF5Recipe(TypedDict, total=False):
    datasets: dict[str, HDF5Transformation]
    attributes: dict[str, HDF5LimitedTransformation]


logger = logging.getLogger(__name__)


class HDF5Reader:
    """Class for reading in data from hdf5 files using a specified recipe

    :param file: filepath to hdf file or opened file handle (mode 'rb')
    :param move_to_memory: bool if True after reading and transforming the data
                           all leftover h5py.Datasets are moved into np.arrays
    :param filename: Name of the file. Only used for logging. If not given and the file
                     provides the information extract it from there

    The recipe is passed to the :py:meth:`HDF5Reader.read()` method and consists
    of a dict specifying which attributes and datasets to read in and how to transform them

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

    _transforms: dict[str, Callable[[Any], Any]] = {}
    _attribute_transforms: set[str] = set()

    def __init__(self, file: FileLike, move_to_memory: bool = True, filename: str = 'UNKNOWN') -> None:

        self._original_file = file
        self.file: h5py.File = None
        self._tempfile: IO[Any] | None = None

        self.filename = filename
        if self.filename == 'UNKNOWN':
            self.filename, extension = self._get_filename_and_extension(self._original_file)
        else:
            extension = Path(self.filename).suffix

        if extension and extension not in ('.hdf', '.hdf5', '.h5'):
            logger.exception('Wrong File Type for %s: Got %s', self.__class__.__name__, self.filename)
            raise ValueError(f'Wrong File Type for {self.__class__.__name__}: Got {self.filename}')

        logger.info('Instantiated %s with file %s', self.__class__.__name__, self.filename)

        self._move_to_memory = move_to_memory

    def __enter__(self) -> HDF5Reader:
        try:
            self.file = h5py.File(self._original_file, 'r')
        except NotImplementedError:
            #This except clause catches a special case resulting from
            #the AiiDA v2 file repository. The h5py.File constructor
            #wants to determine the end of the file stream and tries
            #`os.seek` with the argument `whence=2` (i.e. read starting from the end of the stream)
            #The AiiDA v2 file repository cannot support this case if the
            #files are compressed/packed (compressed streams want to be read only forwards)
            #To circumvent this we copy the file into a temporary file and
            #construct the File this way. Notice that we do not lose performance
            #if the files are not yet packed, e.g. while workflows are running :)
            #The solution below is taken out of a mailing list suggestion for this
            #exact problem
            self._tempfile = tempfile.TemporaryFile()
            # Copy the content of source to target in chunks
            shutil.copyfileobj(self._original_file, self._tempfile)  #type: ignore[arg-type]
            self._tempfile.seek(0)  # Make sure to reset the pointer to the beginning of the stream
            self.file = h5py.File(self._tempfile, 'r')

        logger.debug('Opened h5py.File with id %s', self.file.id)
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None,
                 exc_traceback: TracebackType | None) -> None:
        self.file.close()
        if self._tempfile is not None:
            self._tempfile.close()
        logger.debug('Closed h5py.File with id %s', self.file.id)

    @staticmethod
    def _get_filename_and_extension(file: FileLike) -> tuple[str, str]:
        """Extract the filename and extension of the given file if possible
        """
        filename: str = getattr(file, 'name', 'UNKNOWN')
        if isinstance(file, bytes):
            filename = os.fsdecode(file)
        elif isinstance(file, str):
            filename = file

        return filename, Path(filename).suffix

    def _read_dataset(self, h5path: str, strict: bool = True) -> h5py.Dataset | None:
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

        logger.debug('Reading dataset from path %s', h5path)

        dset = self.file.get(h5path)
        if dset is not None:
            return dset
        if strict:
            logger.exception('HDF5 input file %s has no Dataset at %s.', self.filename, h5path)
            raise ValueError(f'HDF5 input file {self.filename} has no Dataset at {h5path}.')
        return None

    def _transform_dataset(self,
                           transforms: list[Transformation] | list[Transformation | AttribTransformation],
                           dataset: h5py.Dataset,
                           attributes: dict[str, Any] | None = None,
                           dataset_name: str | None = None) -> Any:
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
                spec = cast(AttribTransformation, spec)
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
    def _unpack_dataset(output_dict: dict[str, Any], dataset_name: str) -> dict[str, Any]:
        """
        Unpack the entries of the dictionary dataset in the entry dataset_name into the
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

    def read(self, recipe: HDF5Recipe | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
        """Extracts datasets from HDF5 file, transforms them and puts all into a namedtuple.

        :param recipe: dict with the format given in :py:mod:`~masci_tools.io.parsers.hdf5.recipes`

        :returns: two dicts with the datasets/attributes read in and transformed according to the recipe
        """
        from itertools import chain
        from masci_tools.io.hdf5_util import read_hdf_simple

        logger.info('Started reading HDF file: %s', self.filename)

        if recipe is None:
            msg = 'Using the HDF5Reader without a recipe falling back to simple HDF reader'
            logging.warning(msg)
            warnings.warn(msg)
            res = read_hdf_simple(self._original_file)
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
        for key, val in datasets.items():  #type:ignore
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

        logger.info('Finished reading HDF file: %s', self.filename)

        return output_data, output_attrs
