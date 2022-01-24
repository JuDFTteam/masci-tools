# pylint: disable=unused-import
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
"""This subpackage contains the tabulator class for the tabulator subpackage, which turns
properties of a collections of objects into a table.
"""
from __future__ import annotations

import abc
from collections import defaultdict
from typing import Any, FrozenSet, Iterable, TypeVar

import pandas as pd
import numpy as np

from .recipes import Recipe, KeyPaths

__all__ = ('Tabulator', 'NamedTupleTabulator', 'TableType')

TableType = TypeVar('TableType', 'dict[str,Any]', pd.DataFrame)


class Tabulator(abc.ABC):
    """For tabulation of a collection of objects' (common) properties into a dict or dataframe.

    List of external implementations:

    - aiida-jutools/io `NodeTabulator` for nodes -> pandas DataFrame.

    TODO: increase memory performance:

    The following points are meant for the `NodeTabulator` implementation, but may be of interest for other
    implementations.

    - use optional dtypes from recipe (see TODO in Recipe) when building table. otherwise, e.g. when returning
      pandas dataframe, all columns will have dtype 'object' or 'float64' and the table won't fit into memory
      anymore very quickly.
    - internal storage format dict of lists while building must remain, but when finished, convert to dict
      of numpy arrays -> more memory efficient. for repeated tabulate() calls (to build larger table), have
      to adjust code to concatenate new lists to existing numpy arrays when finished.
    - change tabulate() signature: should not return table, only build it. another method (e.g. table @property
      getter) should return table and before del (delete) its inner storage (self._table) of it, because return
      will likely create a copy. that way can ~half the memory footprint.
    - when returning pandas dataframe, and recipe supplied no dtypes, use automatic downcasting to smallest dtype
      for numeric types (pd.to_numeric), and maybe 'categorical' for string coluns (if num unique values << num
      values). See pandas > Scaling to large datasets for more.
    - maybe add save option (or method) and read() method to read in tabulated table. for pandas, that allow a user
      to easily reuse the dtypes information from the recipe.
    """

    def __init__(self, recipe: Recipe | None = None, separator: str = '.', buffer_size: int = 1024) -> None:
        """Initialize a tabulator object.

        The attribute :py:attr:`~.recipe` defines *what* to extract from a set of objects and put them in a table (
        properties = column names of the table, one table row per object), with property transformations if needed.
        The tabulator on the other hand, knows *how* to extract those properties. It depends on the nature of the
        objects. Therefore, different implementations of the tabulator exist for different object types, and the
        base class is abstract.

        If no recipe is given, a default empty recipe will be used, and if :py:meth:`~tabulate` is called, the
        empty include list of the recipe will be replaced by an auto-generated extensive include list of object
        properties via the :py:meth:`~autolist` method.

        :param recipe: Optional recipe.
        :param kwargs: Additional keyword arguments for subclasses.
        """
        if not recipe:
            recipe = Recipe()
        self.recipe = recipe
        self.has_transformer = recipe.transformer is not None
        self._table: dict[str, Any] = {}

        self.separator = separator
        self.buffer_size = buffer_size

        self._column_policies = ['flat', 'flat_full_path', 'multiindex']

    @abc.abstractmethod
    def autolist(self, item: Any, overwrite: bool = False, pretty_print: bool = False, **kwargs: Any) -> None:
        """Auto-generate an list of properties to be included in the generated table from a given object.

        This can serve as an overview for customized include and exclude lists.
        :param item: An example object of a type compatible with the tabulator.
        :param overwrite: True: replace recipe list with the auto-generated list. False: Only if recipe list empty.
        :param pretty_print: True: Print the generated list in pretty format.
        :param kwargs: Additional keyword arguments for subclasses.
        """

    @abc.abstractmethod
    def get_value(self, item: Any, keypath: Iterable[str]) -> Any:
        """
        Extract a value based the path given as an iterable of attribute names
        :param item: Item under consideration
        :param keypath: path to the attribute/value of interest

        :returns: Value under that keypath
        """
        pass

    def clear(self) -> None:
        """Clear table if already tabulated."""
        self._table = {}

    @property
    def table(self) -> pd.DataFrame | None:
        """The result table. None if :py:meth:`~tabulate` not yet called."""
        return pd.DataFrame.from_dict(self._table) if self._table else None

    def process_item(self, item: Any, index: int, table: dict[str, Any], keypaths: list[tuple[tuple[str, ...], str]],
                     dtypes: frozenset[str], pass_item_to_transformer: bool, **kwargs: Any) -> None:
        """
        Process a single item of the collection of items to be tabulated

        :param item: Item to be tabulated
        :param table: dict of the already tabulated data
        :param keypaths: list of the paths to tabulate
        :param pass_item_to_transformer: If a transformer is specified should the item be passed
        :param kwargs: Additional arguments passed to the transformer
        """

        failed_paths = defaultdict(list)
        failed_transforms = defaultdict(list)

        for keypath, column in keypaths:
            value = self.get_value(item, keypath)
            if value is None:
                failed_paths[keypath].append(self.item_uuid(item))
                continue

            if self.has_transformer:
                try:
                    transformed_value = self.recipe.transformer.transform(  #type:ignore
                        keypath=keypath,
                        value=value,
                        obj=item if pass_item_to_transformer else None,
                        **kwargs)
                except (ValueError, KeyError, TypeError):
                    failed_transforms[keypath].append(self.item_uuid(item))
                    continue

                if transformed_value.is_transformed and isinstance(transformed_value.value, dict):
                    value = {}
                    for t_column, t_value in transformed_value.value.items():
                        value[t_column] = t_value
                else:
                    value = transformed_value.value

            if column in dtypes:
                try:
                    table[column][index] = value
                except IndexError:
                    table[column] = np.append(table[column], np.zeros(len(table[column]), dtype=table[column].dtype))
                    table[column][index] = value
            else:
                table.setdefault(column, []).append(value)

    def item_uuid(self, item: Any) -> str:
        """
        Function to return str to identify items (Can be used for logging failures)
        """
        return repr(item)

    def _remove_collisions(self,
                           keypaths: list[tuple[tuple[str, ...], str]],
                           index: int = -2) -> list[tuple[tuple[str, ...], str]]:
        """
        Disambiguate keypaths so that there are no key collisions. If there is a collision
        the key one level up is taken and combined with apoint

        :param keypaths: Paths to investigate
        :param index: int index of the next element in the path to try

        :returns: diambigouoated paths
        """

        grouped_paths = defaultdict(list)
        for path, name in keypaths:
            grouped_paths[name].append(path)

        for name, paths in grouped_paths.items():
            if len(paths) == 1:
                continue

            if abs(index) > len(paths[0]):
                raise ValueError(f'Cannot disambiguate paths {paths}')

            #Go up levels until they can be distinguished
            unique_paths = self._remove_collisions(
                [(path[:index], f'{path[index]}{self.separator}{name}') for path in paths], index=index - 1)

            for path, unique_path in zip(paths, unique_paths):
                keypaths[keypaths.index((path, name))] = path, unique_path[1]

        return keypaths

    def tabulate(self,
                 collection: Iterable[Any],
                 table_type: type[TableType] = pd.DataFrame,
                 append: bool = True,
                 column_policy: str = 'flat',
                 pass_item_to_transformer: bool = True,
                 drop_empty_columns: bool = True,
                 **kwargs: Any) -> TableType:
        """Tabulate the common properties of a collection of objects.

        :param collection: collection of objects with same set of properties.
        :param table_type: Type of the tabulated data. Usually a pandas DataFrame or a dict.
        :param append: True: append to table if not empty. False: Overwrite table.
        :param column_policy: 'flat': Flat table, column names are last keys per keypath, name conflicts produce
                              warnings. 'flat_full_path': Flat table, column names are full keypaths,
                              'multiindex': table with MultiIndex columns (if pandas: `MultiIndex` columns), reflecting
                              the full properties' keypath hierarchies.
        :param kwargs: Additional keyword arguments for subclasses.
        :return: Tabulated objects' properties.
        """
        if table_type not in (dict, pd.DataFrame):
            raise TypeError(f'Unknown {table_type=}')

        if table_type == pd.DataFrame and (column_policy not in self._column_policies or
                                           column_policy in {'flat_full_path', 'multiindex'}):
            raise ValueError(f"Warning: Unknown pandas column policy '{column_policy}'")

        if not collection:
            raise ValueError(f'{collection=} is empty. Will do nothing.')

        # now we can finally build the table
        table: dict[str, Any] = {}

        keypaths: KeyPaths = []

        dtypes_set: frozenset[str] = frozenset()
        for index, item in enumerate(collection):

            # get inc/ex lists. assume that they are in valid keypaths format already
            # (via property setter auto-conversion)
            if not keypaths:
                if not self.recipe.include_list:
                    self.autolist(item=item, overwrite=True, pretty_print=False)
                keypaths = self.recipe.include_list.copy()
                dtypes = self.recipe.dtypes
                exclude_keypaths = self.recipe.exclude_list
                for keypath in exclude_keypaths:
                    keypaths.remove(keypath)

                #Create tuple with (path to take, name of column) to make disambiguating easier
                named_keypaths = [(path, path[-1]) for path in keypaths]

                self._remove_collisions(named_keypaths)

                for path, dtype in dtypes.items():
                    #find corresponding column name
                    column = [column for p, column in named_keypaths if p == path][0]
                    table[column] = np.zeros(self.buffer_size, dtype=dtype)
                dtypes_set = frozenset(table.keys())
                self.has_transformer = self.recipe.transformer is not None

            self.process_item(item,
                              index=index,
                              table=table,
                              keypaths=named_keypaths,
                              dtypes=dtypes_set,
                              pass_item_to_transformer=pass_item_to_transformer,
                              **kwargs)
            length = index + 1

        #Adjust to actual length
        for column in dtypes_set:
            table[column] = table[column][:length]

        if drop_empty_columns:
            empty_columns = [colname for colname, values in table.items() if all(v is None for v in values)]
            if empty_columns:
                for colname in empty_columns:
                    table.pop(colname)

        if append and self._table:
            difference = self._table.keys() ^ table.keys()
            if difference:
                raise ValueError(
                    f'Warning: Selected {append=}, but new table columns are different from columns of the '
                    f'existing table. Difference: {difference}. I will abort tabulation. Please clear the table '
                    f'first.')

        self._table = dict(table)

        if table_type == pd.DataFrame:
            return self.table  #type:ignore
        return self._table


class NamedTupleTabulator(Tabulator):
    """
    Simple Example of Tabulator for creating Dataframes from Namedtuples
    """

    def autolist(self, item: Any, overwrite: bool = False, pretty_print: bool = False, **kwargs: Any) -> None:
        """
        Just tabulate all the fields (no recursion into the objects)
        """
        self.recipe.include_list = list(item._fields)

    def get_value(self, item, keypath):
        """
        Just recursively extract all the attributes
        """
        value = item
        for key in keypath:
            value = getattr(value, key, None)
            if value is None:
                break
        return value


class NestedDictTabulator(Tabulator):
    """
    Simple Example of Tabulator for creating Dataframes from nested dicts
    """

    def autolist(self, item: Any, overwrite: bool = False, pretty_print: bool = False, **kwargs: Any) -> None:
        """
        Just tabulate all the keys with recursing into subdicts
        """

        def collect_keypaths(item):
            keypaths = []
            for key, value in item.items():
                if isinstance(value, dict):
                    subpaths = collect_keypaths(value)
                    keypaths.extend((key, *path) for path in subpaths)
                else:
                    keypaths.append((key,))
            return keypaths

        self.recipe.include_list = collect_keypaths(item)

    def get_value(self, item, keypath):
        """
        Just recursively extract all the attributes
        """
        value = item
        for key in keypath:
            value = value.get(key)
            if value is None:
                break
        return value
