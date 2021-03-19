# -*- coding: utf-8 -*-
import h5py
import numpy as np
from functools import wraps
from masci_tools.util.hdf5.reader import HDF5Reader


def hdf5_transformation(func):
    """

    """

    @wraps(func)
    def transform_func(*args, **kwargs):
        return func(*args, **kwargs)

    if not hasattr(HDF5Reader, '_transforms'):
        HDF5Reader._transforms = {}  # pylint: disable=protected-access

    HDF5Reader._transforms[func.__name__] = transform_func  # pylint: disable=protected-access

    return transform_func


@hdf5_transformation
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


@hdf5_transformation
def get_first_element(dataset):
    """

   """

    return slice_dataset(dataset, 0)


@hdf5_transformation
def slice_dataset(dataset, slice_arg):
    """

    """
    if isinstance(dataset, dict):
        transformed = {key: data[slice_arg] for key, data in dataset.items()}
    else:
        transformed = dataset[slice_arg]

    return transformed


@hdf5_transformation
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


@hdf5_transformation
def get_attribute(dataset, attribute_name):
    """Extracts a specified attribute's value.

     :param name:
     :type dataset: Dataset
     :param attribute: attribute name
     :return:
   """
    transformed = dataset.attrs[attribute_name]

    return transformed


@hdf5_transformation
def attributes(self, dataset):
    """Extracts attributes of a dataset as a dict.

   :param name:
   :type dataset: Dataset
   :return: attributes dict
   """

    transformed = dict(dataset.attrs)

    return transformed
