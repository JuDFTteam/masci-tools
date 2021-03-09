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
IO routines for hdf files
"""

import h5py
import numpy as np


def read_hdf(filepath, flatten=False):
    """
    Reads in an hdf file and returns its context in a nested dictionary

    :param filepath: path to the hdf file
    :param flatten: bool, if True the dictionary will be flattened (does not check for lost information)

    :returns: two dictionaries, one with the datasets the other
              with the attributes in the file

    **Non unique group attribute or dataset names will be overwritten in the return dict**
    """

    datasets = {}
    group_attrs = {}

    with h5py.File(filepath, 'r') as file_hdf:
        datasets, group_attrs = read_groups(file_hdf, flatten=flatten)

    return datasets, group_attrs


def read_groups(hdfdata, flatten=False):
    """
    Recursive function to read a hdf datastructure and extract the datasets
    and attributes

    :param hdfdata: current hdf group to process
    :param flatten: bool, if True the dictionary will be flattened (does not check for lost information)

    :returns: two dictionaries, one with the datasets the other
              with the attributes in the file
    """
    datasets = {}
    attrs = {}

    for name, attr_val in hdfdata.attrs.items():
        if len(attr_val) == 1:
            attr_val = attr_val[0]
        attrs[name] = attr_val

    for key, val in hdfdata.items():

        if isinstance(val, h5py.Dataset):
            datasets[key] = np.array(val)
        else:
            new_datasets, new_attrs = read_groups(val, flatten=flatten)
            if not flatten:
                if new_datasets:
                    datasets[key] = new_datasets
                if new_attrs:
                    attrs[key] = new_attrs
            else:
                datasets.update(new_datasets)
                attrs.update(new_attrs)

    return datasets, attrs


def get_name_and_attributes(name, obj):
    """
    Print the name of the current object (indented to create a nice tree structure)

    Also prints attribute values and dataset shapes and datatypes
    """
    print(f"{name.split('/')[-1]:>{len(name)-1}}")

    if isinstance(obj, h5py.Dataset):
        print(f"{'Datatype:':>{len(name)+9}} {obj.dtype}")
        print(f"{'Shape:':>{len(name)+6}} {obj.shape}")

    if obj.attrs:
        print(f"{'Attributes:':>{len(name)+11}}")
        for attr_name, attr_val in obj.attrs.items():
            if len(attr_val) == 1:
                attr_val = attr_val[0]
            print(f'{attr_name:>{len(name)+len(attr_name)+1}}: {attr_val}')


def show_file_structure(filepath):
    """
    Shows the overall filestructure of an hdf file
    Goes through all groups and subgroups and prints the attributes
    or the shape and datatype of the datasets

    :param filepath: path to the hdf file
    """
    with h5py.File(filepath, 'r') as file_hdf:
        file_hdf.visititems(get_name_and_attributes)
