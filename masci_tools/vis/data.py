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
This module contains classes and functions to make plotting functions
more flexible with respect to the used data. This way plotting functions
can both allow the flexible usage of lists, arrays directly or dataframes
together with the keys that should be used
"""
from collections import namedtuple
import numpy as np
import pandas as pd
import copy
from bokeh.models import ColumnDataSource

class PlotData:
    """Class for iterating over the data in a dict or dataframe with
      automatic filling in of single defined keys to get a list of
      keys to extract.

      The iteration allows for implicit definition of data for multiple
      plot sets, without excessive copying of the given data

      Usage Example

      .. code-block:: python

         from masci_tools.vis.data import PlotData
         import numpy as np

         #Let's say we have one energy grid and a couple of functions
         #defined on this energy grid.
         #We collect these in a dict

         x = np.linspace(-10,10,100)
         data = {'x': x, 'y1': np.sin(x), 'y2':np.cos(x), 'y3', x**2}

         p = PlotData(data, x='x', y=['y1', 'y2', 'y3'])

         #If we now iterate over this object it will result in the data
         #for y being returned together with the x data (The same would work the other way around)
         for entry in p:
            print(entry.x) #'x' entry
            print(entry.y) #'y1' then 'y2' and finally 'y3'

         #Additionally data for z, color and size can be defined


      :param data: object or list of objects which can be bracket indexed with the given keys
                   e.g. dicts, pandas dataframes, ...
      :param mask: optional list or Tuple of bool, of the same length as the specified data
                   When iterating over it only the objects with the mask set to True are returned

      Kwargs are used to specify the columns in a namedtuple
      If a list is given for any of the keys the data will be expanded to a list of
      namedtuple with the same length

    """

    #These we know to be safely working as the data argument
    #In principle this could be extended to any Mapping
    ALLOWED_DATA_HOLDERS = (dict, pd.DataFrame, ColumnDataSource
                            )

    def __init__(self, data, mask=None, use_column_source=False, **kwargs):

        self.data = data

        if isinstance(self.data, list):
            assert isinstance(self.data[0], self.ALLOWED_DATA_HOLDERS), f'Wrong type for data argument: Got {self.data}'
            dict_data = isinstance(self.data[0], dict)
        else:
            assert isinstance(self.data, self.ALLOWED_DATA_HOLDERS), f'Wrong type for data argument: Got {self.data}'
            dict_data = isinstance(self.data, dict)

        if dict_data and use_column_source:
            if isinstance(self.data, list):
                for index, entry in enumerate(self.data):
                    self.data[index] = ColumnDataSource(entry)
            else:
                self.data = ColumnDataSource(self.data)

        self._column_spec = namedtuple('Columns', list(kwargs.keys()))

        if any(isinstance(val, list) for val in kwargs.values()):
            num_sets = max(len(val) for val in kwargs.values() if isinstance(val, list))

            if isinstance(self.data, list):
                if len(self.data) != num_sets:
                    raise ValueError('Mismatch in lengths between data and indices')

            column_args = {}
            for key, val in kwargs.items():
                if isinstance(val, list):
                    if len(val) != num_sets:
                        raise ValueError(f'Mismatch of dimensions: {val} num_sets: {num_sets}')
                    column_args[key] = val
                else:
                    column_args[key] = [val] * num_sets

            self.columns = [
                self._column_spec(**{key: value[index]
                                     for key, value in column_args.items()})
                for index in range(num_sets)
            ]
        else:
            if isinstance(self.data, list):
                num_sets = len(self.data)
            else:
                num_sets = 1
            self.columns = [self._column_spec(**kwargs)] * num_sets

        if mask is None:
            mask = [True] * num_sets
        if not isinstance(mask, (list, tuple)) or len(mask) != num_sets:
            raise ValueError(f'Wrong Value for mask: {mask}')
        self.mask = mask

    @property
    def masked_columns(self):
        """
        Return the columns that are not disabled by the mask argument
        """
        return [col for col, msk in zip(self.columns, self.mask) if msk]

    def __iter__(self):
        """
        Iterate over PlotData. Returns the values for the data
        """
        return PlotDataIterator(self, mode='values')

    def keys(self):
        """
        Iterate over PlotData keys. Returns the keys for the corresponding sources
        """
        return PlotDataIterator(self, mode='keys')

    def values(self):
        """
        Iterate over PlotData values. Returns the values for the data
        """
        return PlotDataIterator(self, mode='values')

    def items(self):
        """
        Iterate over PlotData items. Returns the key and corresponding source for the data
        """
        return PlotDataIterator(self, mode='items')

    def getfirst(self):
        """
        Get the first item in the data
        """
        for data in self.items():
            return data

    def getfirstvalue(self):
        """
        Get the values in the first entry of the data
        """
        for data in self.values():
            return data

    def getfirstkeys(self):
        """
        Get the keys in the first entry of the data
        """
        for data in self.keys():
            return data

    def getkeys(self, data_key):
        """
        Get the keys for a given data column for all entries

        :param data_key: name of the data key to return the keys

        :returns: list of keys, corresponding to the entries for the
                  given data in the sources
        """
        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        keys = []
        for entry in self.keys():
            keys.append(entry._asdict()[data_key])

        return keys

    def getvalues(self, data_key):
        """
        Get the values for a given data column for all entries

        :param data_key: name of the data key to return the values

        :returns: list of values, corresponding to the entries for the
                  given data in the sources
        """
        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        values = []
        for entry in self.values():
            values.append(entry._asdict()[data_key])

        return values

    def min(self, data_key, separate=False, mask=None):
        """
        Get the minimum value for a given data column for all entries

        :param data_key: name of the data key to determine the minimum
        :param separate: bool if True the minimum will be determined and returned
                         for all entries separately
        :param mask: optional mask to select specifc rows from the data entries

        :returns: minimum value for all entries either combined or as a list
        """
        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        if mask is not None:
            if len(mask) == len(self):
                mask_gen = (mask_indx for mask_indx in mask)
            else:
                mask_gen = (mask for i in self)
        else:
            mask_gen = (None for i in self)

        min_val = []
        for (entry, source), mask in zip(self.items(), mask_gen):

            key = entry._asdict()[data_key]

            if mask is None:
                data = source[key]
            else:
                data = source[key][mask]

            if isinstance(source[key], (np.ndarray, pd.Series)):
                min_val.append(data.min())
            else:
                min_val.append(min(data))

        if separate:
            return min_val
        else:
            return min(min_val)

    def max(self, data_key, separate=False, mask=None):
        """
        Get the maximum value for a given data column for all entries

        :param data_key: name of the data key to determine the maximum
        :param separate: bool if True the maximum will be determined and returned
                         for all entries separately
        :param mask: optional mask to select specifc rows from the data entries

        :returns: maximum value for all entries either combined or as a list
        """
        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        if mask is not None:
            if len(mask) == len(self):
                mask_gen = (mask_indx for mask_indx in mask)
            else:
                mask_gen = (mask for i in range(len(self)))
        else:
            mask_gen = (None for i in range(len(self)))

        max_val = []
        for (entry, source), mask in zip(self.items(), mask_gen):

            key = entry._asdict()[data_key]

            if mask is None:
                data = source[key]
            else:
                data = source[key][mask]

            if isinstance(source[key], (np.ndarray, pd.Series)):
                max_val.append(data.max())
            else:
                max_val.append(max(data))

        if separate:
            return max_val
        else:
            return max(max_val)

    def apply(self, data_key, lambda_func):
        """
        Apply a function to a given data column for all entries

        .. warning::
            This operation is done in-place. Meaning if there are multiple
            data entries pointing to the same data set and only one should be
            modified by this method, the data needs to be copied beforehand
            using :py:meth:`copy_data()`

        :param data_key: name of the data key to determine the maximum
        :param lambda_func: function to apply to the data
        """
        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        for indx, (entry, source) in enumerate(self.items()):

            key = entry._asdict()[data_key]

            if isinstance(source[key], pd.Series):
                if isinstance(source, pd.DataFrame):
                    dataframe_func = lambda x: lambda_func(x) if x.name == key else x
                    new_source = source.apply(dataframe_func)
                    if isinstance(self.data, list):
                        self.data[indx] = new_source
                    else:
                        self.data = new_source
                else:
                    source[key] = source[key].apply(lambda_func)
            elif isinstance(source[key], np.ndarray):
                source[key] = lambda_func(source[key])
            else:
                source[key] = [lambda_func(value) for value in source[key]]

    def copy_data(self, data_key_from, data_key_to, prefix=None, rename_original=False):
        """
        Copy the data for a given data key to another one

        :param data_key_from: data key to copy from
        :param data_key_to: data key to copy to
        :param prefix: optional prefix to use for the renamed data entries. Can be used
                       to avoid name clashes. If not given the data keys are used
        :param rename_original: optional bool (default False). If True the original entries are renamed
                                instead of the ones under ``data_key_to``
        """
        if data_key_from not in self._column_spec._fields:
            raise ValueError(f'Field {data_key_from} does not exist')

        if data_key_to not in self._column_spec._fields:
            raise ValueError(f'Field {data_key_to} does not exist')

        for indx, (entry, source) in enumerate(self.items()):

            key = entry._asdict()[data_key_from]
            if rename_original:
                new_key = f'{prefix}_{indx}' if prefix is not None else f'{data_key_from}_{indx}'
                self.columns[indx] = entry._replace(**{data_key_from: new_key, data_key_to: key})
            else:
                new_key = f'{prefix}_{indx}' if prefix is not None else f'{data_key_to}_{indx}'
                self.columns[indx] = entry._replace(**{data_key_to: new_key})

            if new_key in source:
                raise ValueError(f'Key {new_key} already exists')

            if isinstance(source, pd.DataFrame):
                new_column = pd.Series(data=source[key], name=new_key, copy=True)
                new_source = pd.concat([source, new_column], axis=1)
                if isinstance(self.data, list):
                    self.data[indx] = new_source
                else:
                    self.data = new_source
            elif isinstance(source, ColumnDataSource):
                source.add(copy.copy(source[key]), name=new_key)
            else:
                source[new_key] = copy.copy(source[key])

    def __len__(self):
        return len(self.masked_columns)

    def __getitem__(self, key):
        if isinstance(self.data, list):
            if isinstance(key, tuple):
                return self.data[key[0]][key[1:]]
            else:
                raise KeyError("No index given but data is a list. Provide key as '(index,key)'")
        else:
            return self.data[key]

    def export(self, **kwargs):
        raise NotImplementedError

class PlotDataIterator:
    """
    Class containing the iteration behaviour over the
    :py:class:`PlotData` class. Can be used in three modes:

      - `keys`: Returns the keys to be entered in the corresponding data sources for each entry
      - `values`: Returns the data for each entry
      - `items`: Returns the keys and the data sources in a tuple

    The keys and values are always returned in a ``namedtuple`` with fields corresponding
    to the set data keys
    """
    def __init__(self, plot_data, mode='values'):
        self._plot_data = plot_data
        self._column_iter = iter(col for col, msk in zip(self._plot_data.columns, self._plot_data.mask) if msk)

        self._data_indx = 0
        self._iter_mode = mode

    def __iter__(self):
        return self

    def __next__(self):
        columns = next(self._column_iter)
        if self._iter_mode == 'keys':
            return columns
        elif self._iter_mode == 'values':
            if isinstance(self._plot_data.data, list):
                plot_data = {
                    key: self._plot_data.data[self._data_indx][val] if val is not None else None
                    for key, val in columns._asdict().items()
                }
                self._data_indx += 1
            else:
                plot_data = {
                    key: self._plot_data.data[val] if val is not None else None
                    for key, val in columns._asdict().items()
                }
            return self._plot_data._column_spec(**plot_data)
        elif self._iter_mode == 'items':
            if isinstance(self._plot_data.data, list):
                data_source = self._plot_data.data[self._data_indx]
                self._data_indx += 1
            else:
                data_source = self._plot_data.data
            return columns, data_source
        raise StopIteration


def normalize_list_or_array(data, key, out_data, flatten_np=False, forbid_split_up=False):
    """
    Split up a given list/numpy array or pd.Series to be used in the plotting methods

    :param data: The (array-like) data to be normalized
    :param key: key under which to enter the new data
    :param out_data: dict containining previously normalized data
    :param flatten_np: bool, if True multidimensional numpy arrays are flattened
    :param forbid_split_up: bool, if True multidimensional arrays are not split up

    The rules are the following:
        - if ``data`` is a multidimesional array (list of lists, etc.)
          and it is not forbidden by the given argument the first dimension
          of the array is iterated over and interpreted as separate entries
          (if the data was previously split up into multiple sets a length check is performed)
        - if ``data`` is a one-dimensional array and of a different length than the
          number of defined data sets it is added to all previously existing entries
        - if ``data`` is a one-dimensional array and of the same length as the
          number of defined data sets each entry is added to the corresponding data set

    :returns: list of dicts or dict containing the nomralized data
    """
    LIST_TYPES = (list, np.ndarray, pd.Series)

    if isinstance(data, np.ndarray) and flatten_np:
        data = data.flatten()

    if isinstance(data, LIST_TYPES):
        if isinstance(data[0], LIST_TYPES) and not forbid_split_up:
            #Split up
            if isinstance(out_data, list):
                if len(out_data) != len(data):
                    raise ValueError(
                        f"Mismatch of dimensions: Got two different dimensions 'key' {len(data)} 'previous' {len(out_data)}"
                    )
                for entry, new_data in zip(out_data, data):
                    entry[key] = new_data
            else:
                new_list = []
                for new_data in data:
                    new_list.append(out_data.copy())
                    new_list[-1][key] = new_data
                out_data = new_list

            return out_data
        elif isinstance(out_data, list):
            if len(out_data) == len(data):
                for entry, new_data in zip(out_data, data):
                    entry[key] = new_data
                return out_data

    if isinstance(out_data, list):
        for entry in out_data:
            entry[key] = data
    else:
        out_data[key] = data

    return out_data


def process_data_arguments(data=None,
                           single_plot=False,
                           mask=None,
                           use_column_source=False,
                           flatten_np=False,
                           forbid_split_up=None,
                           **kwargs):
    """
    Initialize PlotData from np.arrays or lists of np.arrays or lists or a already given
    data argument, i.e. mapping

    :param data: either None or Mapping to be used as the data in the PlotData class
    :param single_plot: bool, if True only a single dataset is allowed
    :param mask: list of bools deactivating some data sets for plotting
    :param use_column_source: bool, if True all data arguments are converted to ColumnDataSource of bokeh
    :param flatten_np: bool, if True multidimensional numpy arrays are flattened (Only if data not given)
    :param forbid_split_up: set of keys for which not to split up multidimensional arrays


    Kwargs define which keys belong to which data entries if data is given or they contain
    the data to be normalized

    The following two example calls will both create a PlotData object with the same two
    plot data sets with the entries ``x`` and ``y``::

        import numpy as np

        x = np.linspace(-10,10,100)
        y1 = y**2
        y2 = np.sin(x)

        #Use a predefined data argument (a dict in this case) and the keys in the kwargs
        p = process_data_arguments({'x': x, 'y1': y1, 'y2': y2}, x='x', y=['y1','y2'])

        #Let the function normalize the given arrays
        p = process_data_arguments=(x=x,y=[y1, y2])

    :returns: A :py:class:`PlotData` object corresponding to the given data
    """

    if forbid_split_up is None:
        forbid_split_up = set()

    if data is None:
        data = {}
        keys = {}

        for key, val in kwargs.items():
            if val is not None:
                keys[key] = key
            else:
                keys[key] = None
            data = normalize_list_or_array(val,
                                           key,
                                           data,
                                           flatten_np=flatten_np,
                                           forbid_split_up=key in forbid_split_up)
    else:
        keys = kwargs

    p_data = PlotData(data, mask=mask, use_column_source=use_column_source, **keys)

    if len(p_data) != 1 and single_plot:
        raise ValueError(f'Got multiple data sets ({len(p_data)}) but expected 1')

    return p_data
