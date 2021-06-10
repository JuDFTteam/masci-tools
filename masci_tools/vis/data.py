# -*- coding: utf-8 -*-
"""

"""
from collections import namedtuple
import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource


class PlotDataIterator:

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
                    key: self._plot_data.data[self._data_indx][val]
                    for key, val in columns._asdict().items()
                    if val is not None
                }
                self._data_indx += 1
            else:
                plot_data = {
                    key: self._plot_data.data[val] for key, val in columns._asdict().items() if val is not None
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


class PlotData:
    """Class for iterating over the data in a dict or dataframe with
      automatic filling in of single defined keys to get a list of
      keys to extract.

      The iteration allows for implicit definition of data for multiple
      plot sets, without excessive copying of the given data

      Usage Example

      .. code-block:: python

         from masci_tools.vis.plot_data import PlotData
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

    ALLOWED_DATA_HOLDERS = (dict, pd.DataFrame, ColumnDataSource
                            )  #These we know to be safely working as the data argument

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
        return [col for col, msk in zip(self.columns, self.mask) if msk]

    def __iter__(self):
        return PlotDataIterator(self, mode='values')

    def keys(self):
        return PlotDataIterator(self, mode='keys')

    def values(self):
        return PlotDataIterator(self, mode='values')

    def items(self):
        return PlotDataIterator(self, mode='items')

    def getfirst(self):
        for data in self.items():
            return data

    def getfirstvalue(self):
        for data in self.values():
            return data

    def getkeys(self, data_key):

        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        keys = []
        for entry in self.keys():
            keys.append(entry._asdict()[data_key])

        return keys

    def getvalues(self, data_key):

        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        values = []
        for entry in self.values():
            values.append(entry._asdict()[data_key])

        return values

    def min(self, data_key, separate=False):

        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        min_val = []
        for entry, source in self.items():

            key = entry._asdict()[data_key]

            if isinstance(source[key], (np.ndarray, pd.Series)):
                min_val.append(source[key].min())
            else:
                min_val.append(min(source[key]))

        if separate:
            return min_val
        else:
            return min(min_val)

    def max(self, data_key, separate=False):

        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        max_val = []
        for entry, source in self.items():

            key = entry._asdict()[data_key]

            if isinstance(source[key], (np.ndarray, pd.Series)):
                max_val.append(source[key].max())
            else:
                max_val.append(max(source[key]))

        if separate:
            return max_val
        else:
            return max(max_val)

    def apply(self, data_key, lambda_func):

        if data_key not in self._column_spec._fields:
            raise ValueError(f'Field {data_key} does not exist')

        for entry, source in self.items():

            key = entry._asdict()[data_key]

            if isinstance(source[key], (np.ndarray, pd.Series)):
                source[key] = lambda_func(source[key])
            else:
                source[key] = [lambda_func(value) for value in source[key]]

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


def normalize_list_or_array(data, key, out_data, flatten_np=False, forbid_split_up=False, single_plot=False):

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


def process_data_arguments(data,
                           single_plot=False,
                           mask=None,
                           use_column_source=False,
                           flatten_np=False,
                           forbid_split_up=None,
                           **kwargs):
    """
    Initialize PlotData from np.arrays or lists of np.arrays or lists

    The logic is as follows:


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
                                           forbid_split_up=key in forbid_split_up,
                                           single_plot=single_plot)
    else:
        keys = kwargs

    p_data = PlotData(data, mask=mask, use_column_source=use_column_source, **keys)

    if len(p_data) != 1 and single_plot:
        raise ValueError(f'Got multiple data sets ({len(p_data)}) but expected 1')

    return p_data
