# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
#                                                                             #
###############################################################################
"""
This module defines a small helper class to make case insensitive dictionary
lookups available naturally
"""
from collections import UserDict


class CaseInsensitiveDict(UserDict):
    """
    Dict with case insensitive lookup. Used in Schema dicts to make finding
    paths for tags and attributes easier.
    Does not preserve the case of the inserted key.
    Does not support case insensitive lookups in nested dicts

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
        Up till now only __contains__ is modified for case insensitivity so not all functionality will be as expected
        for full case insensitivity

    """

    def __new__(cls, iterable):
        return super().__new__(cls, [key.lower() for key in iterable])

    def __init__(self, iterable):
        self.__original_case = CaseInsensitiveDict()
        for key in iterable:
            if key not in self.__original_case:
                self.__original_case[key] = key
        super().__init__()

    def original_case(self, key):
        return self.__original_case[key]

    def __contains__(self, key):
        return super().__contains__(key.lower())

    def __repr__(self):
        """Returns the repr with the orinal case of the entered keys (first encounter)"""
        return f'{self.__class__.__name__}({self.__original_case.values()})'
