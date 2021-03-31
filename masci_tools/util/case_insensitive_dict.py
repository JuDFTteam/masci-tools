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
This module defines a small helper class to make case insensitive dictionary
lookups available naturally
"""
from masci_tools.util.lockable_containers import LockableDict
import pprint


class CaseInsensitiveDict(LockableDict):
    """
    Dict with case insensitive lookup. Used in Schema dicts to make finding
    paths for tags and attributes easier.
    Does not preserve the case of the inserted key.
    Does not support case insensitive lookups in nested dicts
    Subclass of :py:class:`masci_tools.util.lockable_containers.LockableDict`. So
    can be frozen via the`freeze()` method

    :param upper: bool if True the method `upper()` will be used instead of `lower()`
                  to normalize keys

    All other args or kwargs will be passed on to initialize the `UserDict`

    IMPORTANT NOTE:
        This is not a direct subcalss of dict. So isinstance(a, dict)
        will be False if a is an CaseInsensitiveDict

    """

    def __init__(self, *args, upper=False, **kwargs):
        self._upper = upper
        super().__init__(*args, **kwargs)

    def _norm_key(self, key):
        if self._upper:
            return key.upper()
        else:
            return key.lower()

    #Here we modify the methods needed to make the lookups case insensitive
    #Since we use UserDict these methods should be enough to modify all behaviour
    def __delitem__(self, key):
        super().__delitem__(self._norm_key(key))

    def __setitem__(self, key, value):
        super().__setitem__(self._norm_key(key), value)

    def __getitem__(self, key):
        return super().__getitem__(self._norm_key(key))

    def __contains__(self, key):
        return super().__contains__(self._norm_key(key))

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'


class CaseInsensitiveFrozenSet(frozenset):
    """
    Frozenset (i.e. immutable set) with case insensitive membership tests. Used in Schema dicts in `tag_info`
    entries to make flexible classification easy
    Preserves the case of the entered keys (`original_case()` returns the case of the first encounter)

    :param iterable: iterable only containing str

    Note:
        There might be subtle differences to expected behaviour with the methods
        __radd__, __ror__, and so on

    """

    def __new__(cls, iterable=None):
        if iterable is not None:
            return super().__new__(cls, [key.lower() for key in iterable])
        else:
            return super().__new__(cls, [])

    def __init__(self, iterable=None):
        if iterable is not None:
            self.original_case = self._get_new_original_case(iterable)
        else:
            self.original_case = {}
        self._frozenset_iter = None  #Used for customizing the iteration behaviour
        super().__init__()

    def _get_new_original_case(self, *iterables):
        new_dict = CaseInsensitiveDict()
        for iterable in iterables:
            for key in iterable:
                if key not in new_dict:
                    if isinstance(iterable, self.__class__):
                        new_dict[key] = iterable.original_case[key]
                    else:
                        new_dict[key] = key
        new_dict.freeze()
        return new_dict

    def __contains__(self, key):
        return super().__contains__(key.lower())

    def __repr__(self):
        """Returns the repr with the orinal case of the entered keys (first encounter)"""
        if self.original_case:
            return f'{self.__class__.__name__}({set(self.original_case.values())})'
        else:
            return f'{self.__class__.__name__}()'

    def __sub__(self, other):
        return self.difference(other)

    def __and__(self, other):
        return self.intersection(other)

    def __xor__(self, other):
        return self.symmetric_difference(other)

    def __or__(self, other):
        return self.union(other)

    def __eq__(self, other):
        return super().__eq__({key.lower() for key in other})

    def __ne__(self, other):
        return super().__ne__({key.lower() for key in other})

    def __iter__(self):
        self._frozenset_iter = super().__iter__()
        return self

    def __next__(self):
        try:
            return self.original_case[next(self._frozenset_iter)]
        except StopIteration:
            self._frozenset_iter = None
            raise

    def difference(self, *others):
        new_frozenset = super().difference(*[{key.lower() for key in other} for other in others])
        new_case_dict = self._get_new_original_case(self.original_case.values(), *others)
        return self.__class__({new_case_dict[key] for key in new_frozenset})

    def symmetric_difference(self, other):
        new_frozenset = super().symmetric_difference({key.lower() for key in other})
        new_case_dict = self._get_new_original_case(self.original_case.values(), other)
        return self.__class__({new_case_dict[key] for key in new_frozenset})

    def union(self, *others):
        new_frozenset = super().union(*[{key.lower() for key in other} for other in others])
        new_case_dict = self._get_new_original_case(self.original_case.values(), *others)
        return self.__class__({new_case_dict[key] for key in new_frozenset})

    def intersection(self, *others):
        new_frozenset = super().intersection(*[{key.lower() for key in other} for other in others])
        new_case_dict = self._get_new_original_case(self.original_case.values(), *others)
        return self.__class__({new_case_dict[key] for key in new_frozenset})

    def isdisjoint(self, other):
        return super().isdisjoint({key.lower() for key in other})

    def issubset(self, other):
        return super().issubset({key.lower() for key in other})

    def issuperset(self, other):
        return super().issuperset({key.lower() for key in other})


#Define custom pretty printers for these classes
#since pprint only support UserDict subclasses if they have no custom repr


def _pprint_case_insensitive_dict(self, object, stream, indent, allowance, context, level):  #pylint: disable=redefined-builtin
    """
    Modified from pprint dict https://github.com/python/cpython/blob/3.7/Lib/pprint.py#L194
    """
    cls = object.__class__
    stream.write(cls.__name__ + '(')
    self._pprint_dict(object, stream, indent + len(cls.__name__), allowance + 1, context, level)
    stream.write(')')


pprint.PrettyPrinter._dispatch[CaseInsensitiveDict.__repr__] = _pprint_case_insensitive_dict


def _pprint_case_insensitive_frozenset(self, object, stream, indent, allowance, context, level):  #pylint: disable=redefined-builtin
    """
    Modified from pprint dict https://github.com/python/cpython/blob/3.7/Lib/pprint.py#L194
    """
    cls = object.__class__
    stream.write(cls.__name__ + '(')
    if object:
        self._pprint_set(set(object.original_case.values()), stream, indent + len(cls.__name__), allowance + 1, context,
                         level)
    stream.write(')')


pprint.PrettyPrinter._dispatch[CaseInsensitiveFrozenSet.__repr__] = _pprint_case_insensitive_frozenset
