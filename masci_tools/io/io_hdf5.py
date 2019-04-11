# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
#                                                                             #
###############################################################################

"""
IO routines for hdf
"""


from __future__ import absolute_import
import six
def read_hdf(filepath):
    """
    Reads in an hdf file and returns its context in a nested dictionary
    
    !Only works for files with unique group and dataset names
    """
    import h5py
    
    datasets = {}
    group_attrs = {}
    groups = []
    file_hdf = h5py.File(filepath, 'r')
    groups = list(file_hdf.keys())
    
    for key, val in six.iteritems(file_hdf):
        for k, v in six.iteritems(val):
            datasets[k] = v.value
        attr = val.attrs
        for ke, val in six.iteritems(attr):
            group_attrs[ke] = val
    file_hdf.close()
    
    return datasets, groups, group_attrs