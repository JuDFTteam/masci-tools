# pylint: disable=protected-access
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
"""This module contains a simple class for set-like chemical elements enumeration."""
from __future__ import annotations as _annotations

import copy as _copy
import dataclasses as _dc
import json as _json
import numbers as _numbers
import os as _os
import typing as _typing
from pathlib import Path as _Path

import bokeh as _bokeh
import deepdiff as _deepdiff
import matplotlib as _mpl
import matplotlib.pyplot as plt
import mendeleev as _mendeleev
import numpy as _np
import seaborn as _sns

import masci_tools.util.python_util as _masci_python_util
import masci_tools.vis.plot_methods as _masci_plot_methods

T_FLAT_ELEMENTS_CONTAINER = _typing.Union[_typing.List[str], _typing.List[int], _typing.Dict[str, int],
                                          _typing.Set[str], _typing.Set[int], _typing.Tuple[str], _typing.Tuple[int]]

T_NESTED_ELEMENTS_CONTAINER = _typing.Union[_typing.Dict[str, _typing.List[str]], _typing.Dict[str, _typing.List[int]]]

T_ELEMENTS_CONTAINER = _typing.Union[T_FLAT_ELEMENTS_CONTAINER, T_NESTED_ELEMENTS_CONTAINER]


@_dc.dataclass(init=True, repr=True, eq=True, order=False, frozen=False)
class ChemicalElementsPlottingProfile:
    """"For reusing plotting settings over several plots. Serializable.

    Instances of this class can be used as input to the
    :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.plot`
    method, to simplify reusing non-changing argumments over a series of periodic table plots. The profile can be saved
    to and loaded from a JSON file for reuse as well.

    :param profile_name: name of the profile
    :param values_range: list of sortable, unique values. Must contain at least all plotted attribute values.
    :param missing_value: Value to set for missing elements.
    :param missing_name: Name to set for missing elements in legend.
    :param title_prefix: If set, will be preprended to plot title.
    :param output_prefix: If set, will be prepended to plot output filepath.
    :param legend_title_prefix: If set, will be prepended to legend title.
    :param colorby: 'group': Colormap by selected groups, 'attribute': by mendeleev periodic table attribute.
    :param attribute: Attribute's value displayed below elements. Either PTE attribute, or group values.
    :param without_attribute: Do not display the attribute values below the elements.
    :param colormap_name: Name of seaborn or matplotlib colormap.
    :param missing_color: Hex code of the color to be used for the missing values (#ffffff white, #bfbfbf light gray).
    :param missing_group_value: If colorby 'group' and instance is flat, this correct missing colorisation.
    :param colormap: Dictionary {value : hexcolor string}. If not specified, created from value_range and map name.
    :param size: Tuple (width, height) of the table figure in pixels.
    :param showfblock: Show the elements from the f block
    :param long_version: Show the long version of the periodic table with the f block between the s and d blocks.
    :param with_legend: True: return extra matplotlib figure = legend. plot(...) will render it below the table.
    """
    profile_name: str = ''
    values_range: list = _masci_python_util.dataclass_default_field([])
    missing_value: object = None
    missing_name: str = 'Missing'
    title_prefix: str = None
    output_prefix: str = None
    legend_title_prefix: str = None
    colorby: str = 'group'
    attribute: str = 'atomic_weight'
    without_attribute: bool = False
    colormap_name: str = 'PiYG'
    missing_color: str = '#404040'  # dark gray
    missing_group_value: object = 1
    colormap: dict = _masci_python_util.dataclass_default_field({})
    size: tuple = _masci_python_util.dataclass_default_field(())
    showfblock: bool = True
    long_version: bool = False
    with_legend: bool = False
    _version: int = 1
    _cls_name: str = ''

    def __post_init__(self):
        """Create colormap from values_range, if the former was not specified."""
        # save class name
        cls = type(self)
        self._cls_name = cls.__module__ + '.' + cls.__name__

        # create colormap
        if not self.colormap and self.values_range:
            self.colormap = {
                key: _mpl.colors.rgb2hex(rgb) for key, rgb in zip(
                    self.values_range, _sns.color_palette(palette=self.colormap_name, n_colors=len(self.values_range)))
            }

    def save(self, filepath):
        raise NotImplementedError()


class ChemicalElements:
    """A container for safe chemical element enumeration."""

    def __init__(self,
                 elements: T_ELEMENTS_CONTAINER = None,
                 empty: bool = False,
                 groups: _typing.List[str] = None,
                 distinct: bool = False,
                 special_elements: _typing.Dict[str, int] = None,
                 filepath: _typing.Union[str, _Path] = None):
        """A container for safe chemical element enumeration.

        Attribute 'elmts' stores either (flat) a dict key = chemical sumbol str : value = atomic number int.
        Or altternatively (nested), a dict of named group of such dicts (e.g. chemical property groups).
        The element dicts are always sorted by atomic number.
        If no or empty elements list/dict is supplied at initialization, will populate elmts with
        dict of entire periodic table.
        Class checks validity and prevents duplicate entries (within one group, not across groups).
        Class provides convenience methods: add/remove, set operations including overloaded operators
        '+' (union) and '-' (left difference), plot periodic table,
        container access methods: 'in' operator, []-operator for element (if flat) or group (if nested) access,
        relational operators (<, <=, ...).

        Additionally, 'data' and 'set_data()' arbitrary object storage for each group of chemical elements.

        DEVNOTES:
        - take care to choose correct 'elmts' access: elmts for interface, __elmts for internal.
        - take care to carry over self.distinct property to new CE objects

        :param elements: collection of element symbols or atomic numbers.
        :type elements: one of dict, list, tuple, set.
        :param empty: True: initialize without any elements.
        :param groups: If not None and more than one, ignore other arguments and initialize with empty groups.
        :param distinct: True: disallow same element in different groups.
        :param special_elements: dict symbol:atomic_number of special elements (eg {'X':0} for vacuum)
        :param filepath: if not None, init from JSON file. Must have been written with ChemicalElements.to_file().

        >>> from masci_tools.util.chemical_elements import ChemicalElements
        >>> a = ChemicalElements([11, 2, 118, 78])
        >>> b = ChemicalElements(['Na', 'He', 'Og', 'Pt'])
        >>> c = ChemicalElements({'Na' : 11, 'He' : 2, 'Og' : 118, 'Pt' : 78})
        >>> d = ChemicalElements({'a' : ['Na', 'He'], 'b' : ['Og']})
        >>> d.add_elements(['Pt'], 'b')
        >>> e = ChemicalElements()
        >>> e.remove_elements([11, 2, 118, 78])
        >>> assert a.elmts == {'He': 2, 'Na': 11, 'Pt': 78, 'Og': 118}
        >>> assert a == b
        >>> assert a + b == c
        >>> assert a.intersection(b) == c
        >>> assert a.union(b) == ChemicalElements(d.flatten())
        >>> assert e.complement() == c
        """
        # Define all attributes.
        # Also see public properties defined below.
        self.distinct = None
        self._pte = None
        self._special_elements = None
        self._special_elements_inv = None
        self.__elmts = None
        self.__data = None
        self.plotting_profile = None

        self.T_INTERNAL_FLAT_ELEMENTS_CONTAINER = _typing.Dict[str, int]
        self.T_INTERNAL_NESTED_ELEMENTS_CONTAINER = _typing.Dict[str, _typing.Dict[str, int]]
        self.T_INTERNAL_ELEMENTS_CONTAINER = _typing.Union[self.T_INTERNAL_FLAT_ELEMENTS_CONTAINER,
                                                           self.T_INTERNAL_NESTED_ELEMENTS_CONTAINER]

        # Now initialize them.

        # property: distinctness
        self.distinct = distinct

        # periodic table, all elements; special element definitions not in actual periodic table
        # devnote: mendeleev.elements.get_all_elements() is very expensive (0.2s). hardcoded pte is faster.
        # self._pte = {el.symbol: el.atomic_number for el in mendeleev.elements.get_all_elements()}
        # yapf: disable
        self._pte = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11,
                     'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21,
                     'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31,
                     'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41,
                     'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50, 'Sb': 51,
                     'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60, 'Pm': 61,
                     'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71,
                     'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80, 'Tl': 81,
                     'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90, 'Pa': 91,
                     'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100,
                     'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109,
                     'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118}
        # yapf: enable
        self._pte_inv = {v: k for k, v in self._pte.items()}

        self._special_elements = {}
        self._special_elements_inv = {}
        if special_elements:
            # assume correct format
            for symbol, number in special_elements.items():
                self.expand_allowed_elements(symbol=symbol, atomic_number=number)

                # if from file,
        if filepath:
            with open(filepath, encoding='utf-8') as file:
                self.__elmts = _json.load(file)
                # in case any group keys were numeric, they will now be string. rectify that.
                # in case user WANTS them to be string, can always use 'rename' method to turn them back.
                group_keys = list(self.__elmts.keys())
                for key in group_keys:
                    if _masci_python_util.is_number(key):
                        group_elmts = self.__elmts.pop(key)
                        self.__elmts[_masci_python_util.to_number(key)] = group_elmts

            # init data as empty since to_file() doesn't save data.
            self.__data = {group_name: None for group_name in self.__elmts.keys()}
        elif groups:
            # init elmts, convert to [optional: container of:] dict[s] sym:num.
            if not isinstance(groups, list) \
                    or not all(isinstance(group_name, str) for group_name in groups):
                raise ValueError('If groups not None, must be a list of strings.')
            if len(groups) < 2:
                raise ValueError('If groups not None, must be more than one group. '
                                 "Else init with 'empty' or 'elements' instead.")

            self.__elmts = {group_name: {} for group_name in groups}
            self.__data = {group_name: None for group_name in groups}
        else:
            self.__elmts = {}
            if not empty:
                list_types = (list, tuple, set)
                if not elements:
                    # fill with whole periodic table
                    self.__elmts = {'': _copy.deepcopy(self._pte)}

                elif isinstance(elements, list_types):
                    # not nested
                    self.__elmts = {'': self._chemical_element_list_to_dict(elements)}
                elif isinstance(elements, dict):
                    if not all(isinstance(v, list_types) for (k, v) in elements.items()):
                        # flact dict
                        elements, _ = self._validate(elements)
                        # lazy type checking for sym:num
                        key_type_is_int = isinstance(list(elements.keys())[0], int)
                        elmts = {v: k for k, v in elements.items()} if key_type_is_int else elements
                        assert all(isinstance(k, str) for k in elmts.keys())
                        assert all(isinstance(v, int) for v in elmts.values())
                        self.__elmts = {'': self._sort(elements)}
                    else:
                        # nested dict
                        new__elmts = {k: self._chemical_element_list_to_dict(v) for k, v in elements.items()}
                        if not self.__validate_distinctness(new__elmts):
                            print('Warning: Chose distinctness, but supplied non-distinct groups. Not stored.')
                            self.__elmts = {'': {}}
                else:
                    # try converting unknown types of 'elements' into a list
                    try:
                        self.__elmts = {'': self._chemical_element_list_to_dict(list(elements))}
                    except TypeError as err:
                        raise TypeError(
                            f'Argument is a {type(elements)}, but must be a list, dict, tuple or set.') from err

            # init data: an object store associated with each elmt group
            group_names = self.groups()
            if not group_names:
                self.__data = {'': None}
            else:
                self.__data = {group_name: None for group_name in group_names}

    def is_flat(self) -> bool:
        """True if 'elmts' attribute is flat dict of chemical elements, False if a dict of groups of such ('nested').
        """
        # DEVnote: CE considers elmts with one group as flat dict, and with more than one as nested. CE's interface
        # changes accordingly. kyes() on a flat dict will return element names, and group names on a nested dict.
        # That is, CE 'hides' the group structure if there is only a single group. CE does not care about the name
        # of the single group. The initial name for the group of a flat CE is the empty string. It can be renamed,
        # and the instance will remain flat.
        return (not list(self.__elmts.keys())) or (list(self.__elmts.keys()) == ['']) or (len(self.__elmts.keys()) == 1)

    @property
    def elmts(self) -> _typing.Dict[str, int]:
        """If flat, returns list of chemical elements, else groups of such.

        Note that read-only, returns deepcopy.
        """
        if not self.is_flat():
            return _copy.deepcopy(self.__elmts)
        key = list(self.__elmts.keys())[0]
        return _copy.deepcopy(self.__elmts[key])

    @property
    def data(self) -> _typing.Any:
        """Returns full 'data' object storage with all groups.

        Note that if nested, is read-only, returns deepcopy.
        """
        if self.is_flat():
            return self.data
            # key = list(self.__elmts.keys())[0]
            # return self.__data[key]
            # return copy.deepcopy(self.__data[key])

        # return self.__data
        return _copy.deepcopy(self.__data)

    def get_data(self, group_name: str) -> _typing.Any:
        """Returns 'data' object storage for given group.
        """
        if self.is_flat():
            return self.data

        return self.__data[group_name]

    def set_data(self, group_name: str, an_object: _typing.Any) -> _typing.Optional[_typing.Any]:
        """Set a data item in the 'data' object storage.

        :return: previously stored data item if present
        """
        if self.is_flat():
            key = list(self.__elmts.keys())[0]
        elif group_name not in self.groups():
            raise KeyError('Supplied group name does not exist.')
        else:
            key = group_name
        dump = self.__data.pop(key, None)
        self.__data[key] = an_object
        return dump

    def pop_data(self, group_name: str) -> _typing.Optional[_typing.Any]:
        return self.set_data(group_name, None)

    def __eq__(self, other: ChemicalElements) -> bool:
        """Overload '==' operator and '!=' operator. Check for equality.

        Note: this DOES take grouping into account.
        """
        if isinstance(other, ChemicalElements):
            return self.__elmts == other.__elmts
        return False

    def __le__(self, other: ChemicalElements) -> bool:
        """Overload '<=' operator. Is this subset of other.

        True if this flattened is a subset of the other (ie, ignoring grouping).

        :param other: possible superset
        :type other: ChemicalElements
        """
        assert isinstance(other, ChemicalElements)
        return (other + self).flatten(as_dict=False) == other.flatten(as_dict=False)

    def __lt__(self, other: ChemicalElements) -> bool:
        """Overload '<' operator. Is this true subset of other.

        True if this flattened is a subset of the other (ie, ignoring grouping).

        :param other: possible superset
        :type other: ChemicalElements
        """
        return (self <= other) and (self.count() < other.count())

    def __ge__(self, other: ChemicalElements) -> bool:
        """Overload '>=' operator. Is other subset of this.

        True if other flattened is a subset of this (ie, ignoring grouping).

        :param other: possible subset
        :type other: ChemicalElements
        """
        assert isinstance(other, ChemicalElements)
        return (self + other).flatten(as_dict=False) == self.flatten(as_dict=False)

    def __gt__(self, other: ChemicalElements) -> bool:
        """Overload '>' operator. Is other true subset of this.

        True if other flattened is a true subset of this (ie, ignoring grouping).

        :param other: possible subset
        :type other: ChemicalElements
        """
        assert isinstance(other, ChemicalElements)
        return (self >= other) and (self.count() > other.count())

    def __getitem__(self, group_name_or_symbol: str) -> _typing.Union[str, int, _typing.Dict[str, int]]:
        """Overload '[]' operator, getter.

        If flat, returns symbol's atomic number, if nested, returns group of elements.
        If flat, also allows inverted input: atomic_number, return symbol.
        """
        if not self.is_flat():
            # accept any type as group symbol type
            return self.elmts[group_name_or_symbol]

        if isinstance(group_name_or_symbol, int):
            return self.invert()[group_name_or_symbol]
        if isinstance(group_name_or_symbol, str):
            return self.elmts[group_name_or_symbol]

        raise KeyError(f"Unsupported key/value type '{type(group_name_or_symbol)}'.")

    def __validate_distinctness(self, new__elmts: _typing.Dict[str, int]) -> bool:
        """Checks if new internal ``__elmts`` would violate distinctniss if dictinct=True.

        If no violation (or distinct=False and not nested) , internal ``__elmts`` will be replaced with new one. If
        (distinct=True and nested) and violation, do not replace.

        :param new__elmts: new internal elements dict to replace current one.
        :return: True if no violation, False if distinctness violation.
        """
        if not self.is_flat() and self.distinct:
            # distinctness check of new internal elements dict: assert that sum over element count in all groups
            # equals distinct sum over element count in all groups
            elmt_count = sum(len(group.keys()) for group_name, group in new__elmts.items())
            distinct_count = len(set().union(*[set(group.keys()) for group_name, group in new__elmts.items()]))
            if elmt_count != distinct_count:
                return False
        self.__elmts = _copy.deepcopy(new__elmts)
        return True

    def __setitem__(self, group_name: str, elements):
        """Overload '[]' operator, setter. Sets group of list of chemical elements.

        Note: this overrides the current elmts in that group, or all if elmts is flat.
        For adding elements, use add_elements().

        :param group_name: a name for this list of elements
        :param elements: examples ['He', 'Na']; [2, 11]; {'bla':['Ca'], 'ble;"['Cu, 'Au'].
        :type elements: dict, list, tuple or set
        """
        self.__elmts[group_name] = self._chemical_element_list_to_dict(elements)
        self.__data[group_name] = None

    def items(self):
        """Overload iteration key-value. Note that iterates over groups if not flat."""
        for group_or_symbol in self.elmts:
            yield (group_or_symbol, self.elmts[group_or_symbol])

    def __iter__(self):
        """Overload iteration key. Note that iterates over groups if not flat."""
        return iter(self.elmts)

    def __contains__(self, item):
        """'Overload 'in' operator. Calls count()."""
        _item = item
        if isinstance(_item, (str, int)):
            return self.count(_item)
        if isinstance(item, (list, dict)):
            _item = ChemicalElements(elements=_item)
        if isinstance(_item, ChemicalElements):
            return _item <= self
        return False

    def __add__(self, other):
        """Overload '+' operator. Addition = set union of two possibly nested dicts."""
        assert isinstance(other, ChemicalElements)
        distinct = self.distinct and other.distinct
        union = ChemicalElements(None, empty=True, distinct=distinct)
        for group_name, group in self.__elmts.items():
            union.add_elements(group, group_name)
        for group_name, group in other.__elmts.items():
            union.add_elements(group, group_name)
        return union

    def __sub__(self, other):
        """Overload '-' operator. Subtraction = set left-difference of possibly nested dicts."""
        assert isinstance(other, ChemicalElements)
        distinct = self.distinct and other.distinct
        difference = ChemicalElements(None, empty=True, distinct=distinct)
        for group_name, group in self.__elmts.items():
            difference.add_elements(group, group_name)
        for group_name, group in other.__elmts.items():
            difference.remove_elements(group, group_name)
        return difference

    def keys(self):
        """If flat, returns symbols, if nested, returns group names, like groups().
        """
        return self.elmts.keys()

    def hidden_key(self):
        """If flat, returns name of the hidden group. If nested, returns None.

        Background: see :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.hidden_group`.
        """
        return self.hidden_group()

    def values(self):
        """If flat, returns atomic numbers, if nested, returns elements of group.
        """
        return self.elmts.values()

    def clear(self, selected_groups: list = None, delete_empty_groups: bool = True):
        """Clear selected groups, optionally delete empty groups.

        Note that objects stored in 'data' get lost.

        :param selected_groups: if None, clear all groups.
        :type selected_groups: list of strings
        :param delete_empty_groups: remove group_name key from elmts if group empty
        """
        if self.is_flat():
            self.__elmts = {'': {}}
            self.__data = {'': {}}
        elif delete_empty_groups:
            for group_name in selected_groups:
                self.__elmts.pop(group_name, None)
                self.__data.pop(group_name, None)
            if not self.__elmts.keys():
                self.__elmts = {'': {}}
                self.__data = {'': {}}
        else:
            for group_name in selected_groups:
                if group_name in self.__elmts:
                    self.__elmts[group_name] = {}
                    self.__data[group_name] = None

    def flatten(self, selected_groups: list = None, in_place: bool = False, as_dict=True):
        """Return flattened dict of group selection, or replace elmts with it in-place.

        Note: if in_place, all objects stored in 'data' will be lost.

        :param selected_groups: If nested and not specified, include all groups.
        :type selected_groups: list of strings
        :param in_place: True: replace elmts with flattened dict.
        :param as_dict: True: return as dict, False: as ChemicalElements
        :return: if not in-place, return flattened dict, else None.
        :rtype: None, dict, or ChemicalElements
        """
        if self.is_flat():
            if not in_place:
                if as_dict:
                    return _copy.deepcopy(self.elmts)
                return ChemicalElements(self.elmts)
            return None

        data_selection = self.select_groups(selected_groups)
        flattened = {}
        for group_name, group in data_selection.items():
            for sym, num in group.items():
                flattened[sym] = num
        if in_place:
            self.__elmts = {'': flattened}
            self.__data = {'': None}
            return None
        if as_dict:
            return flattened

        return ChemicalElements(flattened)

    def count_groups(self, selected_groups: list = None):
        """If flat, return element count. If nested, return dict with element count per group.

        :param selected_groups: only is nested: only count specified groups.
        :type selected_groups: list of strings
        """
        if self.is_flat():
            return len(self.elmts.keys())

        return {k: len(v.keys()) for k, v in self.select_groups(selected_groups).items()}

    def count(self, item=None, group_name: str = None) -> int:
        """Count occurrences of symbol or atomic_number in elmts.

        If nothing specified, count all distinct elements in elmts (sum over all groups).
        If only group_name specified, count all elements in group.
        If only item specified, count element occurrences across all groups.
        If both specified, count item in this group (1 or 0).

        :param item: symbol (case sensitive) or atomic_number
        :type item: str or int
        :param group_name: Optional if elmts is flat, obligatory if nested.
        :type group_name: str
        :return: if not return_dict: 0 if absent, >0 if present
        """
        if item is None:
            if group_name in self.__elmts:
                return len(self.__elmts[group_name].keys())
            if group_name is None:
                return len(self.flatten().keys())
            # else # group_name but not in self.__elmts
            raise KeyError(f"Group '{group_name}' is not in elmts.")

        def contains_item(a_dict):
            if isinstance(item, str):
                return int(item in a_dict)
            if isinstance(item, int):
                return int(item in a_dict.values())
            return int(False)

        if self.is_flat():
            return contains_item(self.elmts)
        if group_name is None:  # and nested
            # check all groups
            count = 0
            for group in self.elmts.values():
                count += contains_item(group)
            return count
        # else: # nested and group_name
        return contains_item(self.elmts[group_name])

    def groups(self):
        """Returns list of group names. If elmts is flat (only one group), will return empty list.
        """
        if self.is_flat():
            return []

        return list(self.elmts.keys())

    def hidden_group(self):
        """If flat, returns name of the hidden group. If nested, returns None.

        Background: If elmts is flat (no groups, i.e. no nested elements), all elements
        are held in a single group (key by default the empty string). This single group is hidden, such
        that for flat elmts, keys() and groups() returns the list of elements instead. As
        soon as there are two groups or more, the group names are returned instead. Still,
        the hidden group key can be renamed, and this has consequences down the line when
        adding or removing elements, or doing set operation with other ``ChemicalElements``
        instances. So this method shows the name of the hidden group if flat.
        """
        if self.is_flat():
            return list(self.__elmts.keys())[0]

        return None

    def adjust_flat_elements(self, other_elements: _typing.List[ChemicalElements], group_name: str = ''):
        """For flat instances of ``ChemicalElements`` with different names, make all names equal.

        Background: Flat elements have hidden group names, if renamed from default hidden group name, the empty
        string (see :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.hidden_group`). If set operations
        are applied to them, they behave as if not flat (nested). This function makes all involved hidden group names
        equal, so that they truly behave as flat instances under set operations.

        :param other_elements: other flat ``ChemicalElement`` instances.
        :param group_name: Hidden group name to apply to all. Default hidden group name is empty string.
        """
        msg_prefix = f'Warning: {self.__class__.__name__}.adjust_flat_elements():'
        if not self.is_flat():
            print(f'{msg_prefix} Main instance is not flat (nested). I will ignore it.')
            group_name = '' if group_name is None else group_name
        else:
            group_name = self.hidden_group() if group_name is None else group_name

        others_flat = [ce for ce in other_elements if ce.is_flat()]
        if len(others_flat) < len(other_elements):
            num_not_flat = len([ce for ce in other_elements if not ce.is_flat()])
            print(f'{msg_prefix} {num_not_flat} instances are not flat (nested). I will ignore them.')

        for ce in others_flat:
            ce.rename_group(ce.hidden_group(), group_name)

    def select_groups(self,
                      selected_groups: list = None,
                      include_special_elements: bool = True,
                      as_dict=True) -> _typing.Union[dict, ChemicalElements]:
        """Return only selected groups from elmts. Always returns a copy.

        :param selected_groups: If flat and not specified, return the empty name group of flat elmts.
        :type selected_groups: list of strings
        :param include_special_elements: False: remove special elements if any defined. This returns a copy always.
        :param as_dict: True: return as dict, False: as ChemicalElements
        :return: subset of elmts
        :rtype: dict
        """
        elements = _copy.deepcopy(self.__elmts)

        if not include_special_elements:
            for group_name, group in elements.items():
                for special_symbol in self._special_elements:
                    elements[group_name].pop(special_symbol, None)

        if not selected_groups or (set(self.groups()) == set(selected_groups)):
            # always return non-flat view, ie if flat, dict with one group
            if as_dict:
                return elements
            return self

        a_dict = {
            data_group: elmts for data_group, elmts in elements.items()
            for selection_group in selected_groups
            if data_group == selection_group
        }
        if as_dict:
            return a_dict
        elmts = ChemicalElements(empty=True)
        for group_name, group in a_dict.items():
            elmts.add_elements(elements=group, group_name=group_name)
        return elmts

    def rename_group(self, old_group_name, new_group_name):
        """Rename a group.

        Note: If the instance is flat (not nested = no groups), then renaming the hidden group might have
        unintended consequences in set operations. See
        Background: see :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.hidden_group`.
        """
        group = self.__elmts.pop(old_group_name)
        self.add_elements(group, new_group_name)

        data = self.__data.pop(old_group_name)
        self.__data[new_group_name] = data

    def group_difference(self, group_name1: str, group_name2: str) -> ChemicalElements:
        """Return difference between two groups.

        If one is the true superset, the set left difference is returned (what is in the one that is not in the other).

        If not, the symmetrical difference is returned.
        """
        if self.is_flat():
            raise KeyError('Elmts is flat, no groups to compare.')
        if group_name1 not in self.groups() or group_name2 not in self.groups():
            raise KeyError(f"Elmts has no groups '{group_name1}', '{group_name2}'.")
        distinct = self.distinct
        elmts_group1 = ChemicalElements(self[group_name1], distinct=distinct)
        elmts_group2 = ChemicalElements(self[group_name2], distinct=distinct)
        if elmts_group1 == elmts_group2:
            print(f"'{group_name1}' equal to '{group_name2}'")
            return ChemicalElements(empty=True, distinct=distinct)
        if elmts_group1 > elmts_group2:
            print(f"'{group_name1}' true superset of '{group_name2}'")
            return elmts_group1 - elmts_group2
        if elmts_group1 < elmts_group2:
            print(f"'{group_name1}' true subset of '{group_name2}'")
            return elmts_group2 - elmts_group1

        print(f"'{group_name1}', '{group_name2}' not subsets of each other, return symmetrical difference")
        return elmts_group1.symmetrical_difference(elmts_group2)

    def compare_groups(self, group_name1, group_name2):
        if self.is_flat():
            raise KeyError('Elmts is flat, no groups to compare.')
        if group_name1 not in self.groups() or group_name2 not in self.groups():
            raise KeyError(f"Elmts has no groups '{group_name1}', '{group_name2}'.")
        return _deepdiff.DeepDiff(self[group_name1],
                                  self[group_name2],
                                  ignore_order=True,
                                  ignore_numeric_type_changes=True)

    def invert(self, group_name: str = None):
        """If flat, return inverted element dict symbol : atomic number to num:sym, or group elmt dict if nested.

        :return: inverted chemical elements dict
        :rtype: dict
        """
        if self.is_flat():
            elmts = self.elmts if self.is_flat() else self.__elmts[group_name]
        elif group_name:
            elmts = self.__elmts[group_name]
        else:
            raise KeyError('Is nested, but did not supply group name.')
        return {v: k for k, v in elmts.items()}

    def get_groups_for(self, symbol: str) -> _typing.Union[_typing.List[str], None]:
        """Find the group names for the groups the chemical element is contained in.
        :param symbol: chemical element symbol
        :return: list of group_names or None if no find or if flat
        """
        if self.is_flat():
            return []
        group_names = [group_name for group_name in self.elmts if symbol in self.elmts[group_name]]
        if group_names:
            return group_names

        return []

    def add_elements(self, elements, group_name: str = ''):
        """Add elements. Elmts get resorted afterwards.

        :param elements: list of symbols str or atomic numbers int
        :type elements: list or dict
        :param group_name: if this nested, add to this' group. ignored if this flat.
        :type group_name: str
        """
        if isinstance(elements, dict):
            # just assume it's a element sym:num dict
            elements, _ = self._validate(elements)
            elmts = elements
        else:
            elmts = self._chemical_element_list_to_dict(elements, sort=False)

        new__elmts = _copy.deepcopy(self.__elmts)
        if group_name not in self.__elmts:
            if not self.is_flat() and not group_name:
                # generate a random group name and add elements
                group_name = 'UNNAMED_' + _masci_python_util.random_string(5)
                print(f'Warning: adding nested and flat ChemicalElements, '
                      f"adding flat elements to new group '{group_name}'")
            new__elmts[group_name] = {}
        for sym, num in elmts.items():
            new__elmts[group_name][sym] = num
        if not self.__validate_distinctness(new__elmts):
            print(f'Warning: {self.__class__.__name__}.add_elements(): '
                  f'Is nested, chose distinct=True, but elements to add would violate this -> not added.')
        else:
            self.__elmts[group_name] = self._sort(self.__elmts[group_name])
            if group_name not in self.__data:
                self.__data[group_name] = None

    def expand_allowed_elements(self, symbol: str, atomic_number: int):
        """Expand allowed elements definition by a 'special element' which is not in the standard periodic table.

        Example: In some applications, 'X':0 element is used to represent free space.

        Note: This will not add the element to elmts, but enable the addition or removal of the special element.
        """
        assert isinstance(symbol, str) and isinstance(atomic_number, int)

        info_msg_prefix = f'INFO: Requested to expand allowed elements definition by special element ' \
                          f'{{{symbol} : {atomic_number}}}. '

        def _remove_special_element_from_definition(symbol, atomic_number):
            self._special_elements.pop(symbol)
            self._special_elements_inv.pop(atomic_number)
            self._pte.pop(symbol)
            self._pte_inv.pop(atomic_number)

        # check symbol
        if symbol in self._pte:
            if symbol not in self._special_elements:
                print(info_msg_prefix + 'Symbol is a standard element of the periodic table. '
                      'I will not expand definition by this element.')
                return

            # now need to check if the stored special element with the same symbol has a different atomic number
            # if so, remove it
            stored_atomic_number = self._special_elements[symbol]
            if atomic_number != stored_atomic_number:
                print(info_msg_prefix + f"Found stored special element '{stored_atomic_number}' with same symbol. "
                      f'I will replace the latter with the former.')
                _remove_special_element_from_definition(symbol=symbol, atomic_number=stored_atomic_number)

        # check atomic number
        if atomic_number in self._pte_inv:
            if atomic_number not in self._special_elements_inv:
                print(info_msg_prefix + 'Atomic number is that of a standard element of the periodic table. '
                      'I will not expand definition by this element.')
                return

            # now need to check if the stored special element with the same atomic number has a different symbol
            # if so, remove it
            stored_symbol = self._special_elements_inv[atomic_number]
            if symbol != stored_symbol:
                print(info_msg_prefix + f"Found stored special element '{stored_symbol}' with same atomic number. "
                      f'I will replace the latter with the former.')
                _remove_special_element_from_definition(symbol=stored_symbol, atomic_number=atomic_number)

        # okay, now finally clear to expand allowed element definition
        self._special_elements[symbol] = atomic_number
        self._special_elements_inv[atomic_number] = symbol
        self._pte[symbol] = atomic_number
        self._pte_inv[atomic_number] = symbol
        self._sort(self._pte)
        self._sort(self._pte_inv, by_key=True)

    def remove_elements(self,
                        elements,
                        group_name: str = None,
                        delete_empty_groups: bool = True) -> _typing.Union[None, object]:
        """Remove elements. Elmts get resorted afterwards.

        If a now empty group is deleted and corresponding 'data' entry held an object, that object
        is returned.

        :param elements: list of symbols str or atomic numbers int
        :type elements: list
        :param group_name: if flat, ignored, if nested, remove from this group
        :type group_name: str
        :param delete_empty_groups: remove group_name key from elmts if group empty
        :return: None or data object, if respective group gets deleted.
        """
        if isinstance(elements, dict):
            # just assume it's a element sym:num dict
            elements, _ = self._validate(elements)
            elmts = elements
        else:
            elmts = self._chemical_element_list_to_dict(elements, sort=False)
        if group_name is None and self.is_flat():
            group_name = list(self.__elmts.keys())[0]
        if group_name in self.__elmts:
            for sym in elmts:
                self.__elmts[group_name].pop(sym, None)
            if self.__elmts[group_name]:
                self.__elmts[group_name] = self._sort(self.__elmts[group_name])
            if not self.__elmts[group_name] and delete_empty_groups:
                self.__elmts.pop(group_name, None)
                return self.__data.pop(group_name, None)
            if not self.__elmts.keys():
                self.__elmts = {'': {}}
                self.__data = {'': {}}
        else:
            print(f'Warning: {self.__class__.__name__}.remove_elements(): '
                  f"No group '{group_name}' present in elmts. Nothing removed.")
        return None

    def union(self, other):
        return self + other

    def difference(self, other):
        return self - other

    def complement(self, selected_groups: list = None):
        """Return set complement of selected groups of elmts with respect to the set of all possible elements.

        Computes union of elements from selected groups, then complement thereof.

        :param selected_groups: If flat and not specified, use all elements in flat elmts.
        :type selected_groups: list of strings
        :return: complement, flat not nested
        :rtype: ChemicalElements
        """
        data_selection = self.select_groups(selected_groups)
        all_elmts = [sym for elmts in data_selection.values() for sym in elmts]
        complement = list(set(self._pte.keys()) - set(all_elmts))
        complement = self._chemical_element_list_to_dict(complement)
        if not complement:
            # need this since supplying 'nothing' to constructor fills whole table by default
            return ChemicalElements(empty=True, distinct=self.distinct)

        return ChemicalElements(list(complement.keys()), distinct=self.distinct)

    def intersection(self, other):
        """Create intersection of two ChemicalElements objects as a new one.

        :param other: other elements container
        :type other: ChemicalElements
        :return: new elements container
        :rtype: ChemicalElements
        """
        assert isinstance(other, ChemicalElements)
        distinct = self.distinct and other.distinct
        intersection = list(set(self.flatten().keys()) & set(other.flatten().keys()))
        return ChemicalElements(intersection, distinct=distinct)

    def symmetrical_difference(self, other):
        """Create intersection of two ChemicalElements objects as a new one.

        :param other: other elements container
        :type other: ChemicalElements
        :return: new elements container
        :rtype: ChemicalElements
        """
        assert isinstance(other, ChemicalElements)
        return (self - other).union(other - self)

    def __repr__(self):
        """For console output."""
        return self.to_string()

    def to_string(self, selected_groups: list = None, indent=4):
        """Print elmts dict nicely indented with linebreaks.
        """
        elmts = self.select_groups(selected_groups)
        if len(elmts.keys()) == 1:
            key = list(elmts.keys())[0]
            elmts = elmts[key]
        return _json.dumps(elmts, indent=indent)

    def print(self, selected_groups: list = None, indent=4):
        """Print elmts dict nicely indented with linebreaks.
        """
        print(self.to_string(selected_groups, indent))

    def to_file(self, filepath):
        """Save elements to file. 'data' is ignored.

        :param filepath: filepath
        :type filepath: str or pathlib.Path
        """
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(_json.dumps(self.__elmts))

    def _get_mendeleev_periodic_table(self):
        """Get full periodic table pandas dataframe from mendeleev."""

        # DEVNOTE: breaking change in mendeleev v0.7.0: replaced get_table with fetch.fetch_table.
        version = _mendeleev.__version__
        version_info = tuple(int(num) for num in version.split('.'))
        if version_info < (0, 7, 0):
            return _mendeleev.get_table('elements')
        import mendeleev.fetch as _mendeleev_fetch
        return _mendeleev_fetch.fetch_table('elements')

    def list_of_attributes(self):
        """Get list of available periodic table attributes from mendeleev."""
        return self._get_mendeleev_periodic_table().columns

    def save_plotting_profile(self, filepath=None, force_overwrite: bool = False):
        """Save plotting profile for :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.plot`.

        This allows to reuse a plotting profile later, to keep consistency between plots.

        Current format of the file is JSON.

        :param filepath: where to save the the profile file.
        :type filepath: str or pathlib.Path
        :param force_overwrite: True: overwrite existing config files. Default False.
        """

        if not self.plotting_profile:
            print('Warning: no plotting profile set. I will do nothing.')
            return

        if not filepath:
            _filepath = _Path.cwd() / 'imp_host_embedding_batches.json'
        elif isinstance(filepath, str):
            _filepath = _Path(filepath)
        else:
            _filepath = filepath

        # persist
        if _filepath.exists() and _filepath.is_file():
            msg = f"File '{_filepath}' exists. Force overwrite = {force_overwrite}."
            msg = f'WARNING: {msg}' if force_overwrite else f'INFO: {msg}'
            print(msg)
            if not force_overwrite:
                return

        data = _copy.deepcopy(self.plotting_profile)
        # assert isinstance(data, ChemicalElementsPlottingProfile) # for autocompletion
        # prevent lists, dicts, tuples to be item-indented in output JSON
        data.values_range = _masci_python_util.NoIndent(data.values_range)
        data.colormap = _masci_python_util.NoIndent(data.colormap)
        data.size = _masci_python_util.NoIndent(data.size)
        data = _dc.asdict(data)

        with open(_filepath, 'w', encoding='utf-8') as file:
            file.write(_json.dumps(data, cls=_masci_python_util.JSONEncoderTailoredIndent, indent=4))

    def load_plotting_profile(self, filepath):
        """Load plotting profile for :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.plot`.

        :param filepath: where the profile file is saved.
        :type filepath: str or pathlib.Path
        """
        try:
            with open(filepath, encoding='utf-8') as file:
                data = _json.load(file)
        except (FileNotFoundError, _json.JSONDecodeError) as err:
            print(f'File {filepath} not found or JSON decoding -> dict failed.')
            raise err

        try:
            data = ChemicalElementsPlottingProfile(**data)
            # print(type(data)) # for testing
            self.plotting_profile = data
            print(f'Successfully loaded plotting profile from file {filepath}.')
        except Exception as err:  # errors: Attribute, Assertion, ...
            dummy = ChemicalElementsPlottingProfile()
            print(f"Failed loading '{ChemicalElementsPlottingProfile.__name__}' from file "
                  f'{filepath}. Check if file has required version: {dummy._version}. '
                  f'If this is satisfied, it is otherwise corrupted.')
            raise err

    def plot(self,
             selected_groups: list = None,
             title: str = '',
             colorby: str = 'group',
             attribute: str = None,
             without_attribute: bool = False,
             missing_value=None,
             missing_color: str = '#bfbfbf',
             missing_name: str = 'Missing',
             missing_group_value=1,
             colormap_name: str = 'RdBu_r',
             colormap: dict = None,
             size: tuple = (1000, 800),
             output: str = None,
             showfblock: bool = True,
             long_version: bool = False,
             with_legend: bool = False,
             legend_title: str = 'Legend',
             use_plotting_profile: bool = True):
        """Plot elements in a periodic table, missing elements greyed out.

        The colormap for the present elements can be chosen via the 'colorby' parameter in either of two ways:
        A) Colorize them by a physical  attribute. For available periodic table attributes, see
        :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.list_of_attributes`. B) Colorize them by their
        group assignment within this instance. If there are no groups (i.e., flat not nested), then all present elements
        will have one color. If selected groups is None, will include all of the instance's groups.

        The value to display below each element is controlled via the 'attribute' parameter. Apart from
        physical attributes, group names can also be chosen to be displayed, if they are numeric.
        To do that, set the same value (argument) for the 'attribute' and 'title' parameters.

        If the title and attribute rendering are not enough, an additional matplotlib figure, acting as legend,
        can be returned.

        For available colormap names, see:

        - https://seaborn.pydata.org/tutorial/color_palettes.html
        - https://matplotlib.org/stable/tutorials/colors/colormaps.html

        :param selected_groups: If flat and not specified, use all elements in flat elmts, else if nested,
               a group subset.
        :param title: Title to appear above the periodic table.
        :param colorby: 'group': Colormap by selected groups, 'attribute': by mendeleev periodic table attribute.
        :param attribute: Attribute's value displayed below elements. Either PTE attribute, or group values.
        :param without_attribute: Do not display the attribute values below the elements.
        :param missing_value: Replaces NaN values, e.g. for custom coloring.
        :type missing_value: str or numeric. Prefer same type as coloring input (group names or attribute).
        :param missing_color: Hex code of the color to be used for the missing values
               (#ffffff white, #bfbfbf light gray).
        :param missing_name: Name to be used for missing values in the legend. If empty, will use missing_value.
        :param missing_group_value: If colorby 'group' and instance is flat, this correct missing colorisation.
        :param colormap_name: Name of seaborn or matplotlib colormap.
        :param colormap: Dictionary {value : hexcolor string}. If not specified, created from colormap_name.
        :param size: Tuple (width, height) of the table figure in pixels.
        :param output: Optional output, e.g. 'img/table.html'. If legend, will also save 'img/table_legend.png'.
        :param showfblock: Show the elements from the f block.
        :param long_version: Show the long version of the periodic table with the f block between the s and d blocks.
        :param with_legend: True: return extra matplotlib figure = legend. plot(...) will render it below the table.
        :param legend_title: If empty, will replace with table title.
        :param use_plotting_profile: If a profile has been set, prefer overlay profile arguments over the ones here.
        :return: Legend or None.
        """
        _title = title
        _output = output
        _legend_title = legend_title
        _missing_value = missing_value
        _missing_name = missing_name
        _missing_color = missing_color
        _missing_group_value = missing_group_value
        _colorby = colorby
        _attribute = attribute
        _without_attribute = without_attribute
        _colormap_name = colormap_name
        _colormap = _copy.copy(colormap)
        _size = size
        _showfblock = showfblock
        _long_version = long_version
        _with_legend = with_legend

        if use_plotting_profile:
            if not self.plotting_profile:
                print('Warning: no plotting profile set. I will fall back to method arguments.')
            else:
                pp = self.plotting_profile
                assert isinstance(pp, ChemicalElementsPlottingProfile)  # for autocompletion
                _title = pp.title_prefix + title if (pp.title_prefix) else title
                _output = pp.output_prefix + output if (output and pp.output_prefix) else output
                _legend_title = pp.legend_title_prefix + legend_title if (legend_title and
                                                                          pp.legend_title_prefix) else legend_title
                _missing_value = pp.missing_value if pp.missing_value is not None else missing_value
                _missing_name = pp.missing_name if pp.missing_name else missing_name
                _missing_color = pp.missing_color if pp.missing_color else missing_color
                _missing_group_value = pp.missing_group_value if pp.missing_group_value else missing_group_value
                _colorby = pp.colorby if pp.colorby else colorby
                if pp.attribute:
                    _attribute = pp.attribute
                else:
                    if attribute == title and pp.title_prefix:
                        _attribute = pp.title_prefix + attribute
                    else:
                        _attribute = attribute
                _without_attribute = pp.without_attribute if pp.without_attribute is not None else without_attribute
                _colormap_name = pp.colormap_name if pp.colormap_name else colormap_name
                _colormap = _copy.copy(pp.colormap) if pp.colormap else _colormap
                _size = pp.size if pp.size else size
                _showfblock = pp.showfblock if pp.showfblock is not None else showfblock
                _long_version = pp.long_version if pp.long_version is not None else long_version
                _with_legend = pp.with_legend if pp.with_legend is not None else with_legend

        # validate inputs
        valid_colorby_values = ['group', 'attribute']
        valid_attributes = self.list_of_attributes()
        if _colorby not in valid_colorby_values:
            raise KeyError(f"Specified argument 'colorby'='{_colorby}', but must be one of {valid_colorby_values}.")
        if _attribute != _title and _attribute not in valid_attributes:
            raise KeyError(f"Specified argument 'attribute'='{_attribute}', but must be one of {valid_attributes}, "
                           f"or equal argument of parameter 'title'.")

        # init output for notebook. if not notebook, this won't have any effect.
        _bokeh.plotting.output_notebook()

        # set up file output
        _output_mendel = _output
        _output_ext = '.html'
        if _output_mendel:
            msg_suffix = ''
            if not _output_mendel.endswith(_output_ext):
                _output_mendel = _output_mendel + _output_ext
                msg_suffix = f"Info: filepath did not end in extension '{_output_ext}'. Appended it."
            print(f'Will write HTML table plot to file {_output_mendel}. {msg_suffix}')
            _bokeh.plotting.output_file(filename=_output_mendel)

        # declare inner variables as arguments for mendeleev plot parameters
        _colorby_mendel, _attribute_mendel = f'{_title}_color', None

        # get instance's elements, nested or flat
        groups = self.select_groups(selected_groups, include_special_elements=False)

        # correct for a particular ChemicalElements quirk: if the CE instance was created flat and
        # groups unchanged, it will (at current implementation) have one single group name, the empty string.
        # If colorby group, this will lead to mendeleev plotting a white table. To prevent that, could either
        # rename the group in the instance, or better rename it in the extracted dict, leaving the CE instance
        # invariant.
        if _colorby == 'group' and (list(self.__elmts.keys()) == ['']):
            elements = groups.pop('')
            groups[_missing_group_value] = elements

            # get the periodic table dataframe
        ptable = self._get_mendeleev_periodic_table()

        # check some conditionals
        is_missing_value_numeric = isinstance(_missing_value, _numbers.Number)

        def _create_column_from_groups():
            for group_key, group in groups.items():
                for symbol in group.keys():
                    ptable.loc[ptable['symbol'] == symbol, [_title]] = group_key

        def _deal_with_missing_values(_missing_value) -> _typing.Tuple[bool, _typing.Any]:
            """Deal with missing values.

            :return: True: filled in missing value, False: not.
            """
            fill_in = False

            is_numeric = all(isinstance(item, _numbers.Number) for item in ptable[_title].to_list())

            if _missing_value is not None:
                if _missing_value in ptable[_title].to_list():
                    print(f'Warning: Specified missing value {_missing_value} would overwrite existing value in '
                          f"column '{_title}'. Will not replace NaN values with it.")
                elif is_numeric:
                    fill_in = is_missing_value_numeric
                else:
                    fill_in = True
                    if is_missing_value_numeric:
                        _missing_value = str(_missing_value)

            if fill_in:
                ptable[_title] = ptable[_title].fillna(_missing_value)
            return fill_in, _missing_value

        legend_figure = None

        # make a new column for the data to be displayed
        if _colorby == 'attribute':
            _attribute_mendel = _title

            # copy attribute col to new title col
            ptable[_title] = ptable[_attribute]
            # deal with missing values
            # first, replace values of all items not present in groups
            missing_elements = self.complement(selected_groups=selected_groups)
            for symbol in missing_elements:
                ptable.loc[ptable['symbol'] == symbol, [_title]] = _np.NaN

        elif _colorby == 'group':
            _attribute_mendel = _attribute

            for group_key, group in groups.items():
                for symbol in group.keys():
                    ptable.loc[ptable['symbol'] == symbol, [_title]] = group_key

        if _without_attribute:
            # create a column with empty values and set that as attribute to display for mendeleev.
            _attribute_mendel = 'empty'
            ptable['empty'] = ' '

        values = sorted(ptable[_title].dropna().unique())
        filled_in, _missing_value = _deal_with_missing_values(_missing_value)

        # # let pandas convert values to most sensible types
        # # Example use case: when group names are integer, legend would display them as floats without this.
        # ptable[title] = ptable[title].convert_dtypes()
        # DEVnote: Commented out, cause this also converts NaN into pandas.NA, and mendeleev plotting method
        # can't deal with the latter. And seems like legend int problem above solved itself without this.

        # for the title column, either use specified colormap, or create custom one from given name
        if _colormap:
            # check if colormap can cover item values. must be a superset or true superset.
            if not all(val in _colormap.keys() for val in values):
                _standard_colormap_name = 'RdBu_r'
                print('Warning: Specified colormap does not cover all values to be colorized. '
                      f"Will fall back to mendeleev standard colormap '{_standard_colormap_name}'."
                      f'\nSpecified Colormap: {_colormap}'
                      f'\nSpecified Colormap name: {_colormap_name}'
                      f'\nValues to be colorized: {values}')
                _colormap_name = _standard_colormap_name
        else:
            # create custom colormpa from gien name
            _colormap = {
                key: _mpl.colors.rgb2hex(rgb)
                for key, rgb in zip(values, _sns.color_palette(palette=_colormap_name, n_colors=len(values)))
            }

        if filled_in:
            if _missing_color in _colormap.values():
                print(f"Warning: Specified missing color value '{_missing_color}' overwrites existing "
                      f'color value. Better choose another one.')
            _colormap[_missing_value] = _missing_color

        # add custom colormap column
        ptable[_colorby_mendel] = ptable[_title].map(_colormap)

        if _with_legend:
            # for the legend color map, we want to use the missing_name instead of the missing_value,
            # and put it first. So, got to repopultate the custom colormap.
            if filled_in:
                _missing_name_inner = _missing_name if _missing_name else _missing_value
                # prepend missing name to dict
                _colormap.pop(_missing_value)
                cmap_copy = _copy.copy(_colormap)
                _colormap = {_missing_name_inner: _missing_color}
                for key, hexcolor in cmap_copy.items():
                    _colormap[key] = hexcolor

            # _legend_title = legend_title if legend_title else title
            _legend_title_inner = _legend_title
            if not _legend_title_inner or _legend_title_inner == 'Legend':
                _legend_title_inner = _legend_title_inner + f' (attribute: {_attribute_mendel})'
            legend_figure = _masci_plot_methods.plot_colortable(colors=_colormap,
                                                                title=_legend_title_inner,
                                                                sort_colors=False)

            # save legend figure if specified
            if _output_mendel:
                _output_legend = _os.path.splitext(_output_mendel)
                _output_legend = _output_legend[0] + '_legend'
                plt.savefig(_output_legend)

        # finally, draw the plot(s)
        # DEVNOTE: breaking change in mendeleev v0.8.0: replaced plotting with vis, signature change.
        version = _mendeleev.__version__
        version_info = tuple(int(num) for num in version.split('.'))
        if version_info < (0, 8, 0):
            import mendeleev.plotting as _mendeleev_plotting  #pylint: disable=no-name-in-module, import-error
            _mendeleev_plotting.periodic_plot(df=ptable,
                                              attribute=_attribute_mendel,
                                              title=_title,
                                              width=_size[0],
                                              height=_size[1],
                                              missing=_missing_color,
                                              colorby=_colorby_mendel,
                                              output=_output_mendel,
                                              showfblock=showfblock,
                                              long_version=long_version)
        else:
            raise NotImplementedError(f'mendeleev version {version}: TODO: implement plotting API change '
                                      f'"plotting" -> "vis".')
        return legend_figure

    def _sort(self, a_dict: _typing.Dict[str, int], by_key=False):
        """Sorts chemical element dict by atomic number.

        :param a_dict: dict key = symbol str : value = atomic_number int
        :type a_dict: dict
        :param by_key: sort by key or value
        :type by_key: bool
        :return: sorted dict
        :rtype: dict
        """
        return dict(sorted(a_dict.items(), key=lambda item: item[not by_key]))

    def _validate(self, elements: T_FLAT_ELEMENTS_CONTAINER) -> _typing.Tuple[T_FLAT_ELEMENTS_CONTAINER, bool]:
        """Checks that no non-valid elements are present.

        :return: tuple of (passed elements, bool), bool: are keys symbol str or atomic number int ('keys'=items if list)
        """
        list_types = (list, tuple, set)
        if isinstance(elements, list_types):
            key_is_symbol = None
            if all(elem in self._pte for elem in elements):
                assert all(elem in self._pte for elem in elements)
                key_is_symbol = True
            elif all(isinstance(num, int) for num in elements):
                assert all(elem in self._pte_inv for elem in elements)
                key_is_symbol = False
            else:
                raise TypeError('received a list, but need list of all atom names or numbers')
            return elements, key_is_symbol
        if isinstance(elements, dict):
            # just assume it is a flat dict
            # i know this is not the most efficient way to test this

            # first, invert dict if needed to simplify cases
            if any(isinstance(k, int) for k in elements.keys()):
                assert all(isinstance(k, int) for k in elements.keys())
                elements = {v: k for k, v in elements.items()}

            # now assume dict is sym:num, else raise error
            if any(isinstance(k, str) for k in elements.keys()):
                assert all(isinstance(k, str) for k in elements.keys())
                assert all(isinstance(v, int) for v in elements.values())
                key_is_symbol = True
                return elements, key_is_symbol

            raise TypeError('received a dict, but need chem.elmt. dict sym:num or num:sym')

        raise TypeError('Elements list is not any of list,tuple,set,dict.')

    def _chemical_element_list_to_dict(self, elements: T_FLAT_ELEMENTS_CONTAINER, sort=True) -> _typing.Dict[str, int]:
        """Converts list/set/tuple of chemical elements into dict symbol : atomic_number.
        :type elements: list, tuple or set of 1) symbols str or 2) atomic numbers int
        :return: dict sym:num
        :rtype: dict
        """
        elements, key_is_sym = self._validate(elements)
        if key_is_sym:
            a_dict = {sym: num for (sym, num) in self._pte.items() if sym in elements}
        else:
            a_dict = {sym: num for (sym, num) in self._pte.items() if num in elements}

        if sort:
            return self._sort(a_dict)

        return a_dict


@_dc.dataclass
class PeriodicTable:
    """Periodic tables for different properties. Properties may be incomplete.

    Current properties: elemental crystal structure, agnetic elements.
    """
    table: ChemicalElements = _masci_python_util.dataclass_default_field(ChemicalElements())
    crystal: ChemicalElements = _masci_python_util.dataclass_default_field(
        ChemicalElements({
            'fcc': ['Ir', 'Pd', 'Pb', 'Pt', 'Al', 'Cu', 'Ca', 'Ag', 'Au', 'Sr', 'Mn', 'Ni'],
            'bcc': ['Ba', 'Cr', 'Cs', 'Fe', 'K', 'Mo', 'Nb', 'Rb', 'Ta', 'V', 'W'],
            'hcp': ['Be', 'Cd', 'Co', 'He', 'Hf', 'Mg', 'Os', 'Re', 'Ru', 'Sc', 'Tc', 'Ti', 'Tl', 'Y', 'Zn', 'Zr'],
            'diamond': ['Ge', 'Si', 'Sn'],
            'rhombohedral': ['As', 'Bi', 'Sb']
        }))
    magnet: ChemicalElements = _masci_python_util.dataclass_default_field(
        ChemicalElements({
            'ferromagnetic': ['Fe', 'Co', 'Ni'],
            'antiferromagnetic': ['Cr', 'Mn', 'O']
        }))
