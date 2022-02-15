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
Collection of predefined transformations for the :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader` class

All Transformation have to be able to handle (or fail gracefully with a clear error)
for the following 3 cases:

    1. The dataset is still a h5py.Dataset and might need to be transformed to a numpy array
    2. The dataset is a numpy array
    3. The dataset is a dict. This is needed to read arbitrary child dataset, where not all labels
       are known. Two options can be chosen apply the transformation to all keys in the dict
       or throw an error
"""
from __future__ import annotations

from typing import Callable
import h5py
import numpy as np
from functools import wraps
from collections import defaultdict
from .reader import HDF5Reader


class HDF5TransformationError(Exception):
    pass


def hdf5_transformation(*, attribute_needed: bool) -> Callable:
    """
    Decorator for registering a function as a transformation functions
    on the :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader` class

    :param attribute_needed: bool if True this function takes a previously processed
                             attribute value and is therefore only available for the entries in datasets
    """

    def hdf5_transformation_decorator(func: Callable) -> Callable:
        """
        Return decorated HDF5Reader object with _transforms dict and
        _attribute_transforms set attribute
        Here all registered transforms are inserted
        """
        #pylint: disable=protected-access

        @wraps(func)
        def transform_func(*args, **kwargs):
            """Decorator for transformation function"""
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                raise HDF5TransformationError(f'The HDF5 transformation {func.__name__} failed with {exc}') from exc

        HDF5Reader._transforms[func.__name__] = transform_func

        if attribute_needed:
            HDF5Reader._attribute_transforms.add(func.__name__)

        return transform_func

    return hdf5_transformation_decorator


@hdf5_transformation(attribute_needed=False)
def get_first_element(dataset):
    """
    Get the first element of the dataset.

    :param dataset: dataset to transform

    :returns: first element of the dataset
    """
    return index_dataset(dataset, 0)


@hdf5_transformation(attribute_needed=False)
def index_dataset(dataset, index):
    """
    Get the n-th element of the dataset.

    :param dataset: dataset to transform

    :returns: first element of the dataset
    """
    if isinstance(dataset, dict):
        transformed = {key: data[index] for key, data in dataset.items()}
    else:
        transformed = dataset[index]

    return transformed


@hdf5_transformation(attribute_needed=False)
def slice_dataset(dataset, slice_arg):
    """
    Slice the dataset with the given slice argument.

    :param dataset: dataset to transform
    :param slice_arg: slice to apply to the dataset

    :returns: first element of the dataset
    """
    if isinstance(dataset, dict):
        transformed = {key: data[slice_arg] for key, data in dataset.items()}
    else:
        transformed = dataset[slice_arg]

    return transformed


@hdf5_transformation(attribute_needed=False)
def get_shape(dataset):
    """
    Get the shape of the dataset.

    :param dataset: dataset to get the shape

    :returns: shape of the dataset
    """

    if isinstance(dataset, dict):
        transformed = {key: data.shape for key, data in dataset.items()}
    else:
        transformed = dataset.shape

    return transformed


@hdf5_transformation(attribute_needed=False)
def get_name(dataset, full_path=False):
    """
    Get the name of the dataset.

    :param dataset: dataset to get the shape
    :param full_path: bool, if True the full path to the dataset is returned

    :returns: name of the dataset
    """

    if isinstance(dataset, (list, np.ndarray)):
        raise ValueError('Dataset has to be a h5py.Dataset for get_name')

    if isinstance(dataset, dict):
        if full_path:
            transformed = {key: data.name for key, data in dataset.items()}
        else:
            transformed = {key: data.name.split('/')[-1] for key, data in dataset.items()}
    elif full_path:
        transformed = dataset.name
    else:
        transformed = dataset.name.split('/')[-1]

    return transformed


@hdf5_transformation(attribute_needed=False)
def tile_array(dataset, n_repeats):
    """
    Use numpy.tile to repeat array n-times

    :param dataset: dataset to transform
    :param attribute_shape: int, time sto repeat the given array

    :returns: dataset repeated n-times
    """
    if isinstance(dataset, dict):
        transformed = {key: np.tile(dataset, n_repeats) for key, data in dataset.items()}
    else:
        transformed = np.tile(dataset, n_repeats)

    return transformed


@hdf5_transformation(attribute_needed=False)
def repeat_array(dataset, n_repeats):
    """
    Use numpy.repeat to repeat each element in array n-times

    :param dataset: dataset to transform
    :param n_repeats: int, time to repeat each element

    :returns: dataset with elements repeated n-times
    """
    if isinstance(dataset, dict):
        transformed = {key: np.repeat(dataset, n_repeats) for key, data in dataset.items()}
    else:
        transformed = np.repeat(dataset, n_repeats)

    return transformed


@hdf5_transformation(attribute_needed=False)
def get_all_child_datasets(group, ignore=None, contains=None):
    """
    Get all datasets contained in the given group

    :param group: h5py object to extract from
    :param ignore: str or iterable of str (optional). These
                   keys will be ignored
    :param contains: str or iterable of str (optional). This phrase has to be in the key


    :returns: a dict with the contained dataset entered with their names as keys
    """
    if ignore is None:
        ignore = set()

    if isinstance(ignore, str):
        ignore = {ignore}

    transformed = {}
    for key, val in group.items():
        if any(phrase in key for phrase in ignore):
            continue
        if contains is not None:
            if any(phrase not in key for phrase in contains):
                continue
        if isinstance(val, h5py.Dataset):
            transformed[key] = val

    return transformed


@hdf5_transformation(attribute_needed=False)
def merge_subgroup_datasets(group,
                            ignore=None,
                            contains=None,
                            ignore_group=None,
                            contains_group=None,
                            stack_results=True,
                            sort_key=None):
    """
    Get all datasets contained in the given group

    :param group: h5py object to extract from
    :param ignore_group: str or iterable of str (optional). These
                   keys will be ignored
    :param contains_group: str or iterable of str (optional). This phrase has to be in the key
    :param ignore: str or iterable of str (optional). These
                   keys of the datasets in the subgroup will be ignored
    :param contains: str or iterable of str (optional). This phrase has to be in the key of the datasets in the subgroup
    :param stack_results: bool if True the resulting list of datasets will be used to construct one numpy array

    :returns: a dict with the contained dataset of the subgroups of the given group entered with their names as keys
    """
    if ignore_group is None:
        ignore_group = set()

    if isinstance(ignore_group, str):
        ignore_group = {ignore_group}

    transformed = defaultdict(list)

    for key in sorted(group.keys(), key=sort_key):
        val = group[key]
        if any(phrase in key for phrase in ignore_group):
            continue
        if contains_group is not None:
            if any(phrase not in key for phrase in contains_group):
                continue
        if isinstance(val, h5py.Group):
            subgroup_dsets = get_all_child_datasets(val, ignore=ignore, contains=contains)
            for k, v in subgroup_dsets.items():
                transformed[k].append(v)

    if stack_results:
        transformed = {key: np.stack(val) for key, val in transformed.items()}

    return transformed


@hdf5_transformation(attribute_needed=False)
def stack_datasets(dataset, axis=0, sort_key=None):
    """
    Stack the entries in the given dict dataset along the given axis

    :param dataset: dict dataset to transform
    :param axis: int along which axis should be stacked

    :returns: the array resulting from stacking all entries in the dictionary
    """

    if not isinstance(dataset, dict):
        raise NotImplementedError

    keys = sorted(dataset.keys(), key=sort_key)
    return np.stack([dataset[key] for key in keys], axis=axis)


@hdf5_transformation(attribute_needed=False)
def shift_dataset(dataset, scalar_value, negative=False):
    """
    Shift the dataset by the given scalar_value

    :param dataset: dataset to transform
    :param scalar_value: value to shift the dataset by
    :param negative: bool, if True the scalar_value will be subtracted

    :returns: the dataset shifted by the scalar
              if it is a dict all entries are shifted
    """
    transformed = dataset
    if isinstance(transformed, dict):
        transformed = {
            key: np.array(entry) if isinstance(entry, h5py.Dataset) else entry for key, entry in transformed.items()
        }
    elif isinstance(transformed, h5py.Dataset):
        transformed = np.array(transformed)

    if isinstance(transformed, dict):
        if negative:
            transformed = {key: entry - scalar_value for key, entry in transformed.items()}
        else:
            transformed = {key: entry + scalar_value for key, entry in transformed.items()}
    else:
        if negative:
            transformed = transformed - scalar_value
        else:
            transformed = transformed + scalar_value

    return transformed


@hdf5_transformation(attribute_needed=False)
def multiply_scalar(dataset, scalar_value):
    """
    Multiply the given dataset with a scalar_value

    :param dataset: dataset to transform
    :param scalar_value: value to multiply the dataset by

    :returns: the dataset multiplied by the scalar
              if it is a dict all entries are multiplied
    """
    transformed = dataset
    if isinstance(transformed, dict):
        transformed = {
            key: np.array(entry) if isinstance(entry, h5py.Dataset) else entry for key, entry in transformed.items()
        }
    elif isinstance(transformed, h5py.Dataset):
        transformed = np.array(transformed)

    if isinstance(transformed, dict):
        transformed = {key: entry * scalar_value for key, entry in transformed.items()}
    else:
        transformed = transformed * scalar_value

    return transformed


@hdf5_transformation(attribute_needed=False)
def convert_to_complex_array(dataset):
    """
    Converts the given dataset of real numbers into
    dataset of complex numbers. This follows the convention of
    how complex numbers are normally written out by Fleur
    (last index 0 real part, last index 1 imag part)

    :param dataset: dataset to transform

    :returns: dataset with complex values
    """
    transformed = dataset
    if isinstance(transformed, dict):
        transformed = {
            key: np.array(entry) if isinstance(entry, h5py.Dataset) else entry for key, entry in transformed.items()
        }
    elif isinstance(transformed, h5py.Dataset):
        transformed = np.array(transformed)

    if isinstance(transformed, dict):
        transformed = {key: entry[..., 0] + 1j * entry[..., 1] for key, entry in transformed.items()}
    else:
        transformed = transformed[..., 0] + 1j * transformed[..., 1]

    return transformed


@hdf5_transformation(attribute_needed=False)
def multiply_array(dataset, matrix, transpose=False):
    """
    Multiply the given dataset with a matrix

    :param dataset: dataset to multiply
    :param matrix: matrix to multiply by
    :param transpose: bool, if True the given matrix is transposed

    :returns: dataset multiplied with the given matrix
    """

    transformed = dataset

    if isinstance(transformed, dict):
        transformed = {
            key: np.array(entry) if isinstance(entry, h5py.Dataset) else entry for key, entry in transformed.items()
        }
    elif isinstance(transformed, h5py.Dataset):
        transformed = np.array(dataset)

    if transpose:
        matrix = matrix.T

    if isinstance(transformed, dict):
        transformed = {key: entry.dot(matrix) for key, entry in transformed.items()}
    else:
        transformed = transformed.dot(matrix)

    return transformed


@hdf5_transformation(attribute_needed=False)
def calculate_norm(dataset, between_neighbours=False):
    """
    Calculate norms on the given dataset. Calculates the norm of each row in the dataset

    :param dataset: dataset to transform
    :param between_neighbours: bool, if True the distance between subsequent entries in the dataset is calculated

    :returns: norms of the given dataset
    """
    transformed = dataset
    if isinstance(dataset, h5py.Dataset):
        transformed = np.array(dataset)

    if isinstance(dataset, dict):
        raise NotImplementedError

    if between_neighbours:
        transformed = np.array([np.linalg.norm(ki - kj) for ki, kj in zip(transformed[1:], transformed[:-1])])
    else:
        transformed = np.linalg.norm(transformed, axis=0)

    return transformed


@hdf5_transformation(attribute_needed=False)
def cumulative_sum(dataset, beginning_zero=True):
    """
    Calculate the cumulative sum of the dataset

    :param dataset: dataset to transform

    :returns: cumulative sum of the dataset
    """

    if isinstance(dataset, dict):
        raise NotImplementedError

    transformed = dataset
    if isinstance(dataset, h5py.Dataset):
        transformed = np.array(dataset)

    if beginning_zero:
        transformed = np.insert(transformed, 0, 0.0)

    transformed = np.cumsum(transformed)

    return transformed


@hdf5_transformation(attribute_needed=False)
def get_attribute(dataset, attribute_name):
    """Extracts a specified attribute's value.

    :param dataset: dataset to transform
    :param attribute_name: str of the attribute to extract from the dataset

    :returns: value of the attribute on the dataset
    """
    if isinstance(dataset, (np.ndarray, dict)):
        raise NotImplementedError

    transformed = dataset.attrs[attribute_name]

    return transformed


@hdf5_transformation(attribute_needed=False)
def attributes(dataset):
    """Extracts all attributes of the dataset

    :param dataset: dataset to transform

    :returns: dict with all the set attributes on the dataset
    """
    if isinstance(dataset, (np.ndarray, dict)):
        raise NotImplementedError

    transformed = dict(dataset.attrs)

    return transformed


@hdf5_transformation(attribute_needed=False)
def move_to_memory(dataset):
    """Moves the given dataset to memory, if it's not already there
    Creates numpy arrays for each dataset it finds

    :param dataset: dataset to transform

    :returns: dataset with h5py.Datasets converted to numpy arrays
    """

    transformed = dataset
    if isinstance(transformed, dict):
        for key, val in transformed.items():
            transformed[key] = move_to_memory(val)
    elif isinstance(transformed, h5py.Dataset):
        transformed = np.array(dataset)

    return transformed


@hdf5_transformation(attribute_needed=False)
def flatten_array(dataset, order='C'):
    """
    Flattens the given dataset to one dimensional array.
    Copies the array !!

    :param dataset: dataset to transform
    :param order: str {`C`, `F`, `A`, `K`} flatten in column major
                  or row-major order (see numpy.flatten documentation)

    :returns: flattened dataset
    """

    transformed = dataset
    if isinstance(transformed, dict):
        transformed = {
            key: np.array(entry) if isinstance(entry, h5py.Dataset) else entry for key, entry in transformed.items()
        }
    elif isinstance(transformed, h5py.Dataset):
        transformed = np.array(transformed)

    if isinstance(transformed, dict):
        transformed = {key: entry.flatten(order=order) for key, entry in transformed.items()}
    else:
        transformed = transformed.flatten(order=order)

    return transformed


@hdf5_transformation(attribute_needed=False)
def split_array(dataset, suffixes=None, name=None):
    """
    Split the arrays in a dataset into multiple entries
    by their first index

    If the dataset is a dict the entries will be split up.
    If the dataset is not a dict a dict is created with the dataset
    entered under `name` and this will be split up

    :param dataset: dataset to transform
    :param suffix: Optional list of str to use for suffixes
                   for the split up entries. by default it is
                   the value of the first index of the original
                   array
    :param name: str for the case of the dataset not being a
                 dict. Key for the entry in the new dict for
                 the original dataset. The returned dataset will only
                 contain the split up entries

    :param dataset: dict with the entries split up
    """

    if not isinstance(dataset, dict) and name is None:
        raise ValueError('split_arrays has to be given a name if the dataset is not a dict')

    transformed = dataset
    if not isinstance(dataset, dict):
        transformed = {name: dataset}

    transformed = {
        key: np.array(entry) if isinstance(entry, h5py.Dataset) else entry for key, entry in transformed.items()
    }
    max_length = max(len(entry) for entry in transformed.values())

    if suffixes is None:
        suffixes = list(range(max_length))

    if len(suffixes) < max_length:
        raise ValueError(f'Too few suffixes provided: Expected {max_length} Got: {len(suffixes)}')

    for key in list(transformed.keys()):
        val = transformed.pop(key)
        for suffix, entry in zip(suffixes, val):
            transformed[f'{key}_{suffix}'] = entry

    return transformed


@hdf5_transformation(attribute_needed=False)
def convert_to_str(dataset, join=False):
    """Converts the given dataset to a numpy array of type string

    :param dataset: dataset to transform
    :param join: bool if True the result will be joined together

    :returns: numpy array of dtype str
    """

    transformed = np.array(dataset).astype(str)
    if join:
        transformed = ''.join(transformed)

    return transformed


@hdf5_transformation(attribute_needed=False)
def apply_lambda(dataset, lambda_func):
    """Applies a given lambda function to the dataset
       This should be used with care. One possible example is
       converting to a boolean with lambda x: x==1

    :param dataset: dataset to transform
    :param lambda_func: lambda function to apply to the dataset

    :returns: return value of the lambda function
    """

    transformed = dataset
    if isinstance(transformed, dict):
        transformed = {key: lambda_func(entry) for key, entry in transformed.items()}
    else:
        transformed = lambda_func(dataset)

    return transformed


@hdf5_transformation(attribute_needed=False)
def periodic_elements(dataset):
    """Converts the given dataset (int or list of ints)
       To the atomic symbols corresponding to the atomic number

    :param dataset: dataset to transform

    :returns: str or array of str with the atomic elements
    """
    from masci_tools.util.constants import PERIODIC_TABLE_ELEMENTS

    if isinstance(dataset, dict):
        raise NotImplementedError

    if isinstance(dataset, int):
        transformed = PERIODIC_TABLE_ELEMENTS[dataset]['symbol']
    else:
        transformed = np.array([PERIODIC_TABLE_ELEMENTS[entry]['symbol'] for entry in dataset], dtype=str)

    return transformed


@hdf5_transformation(attribute_needed=False)
def sum_over_dict_entries(dataset, overwrite_dict=False, entries=None, dict_entry='sum', entry_format=None):
    """
    Sum the datasets contained in the given dict dataset

    :param dataset: dataset to transform
    :param overwrite_dict: bool if True, the result will overwrite the dictionary
                           if False it is entered under `sum` in the dict

    :returns: dataset with summed entries
    """

    if not isinstance(dataset, dict):
        raise ValueError('sum_over_dict_entries is only available for dict datasets')

    if entries is None:
        entries = dataset.keys()

    if entry_format is not None:
        entries = [entry_format(entry) for entry in entries]

    transformed = dataset
    if overwrite_dict:
        transformed = np.sum([entry for key, entry in dataset.items() if key in entries], axis=0)
    else:
        transformed[dict_entry] = np.sum([entry for key, entry in dataset.items() if key in entries], axis=0)

    return transformed


@hdf5_transformation(attribute_needed=False)
def add_partial_sums_fixed(dataset, patterns, replace_entries=None):
    """
    Add entries to the dataset dict (Only available for dict datasets) with sums
    over entries containing a given pattern

    Used for example in the FleurBands recipe to calculate total atom weights
    with the patterns `['MT:1', 'MT:2', ...]`

    :param dataset: dataset to transform
    :param patterns: list of str to sum entries over
    :param replace_entries: list of str under which to enter the entries back

    :returns: dataset with new entries containing the sums over entries matching the given pattern
    """
    from collections.abc import Iterable

    if not isinstance(dataset, dict):
        raise ValueError('add_partial_sums_fixed only available for dict datasets')

    if not isinstance(patterns, Iterable) and not isinstance(patterns, str):
        raise ValueError('patterns has be an Iterable')

    if replace_entries is None:
        replace_entries = patterns

    transformed = dataset.copy()
    for pattern, replace_entry in zip(patterns, replace_entries):
        entries = [key for key in transformed.keys() if pattern in key]

        transformed[replace_entry] = sum_over_dict_entries(dataset, overwrite_dict=True, entries=entries)

    return transformed


#Functions that can use an attribute value (These are passed in from _transform_dataset)
#The transformation don't have access to all the attributes


@hdf5_transformation(attribute_needed=True)
def multiply_by_attribute(dataset, attribute_value, transpose=False):
    """
    Multiply the given dataset with a previously parsed attribute, either scalar or matrix like

    :param dataset: dataset to transform
    :param attribute_value: value to multiply by (attribute value passed in from `_transform_dataset`)

    Only relevant for matrix multiplication:
        :param transpose: bool if True the Matrix order is transposed before multiplying

    :returns: dataset multiplied with the given attribute_value
    """
    if isinstance(attribute_value, h5py.Dataset):
        attribute_value = np.array(attribute_value)

    if isinstance(attribute_value, np.ndarray):
        transformed = multiply_array(dataset, attribute_value, transpose=transpose)
    else:
        transformed = multiply_scalar(dataset, attribute_value)

    return transformed


@hdf5_transformation(attribute_needed=True)
def shift_by_attribute(dataset, attribute_value, negative=False):
    """
    Shift the dataset by the given value of the attribute

    :param dataset: dataset to transform
    :param attribute_value: value to shift the dataset by
    :param negative: bool, if True the scalar_value will be subtracted

    :returns: the dataset shifted by the scalar
              if it is a dict all entries are shifted
    """
    return shift_dataset(dataset, attribute_value, negative=negative)


@hdf5_transformation(attribute_needed=True)
def add_partial_sums(dataset, attribute_value, pattern_format, make_set=False, replace_entries=None):
    """
    Add entries to the dataset dict (Only available for dict datasets) with sums
    over entries containing a given pattern formatted with a attribute_value

    Used for example in the FleurBands recipe to calculate total atom weights
    with the pattern_format `'MT:{}'.format` and the atomtype as the attribute_value

    :param dataset: dataset to transform
    :param attribute_value: value to multiply by (attribute value passed in from `_transform_dataset`)
    :param pattern_format: callable returning a formatted string
                           This will be called with every entry in the attribute_value list
    :param replace_entries: list of str under which to enter the entries back

    :returns: dataset with new entries containing the sums over entries matching the given pattern
    """
    if isinstance(attribute_value, h5py.Dataset):
        attribute_value = np.array(attribute_value)

    if not isinstance(dataset, dict):
        raise ValueError('add_partial_sums only available for dict datasets')

    if not isinstance(attribute_value, (list, np.ndarray)):
        raise ValueError('attribute_value has be a list or array')

    if make_set:
        attribute_value = set(attribute_value)
    sum_patterns = [
        pattern_format(val) for val in attribute_value if any(pattern_format(val) in key for key in dataset.keys())
    ]

    return add_partial_sums_fixed(dataset, sum_patterns, replace_entries=replace_entries)


@hdf5_transformation(attribute_needed=True)
def repeat_array_by_attribute(dataset, attribute_value):
    """
    Use numpy.repeat to repeat each element in array n-times (given by attribute_value)

    :param dataset: dataset to transform
    :param attribute_shape: int, time to repeat the elements in the given array

    :returns: dataset with elements repeated n-times
    """
    return repeat_array(dataset, attribute_value)


@hdf5_transformation(attribute_needed=True)
def tile_array_by_attribute(dataset, attribute_value):
    """
    Use numpy.tile to repeat array n-times (given by attribute_value)

    :param dataset: dataset to transform
    :param attribute_shape: int, time sto repeat the given array

    :returns: dataset repeated n-times
    """
    return tile_array(dataset, attribute_value)
