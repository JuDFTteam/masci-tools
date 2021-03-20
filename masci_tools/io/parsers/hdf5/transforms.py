# -*- coding: utf-8 -*-
import h5py
import numpy as np
from functools import wraps
from masci_tools.io.parsers.hdf5 import HDF5Reader


def hdf5_transformation(*, attribute_needed):

    def hdf5_transformation_decorator(func):
        """

        """

        @wraps(func)
        def transform_func(*args, **kwargs):
            return func(*args, **kwargs)

        if getattr(HDF5Reader, '_transforms', None) is None:
            HDF5Reader._transforms = {}  # pylint: disable=protected-access
            HDF5Reader._attribute_transforms = set()

        HDF5Reader._transforms[func.__name__] = transform_func  # pylint: disable=protected-access

        if attribute_needed:
            HDF5Reader._attribute_transforms.add(func.__name__)

        return transform_func

    return hdf5_transformation_decorator


@hdf5_transformation(attribute_needed=False)
def get_all_child_datasets(dataset, ignore):

    if isinstance(ignore, str):
        ignore = set([ignore])

    transformed = {}

    for key, val in dataset.items():
        if key in ignore:
            continue
        if isinstance(val, h5py.Dataset):
            transformed[key] = val

    return transformed


@hdf5_transformation(attribute_needed=False)
def get_first_element(dataset):
    """

   """

    return slice_dataset(dataset, 0)


@hdf5_transformation(attribute_needed=False)
def slice_dataset(dataset, slice_arg):
    """

    """
    if isinstance(dataset, dict):
        transformed = {key: data[slice_arg] for key, data in dataset.items()}
    else:
        transformed = dataset[slice_arg]

    return transformed


@hdf5_transformation(attribute_needed=False)
def scale_with_constant(dataset, scalar_value):
    """

    """
    transformed = dataset

    if isinstance(transformed, dict):
        transformed = {
            key: data * scalar_value if not isinstance(data, h5py.Dataset) else np.array(data) * scalar_value
            for key, data in dataset.items()
        }
    else:
        if isinstance(dataset, h5py.Dataset):
            transformed = np.array(dataset)
        transformed = transformed * scalar_value

    return transformed


@hdf5_transformation(attribute_needed=False)
def multiply_by_array(dataset, matrix, reverse_order=False, by_element=False):
    """

    """
    transformed = dataset

    if isinstance(transformed, dict):
        transformed = {
            key: np.array(entry) if isinstance(entry, h5py.Dataset) else entry for key, entry in transformed.items()
        }
    elif isinstance(transformed, h5py.Dataset):
        transformed = np.array(dataset)

    if isinstance(transformed, dict):
        if reverse_order:
            if by_element:
                transformed = {key: np.array([matrix.dot(row) for row in entry]) for key, entry in transformed.items()}
            else:
                transformed = {key: matrix.dot(entry) for key, entry in transformed.items()}
        else:
            if by_element:
                transformed = {key: np.array([row.dot(matrix) for row in entry]) for key, entry in transformed.items()}
            else:
                transformed = {key: entry.dot(matrix) for key, entry in transformed.items()}
    else:
        if reverse_order:
            if by_element:
                transformed = np.array([matrix.dot(row) for row in transformed])
            else:
                transformed = matrix.dot(transformed)
        else:
            if by_element:
                transformed = np.array([row.dot(matrix) for row in transformed])
            else:
                transformed = transformed.dot(matrix)

    return transformed


@hdf5_transformation(attribute_needed=False)
def calculate_norm(dataset, between_neighbours=False):

    transformed = dataset
    if isinstance(dataset, h5py.Dataset):
        transformed = np.array(dataset)

    if between_neighbours:
        transformed = np.array([np.linalg.norm(ki - kj) for ki, kj in zip(transformed[1:], transformed[:-1])])
    else:
        transformed = np.linalg.norm(transformed, axis=0)

    return transformed


@hdf5_transformation(attribute_needed=False)
def cumulative_sum(dataset):

    transformed = dataset
    if isinstance(dataset, h5py.Dataset):
        transformed = np.array(dataset)

    transformed = np.cumsum(transformed)

    return transformed


@hdf5_transformation(attribute_needed=False)
def get_attribute(dataset, attribute_name):
    """Extracts a specified attribute's value.

     :param name:
     :type dataset: Dataset
     :param attribute: attribute name
     :return:
   """
    transformed = dataset.attrs[attribute_name]

    return transformed


@hdf5_transformation(attribute_needed=False)
def attributes(dataset):
    """Extracts attributes of a dataset as a dict.

   :param name:
   :type dataset: Dataset
   :return: attributes dict
   """

    transformed = dict(dataset.attrs)

    return transformed


@hdf5_transformation(attribute_needed=False)
def move_to_memory(dataset):
    """Extracts attributes of a dataset as a dict.

    :param name:
    :type dataset: Dataset
    :return: attributes dict
    """

    transformed = dataset
    if isinstance(transformed, dict):
        for key, val in transformed.items():
            transformed[key] = move_to_memory(val)
    elif isinstance(transformed, h5py.Dataset):
        transformed = np.array(dataset)

    return transformed


@hdf5_transformation(attribute_needed=True)
def multiply_by_attribute(dataset, attribute_value, reverse_order=False, by_element=False):

    if isinstance(attribute_value, np.ndarray):
        transformed = multiply_by_array(dataset, attribute_value, reverse_order=reverse_order, by_element=by_element)
    else:
        transformed = scale_with_constant(dataset, attribute_value)

    return transformed


@hdf5_transformation(attribute_needed=True)
def add_partial_sums(dataset, attribute_value, pattern_format):

    if not isinstance(dataset, dict):
        raise ValueError('add_partial_sums only available for dict datasets')

    if not isinstance(attribute_value, (list, np.ndarray)):
        raise ValueError('attribute_value has be a list or array')

    transformed = dataset.copy()
    for val in attribute_value:
        pattern = pattern_format(val)

        transformed[pattern] = np.sum([entry for key, entry in transformed.items() if pattern in key], axis=0)

    return transformed


@hdf5_transformation(attribute_needed=False)
def convert_to_str(dataset):

    transformed = np.array(dataset).astype(str)

    return transformed
