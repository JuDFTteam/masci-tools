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
from __future__ import annotations

from masci_tools.util.lockable_containers import LockableDict, LockableList
import pprint

from typing import Any, Iterable, Generator, TypeVar, FrozenSet, cast, AbstractSet

S = TypeVar('S')
""" Generic Type """
T_co = TypeVar('T_co', covariant=True)
""" Generic Type """
_S = TypeVar('_S')
""" Generic Type """


class CaseInsensitiveDict(LockableDict[S, T_co]):
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

    def __init__(self, *args: Any, upper: bool = False, recursive: bool = True, **kwargs: T_co):
        self._upper = upper
        super().__init__(*args, recursive=recursive, **kwargs)

    def _norm_key(self, key: _S) -> _S:
        if isinstance(key, str):
            if self._upper:
                return cast(_S, key.upper())
            return cast(_S, key.lower())
        return key

    #Here we modify the methods needed to make the lookups case insensitive
    #Since we use UserDict these methods should be enough to modify all behaviour
    def __delitem__(self, key: S) -> None:
        super().__delitem__(self._norm_key(key))

    def __setitem__(self, key: S, value: T_co | LockableDict[S, T_co] | LockableList[T_co]) -> None:
        super().__setitem__(self._norm_key(key), value)

    def __getitem__(self, key: S) -> T_co:
        return cast(T_co, super().__getitem__(self._norm_key(key)))

    def __contains__(self, key: object) -> bool:
        return super().__contains__(self._norm_key(key))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({super().__repr__()})'


class CaseInsensitiveFrozenSet(FrozenSet[T_co]):
    """
    Frozenset (i.e. immutable set) with case insensitive membership tests. Used in Schema dicts in `tag_info`
    entries to make flexible classification easy
    Preserves the case of the entered keys (`original_case()` returns the case of the first encounter)

    :param iterable: iterable only containing str

    Note:
        There might be subtle differences to expected behaviour with the methods
        __radd__, __ror__, and so on

    """

    def __new__(cls, iterable: Iterable[T_co] | None = None, upper: bool = False) -> CaseInsensitiveFrozenSet[T_co]:
        if iterable is not None:
            return super().__new__(cls, [cls.__norm_key(key, upper=upper) for key in iterable])  #type: ignore[misc]
        return super().__new__(cls, [])

    def __init__(self, iterable: Iterable[T_co] | None = None, upper: bool = False) -> None:
        self._upper = upper
        if iterable is not None:
            self.original_case = self._get_new_original_case(iterable)
        else:
            self.original_case = CaseInsensitiveDict(upper=self._upper)
        super().__init__()

    def _get_new_original_case(self, *iterables: Iterable[_S]) -> CaseInsensitiveDict[_S, _S]:
        new_dict: CaseInsensitiveDict[_S, _S] = CaseInsensitiveDict(upper=self._upper)
        for iterable in iterables:
            for key in iterable:
                if key not in new_dict:
                    if isinstance(iterable, self.__class__):
                        new_dict[key] = iterable.original_case[key]  #type: ignore[attr-defined]
                    else:
                        new_dict[key] = key
        new_dict.freeze()
        return new_dict

    def _norm_key(self, key: _S) -> _S:
        return self.__norm_key(key, upper=self._upper)

    @staticmethod
    def __norm_key(key: _S, upper: bool = False) -> _S:
        if isinstance(key, str):
            if upper:
                return cast(_S, key.upper())
            return cast(_S, key.lower())
        return key

    def __contains__(self, key: object) -> bool:
        return super().__contains__(self._norm_key(key))

    def __repr__(self) -> str:
        """Returns the repr with the orinal case of the entered keys (first encounter)"""
        if self.original_case:
            return f'{self.__class__.__name__}({set(self.original_case.values())})'
        return f'{self.__class__.__name__}()'

    def __sub__(self, other: AbstractSet[T_co]) -> CaseInsensitiveFrozenSet[T_co]:
        return self.difference(other)

    def __and__(self, other: AbstractSet[T_co]) -> CaseInsensitiveFrozenSet[T_co]:
        return self.intersection(other)

    def __xor__(self, other: AbstractSet[_S]) -> CaseInsensitiveFrozenSet[_S | T_co]:
        return self.symmetric_difference(other)  #type: ignore[arg-type]

    def __or__(self, other: AbstractSet[_S]) -> CaseInsensitiveFrozenSet[_S | T_co]:
        return self.union(other)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return super().__eq__({self._norm_key(key) for key in other})
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Iterable):
            return super().__ne__({self._norm_key(key) for key in other})
        return False

    def __iter__(self) -> Generator[T_co, None, None]:
        for item in super().__iter__():
            yield self.original_case[item]

    def difference(self, *others: Iterable[object]) -> CaseInsensitiveFrozenSet[T_co]:
        new_frozenset = super().difference(*[{self._norm_key(key) for key in other} for other in others])
        new_case_dict = self._get_new_original_case(self.original_case.values(), *others)
        return self.__class__({new_case_dict[key] for key in new_frozenset}, upper=self._upper)

    def symmetric_difference(self, other: Iterable[T_co]) -> CaseInsensitiveFrozenSet[T_co]:
        new_frozenset = super().symmetric_difference({self._norm_key(key) for key in other})
        new_case_dict = self._get_new_original_case(self.original_case.values(), other)
        return self.__class__({new_case_dict[key] for key in new_frozenset}, upper=self._upper)

    def union(self, *others: Iterable[_S]) -> CaseInsensitiveFrozenSet[T_co | _S]:
        new_frozenset = super().union(*[{self._norm_key(key) for key in other} for other in others])
        new_case_dict = self._get_new_original_case(self.original_case.values(), *others)
        return self.__class__({new_case_dict[key] for key in new_frozenset}, upper=self._upper)

    def intersection(self, *others: Iterable[object]) -> CaseInsensitiveFrozenSet[T_co]:
        new_frozenset = super().intersection(*[{self._norm_key(key) for key in other} for other in others])
        new_case_dict = self._get_new_original_case(self.original_case.values(), *others)
        return self.__class__({new_case_dict[key] for key in new_frozenset}, upper=self._upper)

    def isdisjoint(self, other: Iterable[T_co]) -> bool:
        return super().isdisjoint({self._norm_key(key) for key in other})

    def issubset(self, other: Iterable[object]) -> bool:
        return super().issubset({self._norm_key(key) for key in other})

    def issuperset(self, other: Iterable[object]) -> bool:
        return super().issuperset({self._norm_key(key) for key in other})


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


pprint.PrettyPrinter._dispatch[CaseInsensitiveDict.__repr__] = _pprint_case_insensitive_dict  #type: ignore


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


pprint.PrettyPrinter._dispatch[CaseInsensitiveFrozenSet.__repr__] = _pprint_case_insensitive_frozenset  #type: ignore
