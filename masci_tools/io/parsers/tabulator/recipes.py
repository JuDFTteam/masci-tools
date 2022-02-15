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
"""This subpackage contains recipes for the tabulator subpackage, which turns
properties of a collections of objects into a table.

Recipes let you reuse tabulator settings for different use cases.
"""

import abc as _abc
import typing as _typing

import masci_tools.util.python_util as _masci_python_util
from .transformers import Transformer


class Recipe(_abc.ABC):
    """Recipe for a :py:class:`~.tabulator.Tabulator`.

    Recipes hold the include, exclude list of properties which a tabulator should put into a table, by reading
    them from a set of objects, one row per object. In other words, the recipe specifies the column of the table.
    Transformations of properties for the table (say, a property is a list, and we only want the maximum), can
    be defined by specifying a transformer in the recipe.

    TODO: improve memory performance for tabulation:

    - let include exclude lists values optionally hold pandas dtype strings (numpy 'uint8' etc plus pandas types like
      'categorical'; the latter internally in tabulator replaced by numpy correspondence where needed). tabulator
      will use those when building table. otherwise, e.g. when returning pandas dataframe, all columns will
      have dtype 'object' or 'float64' and the table won't fit into memory anymore very quickly.
    """

    def __init__(self, exclude_list: dict = None, include_list: dict = None, transformer: Transformer = None, **kwargs):
        """Initialize a recipe for a :py:class:`~.tabulator.Tabulator`.

        The attributes :py:attr:`~.include_list` and :py:attr:`~.exclude_list` control which properties
        are to be tabulated (=table columns). A tabulator defines an `autolist` method which can auto-generate
        an extensive include list from a given object. This can be used to define a custom include or exclude list
        for objects of that use case.

        Subclasses define the nature of the objects to be tabulated by making assumptions on their
        property structure. That way, if both include and exclude list are empty, by default the 'complete'
        set of properties of the objects will be tabulated, where the subclass defines the notion of 'complete'.

        If neither exclude nor include list is given, the full set of properties according to implementation
        will be tabulated.

        There are three accepted formats for the include and exclude lists, here shown for an example of an
        AiiDA workchain node (for aiida-jutools `NodeTabulator`). In this example, the objects to be a tabulated
        are nodes in a database, and they have a unique identifier ('uuid'), a label, and some attributes called
        'extras' and 'outputs' with many nested properties inside them. The selection here will tell a tabulator
        to only put those properties in a table.

        .. code-block:: python

           # format 1: 'none' format: all keys are mentioned, values are None
           include_withNone = {
               'uuid': None,
               'extras':{
                   'scale_factor':None,
                   'kkr_constants_version' : {
                       'constants_version': None
                   }
               },
               "outputs": {
                   "last_calc_info": {
                       "convergence_reached": None,
                   },
                   "last_calc_output_parameters": {
                       "charge_core_states_per_atom": None,
                       "charge_core_states_per_atom_unit": None,
                       "charge_valence_states_per_atom": None,
                       "charge_valence_states_per_atom_unit": None,
                   }
               }
           }

           # format 2: 'list' format: if all subkeys remain on the same level, can
           # use shorthand notation and write them as a list instead of
           # {key:None, key:None, ...}
           include_withList = {
               'uuid': None,
               'extras':{
                   'scale_factor': None,
                   'kkr_constants_version' : ['constants_version']
               },
               "outputs": {
                   "last_calc_info": ["convergence_reached"],
                   "last_calc_output_parameters": [
                       "charge_core_states_per_atom",
                       "charge_core_states_per_atom_unit",
                       "charge_valence_states_per_atom",
                       "charge_valence_states_per_atom_unit"
                   ]
               }

           }

           # format 3: keypaths. this is the internal format the recipe uses.
           include_keypaths = [
               ['uuid'],
               ['extras', 'scale_factor'],
               ['extras', 'kkr_constants_version', 'constants_version'],
               ['outputs', 'last_calc_info', 'convergence_reached'],
               ['outputs', 'last_calc_output_parameters', 'charge_core_states_per_atom'],
               ['outputs', 'last_calc_output_parameters', 'charge_core_states_per_atom_unit'],
               ['outputs', 'last_calc_output_parameters', 'charge_valence_states_per_atom'],
               ['outputs', 'last_calc_output_parameters', 'charge_valence_states_per_atom_unit']
           ]

        :param exclude_list: Optional list of properties to exclude. May be set later.
        :param include_list: Optional list of properties to include. May be set later.
        :param transform: Specifies special transformations for certain properties for tabulation.
        :param kwargs: Additional keyword arguments for subclasses.
        """
        # note: for the in/ex lists, using the public setter here,
        # to trigger conversion
        self._exclude_list = exclude_list if exclude_list else {}
        self._include_list = include_list if include_list else {}
        self.transformer = transformer

    @property
    def exclude_list(self) -> dict:
        return self._exclude_list

    @exclude_list.setter
    def exclude_list(self, exclude_list: _typing.Union[dict, list]):
        self._exclude_list = exclude_list
        if isinstance(exclude_list, dict):
            self._to_keypaths()

    @property
    def include_list(self) -> dict:
        return self._include_list

    @include_list.setter
    def include_list(self, include_list: _typing.Union[dict, list]):
        self._include_list = include_list
        if isinstance(include_list, dict):
            self._to_keypaths()

    def _to_keypaths(self):
        """Generate paths from a possibly nested dictionary.

        This method can be used for handling include lists, exclude lists, and when writing
        new :py:class:`~Transformer` transform methods.

        List of paths to each value within the dict as tuples (path, value).

        convert from with-List to with-None format for convert to keypaths

        convert to keypaths (upper: done inside this one anyway)
        """

        def _to_keypaths_recursive(sub_dict: dict, path: list):
            paths = []
            for k, v in sub_dict.items():
                if isinstance(v, dict):
                    paths += _to_keypaths_recursive(v, path + [k])
                paths.append((path + [k], v))
            return paths

        for in_or_ex, a_dict in {'in': self._include_list, 'out': self._exclude_list}.items():

            # precondition: not already keypaths format
            is_list = isinstance(a_dict, list)
            is_all_lists = is_list and all(isinstance(path, list) for path in a_dict)
            if is_all_lists:
                continue

            # if empty, convert to empty list. if not empty, convert to keypaths
            if not a_dict:
                keypaths = []
            else:
                # convert from include list with-list format with-none format:
                # same-level subkeys mentioned as list [k1,k2] -> dict {k1:None, k2:None}.
                _a_dict = _masci_python_util.modify_dict(a_dict=a_dict,
                                                         transform_value=lambda v: {k: None for k in v}
                                                         if isinstance(v, list) else v,
                                                         to_level=99)

                keypaths = _to_keypaths_recursive(sub_dict=_a_dict, path=[])
                # the result consists of sets of subpaths. For each subset, there is
                # an additianal entry where the value contains the whole subdict from
                # which the paths were generated. We are not interested in those duplicate
                # entries, so remove them.
                keypaths = [tup for tup in keypaths if not isinstance(tup[1], dict)]

                # now list should be like [(path1, None), (path2, None), ...],
                # or at least of type _typing.List[_typing.Tuple[list, _typing.Any]].
                # check that. if not, something is wrong.
                # otherwise, just return the paths.
                if all(tup[1] is None for tup in keypaths):
                    keypaths = [tup[0] for tup in keypaths]

            # postcondition: keypaths format
            is_list = isinstance(keypaths, list)
            is_all_lists = is_list and all(isinstance(path, list) for path in keypaths)
            if not is_all_lists:
                raise TypeError(f'Could not generate keypaths of required type {_typing.List[list]} '
                                f'from {in_or_ex}clude list. Either specified list in wrong format '
                                f'(see class init docstring for examples), or list generated from '
                                f'autolist stumbled over untreated special case for some unpacked '
                                f'property.')

            if in_or_ex == 'in':
                self._include_list = keypaths
            elif in_or_ex == 'out':
                self._exclude_list = keypaths
