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

import abc as _abc
import typing as _typing

import pandas as _pd

from .recipes import Recipe


class Tabulator(_abc.ABC):
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
      values). See pandas > Scaling to larg datasets for more.
    - maybe add save option (or method) and read() method to read in tabulated table. for pandas, that allow a user
      to easily reuse the dtypes information from the recipe.
    """

    def __init__(self, recipe: Recipe = None, **kwargs):
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
        self._table_types = []
        self._table = None

    @_abc.abstractmethod
    def autolist(self, obj: _typing.Any, overwrite: bool = False, pretty_print: bool = False, **kwargs):
        """Auto-generate an include list of properties to be tabulated from a given object.

        This can serve as an overview for customized include and exclude lists.
        :param obj: An example object of a type compatible with the tabulator.
        :param overwrite: True: replace recipe list with the auto-generated list. False: Only if recipe list empty.
        :param pretty_print: True: Print the generated list in pretty format.
        :param kwargs: Additional keyword arguments for subclasses.
        """
        pass

    def clear(self):
        """Clear table if already tabulated."""
        self._table = None

    @property
    def table(self) -> _typing.Any:
        """The result table. None if :py:meth:`~tabulate` not yet called."""
        return self._table

    @_abc.abstractmethod
    def tabulate(self,
                 collection: _typing.Any,
                 table_type: _typing.Type = _pd.DataFrame,
                 append: bool = True,
                 column_policy: str = 'flat',
                 **kwargs) -> _typing.Optional[_typing.Any]:
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
        pass
