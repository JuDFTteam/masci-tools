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

      Kwargs are used to specify the columns according to the :py:class:`PlotColumns` namedtuple
      If a list is given for any of the keys the data will be expanded to a list of
      :py:class:`PlotColumns` with the same length

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

        if any(key not in self.column_spec._fields for key in kwargs):
            raise ValueError(f'Invalid data argument: {kwargs} \n' f'Allowed are: {self.column_spec._fields}')

        self._column_spec = namedtuple('Columns', list(kwargs.keys()))

        if any(isinstance(val, list) for val in kwargs.values()):
            num_sets = max(len(val) for val in kwargs.values() if isinstance(val, list))

            if isinstance(self.data, list):
                raise ValueError('Only one of the data or indices can be lists')

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
        for data in self:
            return data

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


def normalize_lists_or_arrays(cls, data, keys=None, mask=None, use_column_source=False, **kwargs):
    """
   Initialize PlotData from np.arrays or lists of np.arrays or lists

   The logic is as follows:


   """

    def process_list_or_array(data, key, out_data):
        #Lists are assumed to be split up (except ehen there is only a list of values) up np.arrays not
        if isinstance(data, list):
            if isinstance(data[0], (list, np.ndarray)):
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

    x, y = data

    processed_data = {}

    processed_data = process_list_or_array(x, 'x', processed_data)
    processed_data = process_list_or_array(y, 'y', processed_data)

    construct_keys = {}

    for key, val in kwargs.items():
        if val is None:
            continue
        construct_keys[key] = key
        processed_data = process_list_or_array(val, key, processed_data)

    return PlotData(processed_data, mask=mask, use_column_source=use_column_source, **construct_keys)
