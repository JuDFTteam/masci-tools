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
from typing import Any, Iterable, TypeVar

import pandas as pd

from .recipes import Recipe, KeyPaths

__all__ = ('Tabulator', 'NamedTupleTabulator', 'TableType')

TableType = TypeVar('TableType', type[dict], type[pd.DataFrame])


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

    def __init__(self, recipe: Recipe | None = None) -> None:
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
        self._table: dict[str, Any] = {}

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
    def get_keypath(self, item: Any, keypath: Iterable[str]) -> Any:
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

    def process_item(self, item: Any, table: dict[str, Any], keypaths: list[tuple[tuple[str, ...], str]],
                     pass_item_to_transformer: bool, **kwargs: Any) -> None:
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

        row: dict[str, Any] = {}

        for keypath, column in keypaths:
            row[column] = None

            value = self.get_keypath(item, keypath)
            if value is None:
                failed_paths[keypath].append(self.item_uuid(item))
                continue

            if not self.recipe.transformer:
                row[column] = value
            else:
                try:
                    transformed_value = self.recipe.transformer.transform(
                        keypath=keypath, value=value, obj=item if pass_item_to_transformer else None, **kwargs)
                except (ValueError, KeyError, TypeError):
                    failed_transforms[keypath].append(self.item_uuid(item))
                    continue

                if transformed_value.is_transformed and isinstance(transformed_value.value, dict):
                    for t_column, t_value in transformed_value.value.items():
                        row[t_column] = t_value
                else:
                    row[column] = transformed_value.value

        for column, value in row.items():
            table[column].append(value)

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
            unique_paths = self._remove_collisions([(path[:index], f'{path[index]}.{name}') for path in paths],
                                                   index=index - 1)

            for path, unique_path in zip(paths, unique_paths):
                keypaths[keypaths.index((path, name))] = path, unique_path[1]

        return keypaths

    def tabulate(self,
                 collection: Iterable[Any],
                 table_type: TableType = pd.DataFrame,
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
        table: dict[str, Any] = defaultdict(list)

        keypaths: KeyPaths = []

        for item in collection:

            # get inc/ex lists. assume that they are in valid keypaths format already
            # (via property setter auto-conversion)
            if not keypaths:
                if not self.recipe.include_list:
                    self.autolist(item=item, overwrite=True, pretty_print=False)
                keypaths = self.recipe.include_list.copy()
                exclude_keypaths = self.recipe.exclude_list
                for keypath in exclude_keypaths:
                    keypaths.remove(keypath)

                #Create tuple with (path to take, name of column) to make disambiguating easier
                named_keypaths = [(path, path[-1]) for path in keypaths]

                self._remove_collisions(named_keypaths)

            self.process_item(item,
                              table=table,
                              keypaths=named_keypaths,
                              pass_item_to_transformer=pass_item_to_transformer,
                              **kwargs)

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

    def get_keypath(self, item, keypath):
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

    def get_keypath(self, item, keypath):
        """
        Just recursively extract all the attributes
        """
        value = item
        for key in keypath:
            value = value.get(key)
            if value is None:
                break
        return value
