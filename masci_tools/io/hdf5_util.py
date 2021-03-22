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
Small utility functions for inspecting hdf files and converting the
complete file structure into a python dictionary
"""

import h5py
import numpy as np


def hdfList(name, obj):
    """
    Print the name of the current object (indented to create a nice tree structure)

    Also prints attribute values and dataset shapes and datatypes
    """
    print(f"{name.split('/')[-1]:>{len(name)-1}}: {type(obj)}")

    ref_length = len(name) - len(name.split('/')[-1]) + 4

    if isinstance(obj, h5py.Dataset):
        print(f"{'Datatype:':>{ref_length+9}} {obj.dtype}")
        print(f"{'Shape:':>{ref_length+6}} {obj.shape}\n")

    if obj.attrs:
        print(f"{'Attributes:':>{ref_length+9}}")
        for attr_name, attr_val in obj.attrs.items():
            if len(attr_val) == 1:
                attr_val = attr_val[0]
            print(f'{attr_name:>{ref_length+len(attr_name)}}: {attr_val}')
        print('')


def h5dump(file, group='/'):
    """
    Shows the overall filestructure of an hdf file
    Goes through all groups and subgroups and prints the attributes
    or the shape and datatype of the datasets

    :param filepath: path to the hdf file
    """
    with h5py.File(file, 'r') as file_hdf:
        if group != '/':
            print(f'Starting from path {group}')
            hdfList(group, file_hdf[group])
            print('This path contains: \n')
        file_hdf[group].visititems(hdfList)


def read_hdf_simple(file, flatten=False):
    """
    Reads in an hdf file and returns its context in a nested dictionary

    :param filepath: path or filehandle to the hdf file
    :param flatten: bool, if True the dictionary will be flattened (does not check for lost information)

    :returns: two dictionaries, one with the datasets the other
              with the attributes in the file

    **Non unique group attribute or dataset names will be overwritten in the return dict**
    """

    datasets = {}
    group_attrs = {}

    with h5py.File(file, 'r') as file_hdf:
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
