# -*- coding: utf-8 -*-
"""
This module contains a generic HDF5 reader
"""
import io
import h5py


class HDF5Reader:
    """Class for reading in data from hdf5 files


    :param file: filepath to hdf file or opened file handle (mode 'rb')
    :param move_to_memory: bool if True after reading and transforming the data
                           all leftover h5py.Datasets are moved into np.arrays

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

        transformed_dset = dataset
        for spec in transforms:
            if isinstance(spec, tuple):
                action_name, args = spec[0], spec[1:]
            else:
                action_name, args = spec, ()

            if action_name in self._attribute_transforms:
                if attributes is None:
                    raise ValueError('Attribute transform not allowed for attributes')
                attrib_value = attributes[args[0]]
                args = attrib_value, *args[1:]

            transformed_dset = self._transforms[action_name](transformed_dset, *args)

        return transformed_dset

    def read(self, recipe):
        """Extracts datasets from HDF5 file, transforms them and puts all into a namedtuple.

        :param recipe: dict with the format given in :py:mod:`~masci_tools.recipes.py`

        :returns: dict with the data read in and transformed according to the recipe
        """
        from itertools import chain

        datasets = recipe.get('datasets', {})
        attributes = recipe.get('attributes', {})

        # remove entries whose key is an empty string
        h5paths = {item['h5path'] for item in chain(datasets.values(), attributes.values())}
        extracted_datasets = {h5path: self._read_dataset(h5path, strict=False) for h5path in h5paths}

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
