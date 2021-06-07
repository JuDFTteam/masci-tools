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
"""This module contains a simple class for set-like chemical elements enumeration."""
import dataclasses as _dc
import numpy as _np
import masci_tools.vis.plot_methods as _plot_methods


@_dc.dataclass(init=True, repr=True, eq=True, order=False, frozen=False)
class ChemicalElementsPlottingProfile:
    """"For reusing plotting settings over several plots. Serializable.

    Instances of this class can be used as input to the :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.plot`
    method, to simplify reusing non-changing argumments over a series of periodic table plots. The profile can be saved
    to and loaded from a JSON file for reuse as well.

    :param profile_name: name of the profile
    :param values_range: list of numeric, sorted, unique values. Must contain at least all plotted attribute values.
    :param missing_value: Value to set for missing elements.
    :param missing_name: Name to set for missing elements in legend.
    :param title_prefix: If set, will be preprended to plot title.
    :param output_prefix: If set, will be prepended to plot output filepath.
    :param legend_title_prefix: If set, will be prepended to legend title.
    :param colorby: 'group': Colormap by selected groups, 'attribute': by mendeleev periodic table attribute.
    :param attribute: Attribute's value displayed below elements. Either PTE attribute, or group values.
    :param colormap_name: Name of seaborn or matplotlib colormap.
    :param missing_color: Hex code of the color to be used for the missing values (#ffffff white, #bfbfbf light gray).
    :param colormap: Dictionary {value : hexcolor string}. If not specified, created from value_range and map name.
    :param size: Tuple (width, height) of the table figure in pixels.
    :param showfblock: Show the elements from the f block
    :param long_version: Show the long version of the periodic table with the f block between the s and d blocks.
    :param with_legend: True: return extra matplotlib figure = legend. plot(...) will render it below the table.
    """
    from masci_tools.util.python_util import dataclass_default_field as _field

    profile_name: str = ''
    values_range: list = _field([])
    missing_value: object = None
    missing_name: str = 'Missing'
    title_prefix: str = None
    output_prefix: str = None
    legend_title_prefix: str = None
    colorby: str = 'group'
    attribute: str = 'atomic_weight'
    colormap_name: str = 'PiYG'
    missing_color: str = '#404040'
    colormap: dict = _field({})
    size: tuple = _field(())
    showfblock: bool = True
    long_version: bool = False
    with_legend: bool = True
    _version: int = 1
    _cls_name: str = ''

    def __post_init__(self):
        """Create colormap from values_range, if the former was not specified."""
        # save class name
        cls = type(self)
        self._cls_name = cls.__module__ + '.' + cls.__name__

        # create colormap
        if not self.colormap and self.values_range:
            import seaborn as sns
            import matplotlib.colors
            self.colormap = {
                key: matplotlib.colors.rgb2hex(rgb) for key, rgb in zip(
                    self.values_range, sns.color_palette(palette=self.colormap_name, n_colors=len(self.values_range)))
            }

    def save(self, filepath):
        raise NotImplementedError()


class ChemicalElements:
    """A container for safe chemical element enumeration."""

    def __init__(self,
                 elements=None,
                 empty=False,
                 groups=None,
                 distinct=False,
                 special_elements: dict = None,
                 filepath=None):
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
        :type groups: list of strings.
        :param distinct: True: disallow same element in different groups.
        :param special_elements: dict symbol:atomic_number of special elements (eg {'X':0} for vacuum)
        :param filepath: if not None, init from JSON file. Must have been written with ChemicalElements.to_file().
        :type filepath: str or pathlib.Path

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
            import json
            with open(filepath, 'r') as file:
                self.__elmts = json.load(file)
            self.__data = {group_name: None for group_name in self.__elmts.keys()}
        else:
            # init elmts, convert to [optional: container of:] dict[s] sym:num.
            import copy
            if groups:
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
                        self.__elmts = {'': copy.deepcopy(self._pte)}

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

    def is_flat(self):
        """True if 'elmts' is dict of chemical elements, False if a dict of groups of such.
        """
        return (not list(self.__elmts.keys())) or (list(self.__elmts.keys()) == ['']) or (len(self.__elmts.keys()) == 1)

    @property
    def elmts(self):
        """If flat, returns list of chemical elements, else groups of such.

        Note that read-only, returns deepcopy.
        """
        import copy
        if self.is_flat():
            key = list(self.__elmts.keys())[0]
            return copy.deepcopy(self.__elmts[key])
        else:
            return copy.deepcopy(self.__elmts)

    @property
    def data(self):
        """Returns full 'data' object storage with all groups.

        Note that if nested, is read-only, returns deepcopy.
        """
        import copy
        if self.is_flat():
            return self.data
            # key = list(self.__elmts.keys())[0]
            # return self.__data[key]
            # return copy.deepcopy(self.__data[key])
        else:
            # return self.__data
            return copy.deepcopy(self.__data)

    def get_data(self, group_name: str):
        """Returns 'data' object storage for given group.
        """
        if self.is_flat():
            return self.data
        else:
            return self.__data[group_name]

    def set_data(self, group_name: str, an_object):
        """Set a data item in the 'data' object storage.

        :return: previously stored data item if present
        """
        if self.is_flat():
            key = list(self.__elmts.keys())[0]
        else:
            if group_name not in self.groups():
                raise KeyError('Supplied group name does not exist.')
            key = group_name
        dump = self.__data.pop(key, None)
        self.__data[key] = an_object
        return dump

    def pop_data(self, group_name: str):
        return self.set_data(group_name, None)

    def __eq__(self, other: object) -> bool:
        """Overload '==' operator and '!=' operator. Check for equality.

        Note: this DOES take grouping into account.
        """
        if isinstance(other, ChemicalElements):
            return self.__elmts == other.__elmts
        return False

    def __le__(self, other):
        """Overload '<=' operator. Is this subset of other.

        True if this flattened is a subset of the other (ie, ignoring grouping).

        :param other: possible superset
        :type other: ChemicalElements
        """
        assert isinstance(other, ChemicalElements)
        return (other + self).flatten(as_dict=False) == other.flatten(as_dict=False)

    def __lt__(self, other):
        """Overload '<' operator. Is this true subset of other.

        True if this flattened is a subset of the other (ie, ignoring grouping).

        :param other: possible superset
        :type other: ChemicalElements
        """
        return (self <= other) and (self.count() < other.count())

    def __ge__(self, other):
        """Overload '>=' operator. Is other subset of this.

        True if other flattened is a subset of this (ie, ignoring grouping).

        :param other: possible subset
        :type other: ChemicalElements
        """
        assert isinstance(other, ChemicalElements)
        return (self + other).flatten(as_dict=False) == self.flatten(as_dict=False)

    def __gt__(self, other):
        """Overload '>' operator. Is other true subset of this.

        True if other flattened is a true subset of this (ie, ignoring grouping).

        :param other: possible subset
        :type other: ChemicalElements
        """
        assert isinstance(other, ChemicalElements)
        return (self >= other) and (self.count() > other.count())

    def __getitem__(self, group_name_or_symbol):
        """Overload '[]' operator, getter.

        If flat, returns symbol's atomic number, if nested, returns group of elements.
        If flat, also allows inverted input: atomic_number, return symbol.
        """
        if isinstance(group_name_or_symbol, str):
            return self.elmts[group_name_or_symbol]
        elif isinstance(group_name_or_symbol, int):
            if self.is_flat():
                return self.invert()[group_name_or_symbol]
            else:
                raise KeyError('Querying [atomic_number] not possible for nested elmts.')
        else:
            raise KeyError(f"Unsupported key/value type '{type(group_name_or_symbol)}'.")

    def __validate_distinctness(self, new__elmts):
        import copy
        if not self.is_flat() and self.distinct:
            elmt_count = 0
            for group_name, group in new__elmts.items():
                elmt_count += len(group.keys())
            distinct_count = len(set().union(*[set(group.keys()) for group_name, group in new__elmts.items()]))
            if elmt_count == distinct_count:
                self.__elmts = copy.deepcopy(new__elmts)
                return True
            else:
                return False
        else:
            self.__elmts = copy.deepcopy(new__elmts)
            return True

    def __setitem__(self, group_name, elements):
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
        elif isinstance(item, (list, dict)):
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
        else:
            if delete_empty_groups:
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
        if self.is_flat() and not in_place:
            import copy
            if as_dict:
                return copy.deepcopy(self.elmts)
            else:
                return ChemicalElements(self.elmts)
        elif not self.is_flat():
            data_selection = self.select_groups(selected_groups)
            flattened = {}
            for group_name, group in data_selection.items():
                for sym, num in group.items():
                    flattened[sym] = num
            if in_place:
                self.__elmts = {'': flattened}
                self.__data = {'': None}
            else:
                if as_dict:
                    return flattened
                else:
                    return ChemicalElements(flattened)

    def count_groups(self, selected_groups: list = None):
        """If flat, return element count. If nested, return dict with element count per group.

        :param selected_groups: only is nested: only count specified groups.
        :type selected_groups: list of strings
        """
        if self.is_flat():
            return len(self.elmts.keys())
        else:
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
            elif group_name is None:
                return len(self.flatten().keys())
            else:  # group_name but not in self.__elmts
                raise KeyError(f"Group '{group_name}' is not in elmts.")

        def contains_item(a_dict):
            if isinstance(item, str):
                return int(item in a_dict)
            elif isinstance(item, int):
                return int(item in a_dict.values())
            else:
                return int(False)

        if self.is_flat():
            return contains_item(self.elmts)
        elif group_name is None:  # and nested
            # check all groups
            count = 0
            for group in self.elmts.values():
                count += contains_item(group)
            return count
        else:  # nested and group_name
            return contains_item(self.elmts[group_name])

    def groups(self):
        """Returns list of group names. If elmts is flat (only one group), will return empty list.
        """
        if self.is_flat():
            return []
        else:
            return list(self.elmts.keys())

    def select_groups(self, selected_groups: list = None, include_special_elements: bool = True, as_dict=True):
        """Return only selected groups from elmts. Always returns a copy.

        :param selected_groups: If flat and not specified, return the empty name group of flat elmts.
        :type selected_groups: list of strings
        :param include_special_elements: False: remove special elements if any defined. This returns a copy always.
        :param as_dict: True: return as dict, False: as ChemicalElements
        :return: subset of elmts
        :rtype: dict
        """
        import copy

        elements = copy.deepcopy(self.__elmts)

        if not include_special_elements:
            for group_name, group in elements.items():
                for special_symbol in self._special_elements:
                    elements[group_name].pop(special_symbol, None)

        if not selected_groups or (set(self.groups()) == set(selected_groups)):
            # always return non-flat view, ie if flat, dict with one group
            if as_dict:
                return elements
            else:
                return self
        else:
            a_dict = {
                data_group: elmts for data_group, elmts in elements.items()
                for selection_group in selected_groups
                if data_group == selection_group
            }
            if as_dict:
                return a_dict
            else:
                elmts = ChemicalElements(empty=True)
                for group_name, group in a_dict.items():
                    elmts.add_elements(elements=group, group_name=group_name)
                return elmts

    def rename_group(self, old_group_name, new_group_name):
        """Rename a group.
        """
        group = self.__elmts.pop(old_group_name)
        self.add_elements(group, new_group_name)

        data = self.__data.pop(old_group_name)
        self.__data[new_group_name] = data

    def group_difference(self, group_name1: str, group_name2: str) -> dict:
        """Return difference between two groups.

        If one is the true superset, the set left difference is returned (what is in the one that is not in the other).

        If not, the symmetrical difference is returned.
        """
        if self.is_flat():
            raise KeyError('Elmts is flat, no groups to compare.')
        if not ((group_name1 in self.groups()) and (group_name2 in self.groups())):
            raise KeyError(f"Elmts has no groups '{group_name1}', '{group_name2}'.")
        distinct = self.distinct
        elmts_group1 = ChemicalElements(self[group_name1], distinct=distinct)
        elmts_group2 = ChemicalElements(self[group_name2], distinct=distinct)
        if elmts_group1 == elmts_group2:
            print(f"'{group_name1}' equal to '{group_name2}'")
            return ChemicalElements(empty=True, distinct=distinct)
        elif elmts_group1 > elmts_group2:
            print(f"'{group_name1}' true superset of '{group_name2}'")
            return elmts_group1 - elmts_group2
        elif elmts_group1 < elmts_group2:
            print(f"'{group_name1}' true subset of '{group_name2}'")
            return elmts_group2 - elmts_group1
        else:
            print(f"'{group_name1}', '{group_name2}' not subsets of each other, return symmetrical difference")
            return elmts_group1.symmetrical_difference(elmts_group2)

    def compare_groups(self, group_name1, group_name2):
        from deepdiff import DeepDiff
        if self.is_flat():
            raise KeyError('Elmts is flat, no groups to compare.')
        if not ((group_name1 in self.groups()) and (group_name2 in self.groups())):
            raise KeyError(f"Elmts has no groups '{group_name1}', '{group_name2}'.")
        return DeepDiff(self[group_name1], self[group_name2], ignore_order=True, ignore_numeric_type_changes=True)

    def invert(self, group_name: str = None):
        """If flat, return inverted element dict symbol : atomic number to num:sym, or group elmt dict if nested.

        :return: inverted chemical elements dict
        :rtype: dict
        """
        if self.is_flat():
            elmts = self.elmts if self.is_flat() else self.__elmts[group_name]
        else:
            if group_name:
                elmts = self.__elmts[group_name]
            else:
                raise KeyError('Is nested, but did not supply group name.')
        return {v: k for k, v in elmts.items()}

    def get_groups_for(self, symbol: str):
        """Find the group names for the groups the chemical element is contained in.
        :param symbol: chemical element symbol
        :return: list of group_names or None if no find or if flat
        """
        if self.is_flat():
            return []
        else:
            group_names = [group_name for group_name in self.elmts if symbol in self.elmts[group_name]]
            if group_names:
                return group_names
            else:
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

        import copy
        new__elmts = copy.deepcopy(self.__elmts)
        if group_name not in self.__elmts:
            if not self.is_flat() and not group_name:
                # generate a random group name and add elements
                from masci_tools.util.python_util import random_string
                group_name = 'UNNAMED_' + random_string(5)
                print(f'Warning: adding nested and flat ChemicalElements, '
                      f"adding flat elements to new group '{group_name}'")
            new__elmts[group_name] = {}
        for sym, num in elmts.items():
            new__elmts[group_name][sym] = num
        if not self.__validate_distinctness(new__elmts):
            print('Warning: Chose distinctness, added elements would violate. Not added.')
        else:
            self.__elmts[group_name] = self._sort(self.__elmts[group_name])
            if not group_name in self.__data:
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
            else:
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
            else:
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

    def remove_elements(self, elements, group_name: str = None, delete_empty_groups: bool = True):
        """Remove elements. Elmts get resorted afterwards.

        If a now empty group is deleted and corresponding 'data' entry held an object, that object
        is returned.

        :param elements: list of symbols str or atomic numbers int
        :type elements: list
        :param group_name: if flat, ignored, if nested, remove from this group
        :type group_name: str
        :param delete_empty_groups: remove group_name key from elmts if group empty
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
                self.__data.pop(group_name, None)
            if not self.__elmts.keys():
                self.__elmts = {'': {}}
                self.__data = {'': {}}
        else:
            print(f"Warning: no group '{group_name}' present in elmts. Nothing removed.")

    def union(self, other):
        return self.__add__(other)

    def difference(self, other):
        return self.__sub__(other)

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
            # neeed this since supplying 'nothing' to constructor fills whole table by default
            return ChemicalElements(empty=True, distinct=self.distinct)
        else:
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
        import json
        elmts = self.select_groups(selected_groups)
        if len(elmts.keys()) == 1:
            key = list(elmts.keys())[0]
            elmts = elmts[key]
        return json.dumps(elmts, indent=indent)

    def print(self, selected_groups: list = None, indent=4):
        """Print elmts dict nicely indented with linebreaks.
        """
        print(self.to_string(selected_groups, indent))

    def to_file(self, filepath):
        """Save elements to file. 'data' is ignored.

        :param filepath: filepath
        :type filepath: str or pathlib.Path
        """
        import json
        with open(filepath, 'w') as file:
            file.write(json.dumps(self.__elmts))

    def _get_mendeleev_periodic_table(self):
        """Get full periodic table pandas dataframe from mendeleev."""

        # DEVNOTE: breaking change in mendeleev v0.7.0: replaced get_table with fetch.fetch_table.
        import mendeleev
        version = mendeleev.__version__
        version_info = tuple(int(num) for num in version.split('.'))
        if version_info < (0, 7, 0):
            pte = mendeleev.get_table('elements')
        else:
            from mendeleev.fetch import fetch_table
            pte = fetch_table('elements')

        return pte

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

        from masci_tools.util.python_util import JSONEncoderTailoredIndent, NoIndent
        from pathlib import Path

        if not filepath:
            _filepath = Path.cwd() / 'imp_host_embedding_batches.json'
        elif isinstance(filepath, str):
            _filepath = Path(filepath)
        else:
            _filepath = filepath

        # persist
        import json
        if _filepath.exists() and _filepath.is_file():
            msg = f"File '{_filepath}' exists. Force overwrite = {force_overwrite}."
            msg = f'WARNING: {msg}' if force_overwrite else f'INFO: {msg}'
            print(msg)
            if not force_overwrite:
                return

        import copy
        data = copy.deepcopy(self.plotting_profile)
        # assert isinstance(data, ChemicalElementsPlottingProfile) # for autocompletion
        # prevent lists, dicts, tuples to be item-indented in output JSON
        data.values_range = NoIndent(data.values_range)
        data.colormap = NoIndent(data.colormap)
        data.size = NoIndent(data.size)
        data = _dc.asdict(data)

        with open(_filepath, 'w') as file:
            file.write(json.dumps(data, cls=JSONEncoderTailoredIndent, indent=4))

    def load_plotting_profile(self, filepath):
        """Load plotting profile for :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.plot`.

        :param filepath: where the profile file is saved.
        :type filepath: str or pathlib.Path
        """
        from json import JSONDecodeError
        import json

        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, JSONDecodeError) as err:
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
             attribute: str = 'atomic_weight',
             missing_value=None,
             missing_color: str = '#bfbfbf',
             missing_name: str = 'Missing',
             colormap_name: str = 'RdBu_r',
             colormap: dict = None,
             size: tuple = (1000, 800),
             output: str = None,
             showfblock: bool = True,
             long_version: bool = False,
             with_legend: bool = True,
             legend_title: str = 'Legend',
             use_plotting_profile: bool = True):
        """Plot elements in a periodic table, missing elements greyed out.

        The colormap for the present elements can be chosen via the 'colorby' parameter in either of two ways:
        A) Colorize them by a physical  attribute. For available periodic table attributes, see
        :py:meth:`~masci_tools.util.chemical_elements.ChemicalElements.list_of_attributes`. B) Colorize them by their
        group assignment within this instance. If there are no groups (i.e., flat not nested), then all present elements
        will have one color. If selected groups is None, will include all of the instance's groups.

        The numeric value to display below each element is controlled via the 'attribute' parameter. Apart from
        physical attributes, group names can also be chosen to be displayed, if they are numeric (not numeric strings).
        To do that, set the same value (argument) for the 'attribute' and 'title' parameters.

        If the group names are not numeric, but you want to display them nonetheless, you can still do so by setting
        the 'with_legend' attribute to True.

        For available colormap names, see:

        - https://seaborn.pydata.org/tutorial/color_palettes.html
        - https://matplotlib.org/stable/tutorials/colors/colormaps.html

        :param selected_groups: If flat and not specified, use all elements in flat elmts, else if nested, a group subset.
        :param title: Title to appear above the periodic table.
        :param colorby: 'group': Colormap by selected groups, 'attribute': by mendeleev periodic table attribute.
        :param attribute: Attribute's value displayed below elements. Either PTE attribute, or group values.
        :param missing_value: Replaces NaN values, e.g. for custom coloring.
        :type missing_value: str or numeric. Prefer same type as coloring input (group names or attribute).
        :param missing_color: Hex code of the color to be used for the missing values (#ffffff white, #bfbfbf light gray).
        :param missing_name: Name to be used for missing values in the legend. If empty, will use missing_value.
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
        import copy

        _title = title
        _output = output
        _legend_title = legend_title
        _missing_value = missing_value
        _missing_name = missing_name
        _missing_color = missing_color
        _colorby = colorby
        _attribute = attribute
        _colormap_name = colormap_name
        _colormap = copy.copy(colormap)
        _size = size
        _showfblock = showfblock
        _long_version = long_version
        _with_legend = with_legend

        if use_plotting_profile:
            if not self.plotting_profile:
                print('Warning: no plotting profile set. I will fall back to method arguments.')
            else:
                pp = self.plotting_profile
                # assert isinstance(pp, ChemicalElementsPlottingProfile) # for autocompletion
                _title = pp.title_prefix + title if (pp.title_prefix) else title
                _output = pp.output_prefix + output if (output and pp.output_prefix) else output
                _legend_title = pp.legend_title_prefix + legend_title if (legend_title and
                                                                          pp.legend_title_prefix) else legend_title
                _missing_value = pp.missing_value if pp.missing_value else missing_value
                _missing_name = pp.missing_name if pp.missing_name else missing_name
                _missing_color = pp.missing_color if pp.missing_color else missing_color
                _colorby = pp.colorby if pp.colorby else colorby
                _attribute = pp.attribute if pp.attribute else attribute
                _colormap_name = pp.colormap_name if pp.colormap_name else colormap_name
                _colormap = copy.copy(pp.colormap) if pp.colormap else _colormap
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

        # imports
        import matplotlib.colors
        import seaborn as sns
        import bokeh.plotting
        import mendeleev.plotting
        import numbers

        # init output for notebook. if not notebook, this won't have any effect.
        bokeh.plotting.output_notebook()

        _output_mendel = _output
        _output_ext = '.html'
        if _output_mendel:
            msg_suffix = ''
            if not _output_mendel.endswith(_output_ext):
                _output_mendel = _output_mendel + _output_ext
                msg_suffix = f"Info: filepath did not end in extension '{_output_ext}'. Appended it."
            print(f'Will write HTML table plot to file {_output_mendel}. {msg_suffix}')
            bokeh.plotting.output_file(filename=_output_mendel)

        # declare inner variables as arguments for mendeleev plot parameters
        _colorby_mendel, _attribute_mendel = f'{_title}_color', None

        # get instance's elements, nested or flat
        groups = self.select_groups(selected_groups, include_special_elements=False)

        # get the periodic table dataframe
        ptable = self._get_mendeleev_periodic_table()

        # check some conditionals
        is_missing_value_numeric = isinstance(_missing_value, numbers.Number)

        def _create_column_from_groups():
            for group_key, group in groups.items():
                for symbol in group.keys():
                    ptable.loc[ptable['symbol'] == symbol, [_title]] = group_key

        def _deal_with_missing_values(_missing_value) -> bool:
            """Deal with missing values.

            :return: True: filled in missing value, False: not.
            """
            fill_in = False

            is_numeric = all(isinstance(item, numbers.Number) for item in ptable[_title].to_list())

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

        values = sorted(ptable[_title].dropna().unique())
        filled_in, _missing_value = _deal_with_missing_values(_missing_value)

        # # let pandas convert values to most sensible types
        # # Example use case: when group names are integer, legend would display them as floats without this.
        # ptable[title] = ptable[title].convert_dtypes()
        # DEVnote: Commented out, cause this also converts NaN into pandas.NA, and mendeleev ploting method
        # can't deal with the latter. And seems like legend int problem above solved itself without this.

        # for the title column, either use specified colormap, or create custom one from given name
        if _colormap:
            # check if colormap can cover item values. must be a superset or true superset.
            if not all(val in _colormap.keys() for val in values):
                _standard_colormap_name = 'RdBu_r'
                print('Warning: Specified colormap does not cover all values to be colorized. '
                      f"Will fall back to mendeleev standard colormap '{_standard_colormap_name}'."
                      f'\nSpecified Colormap: {_colormap_name}'
                      f'\nValues to be colorized: {values}')
                _colormap_name = _standard_colormap_name
        else:
            # create custom colormpa from gien name
            _colormap = {
                key: matplotlib.colors.rgb2hex(rgb)
                for key, rgb in zip(values, sns.color_palette(palette=_colormap_name, n_colors=len(values)))
            }

        if filled_in:
            if _missing_color in _colormap.values():
                print(f"Warning: Specified missing color value '{_missing_color}' overwrites existing "
                      f'color value. Better choose another one.')
            _colormap[_missing_value] = _missing_color

        # add custom colormap column
        ptable[_colorby_mendel] = ptable[_title].map(_colormap)

        if with_legend:
            # for the legend color map, we want to use the missing_name instead of the missing_value,
            # and put it first. So, got to repopultate the custom colormap.
            if filled_in:
                _missing_name_inner = _missing_name if _missing_name else _missing_value
                # prepend missing name to dict
                _colormap.pop(_missing_value)
                cmap_copy = copy.copy(_colormap)
                _colormap = {_missing_name_inner: _missing_color}
                for key, hexcolor in cmap_copy.items():
                    _colormap[key] = hexcolor

            # _legend_title = legend_title if legend_title else title
            _legend_title_inner = _legend_title
            if not _legend_title_inner or _legend_title_inner == 'Legend':
                _legend_title_inner = _legend_title_inner + f' (attribute: {_attribute_mendel})'
            legend_figure = _plot_methods.plot_colortable(colors=_colormap,
                                                          title=_legend_title_inner,
                                                          sort_colors=False)

            # save legend figure if specified
            if _output_mendel:
                import os
                import matplotlib.pyplot as plt
                _output_legend = os.path.splitext(_output_mendel)
                _output_legend = _output_legend[0] + '_legend'
                plt.savefig(_output_legend)

        # finally, draw the plot(s)
        mendeleev.plotting.periodic_plot(df=ptable,
                                         attribute=_attribute_mendel,
                                         title=_title,
                                         width=_size[0],
                                         height=_size[1],
                                         missing=_missing_color,
                                         colorby=_colorby_mendel,
                                         output=_output_mendel,
                                         showfblock=showfblock,
                                         long_version=long_version)
        return legend_figure

    def _sort(self, a_dict, by_key=False):
        """Sorts chemical element dict by atomic number.

        :param a_dict: dict key = symbol str : value = atomic_number int
        :type a_dict: dict
        :param by_key: sort by key or value
        :type by_key: bool
        :return: sorted dict
        :rtype: dict
        """
        return dict(sorted(a_dict.items(), key=lambda item: item[not by_key]))

    def _validate(self, elements):
        """Checks that no non-valid elements are present.
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
        elif isinstance(elements, dict):
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
            else:
                raise TypeError('received a dict, but need chem.elmt. dict sym:num or num:sym')
        else:
            raise TypeError('Elements list is not any of list,tuple,set,dict.')

    def _chemical_element_list_to_dict(self, elements, sort=True):
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
        else:
            return a_dict


@_dc.dataclass
class PeriodicTable:
    """Periodic tables for different properties. Properties may be incomplete.

    Current properties: elemental crystal structure, agnetic elements.
    """
    from masci_tools.util import python_util

    table: ChemicalElements = python_util.dataclass_default_field(ChemicalElements())
    crystal: ChemicalElements = python_util.dataclass_default_field(
        ChemicalElements({
            'fcc': ['Ir', 'Pd', 'Pb', 'Pt', 'Al', 'Cu', 'Ca', 'Ag', 'Au', 'Sr', 'Mn', 'Ni'],
            'bcc': ['Ba', 'Cr', 'Cs', 'Fe', 'K', 'Mo', 'Nb', 'Rb', 'Ta', 'V', 'W'],
            'hcp': ['Be', 'Cd', 'Co', 'He', 'Hf', 'Mg', 'Os', 'Re', 'Ru', 'Sc', 'Tc', 'Ti', 'Tl', 'Y', 'Zn', 'Zr'],
            'diamond': ['Ge', 'Si', 'Sn'],
            'rhombohedral': ['As', 'Bi', 'Sb']
        }))
    magnet: ChemicalElements = python_util.dataclass_default_field(
        ChemicalElements({
            'ferromagnetic': ['Fe', 'Co', 'Ni'],
            'antiferromagnetic': ['Cr', 'Mn', 'O']
        }))
