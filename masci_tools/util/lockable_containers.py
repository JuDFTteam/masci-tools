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
This module defines subclasses of UserDict and UserList to be able to prevent
unintended modifications
"""
from collections import UserDict, UserList
from contextlib import contextmanager

from typing import Union, Any, Generator, Iterable, cast


@contextmanager
def LockContainer(lock_object: Union['LockableList', 'LockableDict']) -> Generator:
    """
    Contextmanager for temporarily locking a lockable object. Object is unfrozen
    when exiting with block

    :param lock_object: lockable container (not yet frozen)
    """

    assert isinstance(lock_object, (LockableDict, LockableList)), f'Wrong type Got: {lock_object.__class__}'

    assert not lock_object.locked, f'{lock_object.__class__.__name__} was already locked before entering the contextmanager'

    lock_object.freeze()

    try:
        yield
    finally:
        lock_object._unfreeze()


class LockableDict(UserDict):
    """
    Subclass of UserDict, which can prevent modifications to itself.
    Raises `RuntimeError` if modification is attempted.

    Use :py:meth:`LockableDict.freeze()` to enforce. :py:meth:`LockableDict.get_unlocked()`
    returns a copy of the locked object with builtin lists and dicts

    :param recursive: bool if True (default) all subitems (lists or dicts) are converted into their
                      lockable counterparts

    All other args or kwargs will be passed on to initialize the `UserDict`

    IMPORTANT NOTE:
        This is not a direct subclass of dict. So isinstance(a, dict)
        will be False if a is an LockableDict

    """

    def __init__(self, *args: dict, recursive: bool = True, **kwargs: object) -> None:
        self._locked = False
        self._recursive = recursive
        super().__init__(*args, **kwargs)

    def __check_lock(self) -> None:
        if self.locked:
            raise RuntimeError('Modification not allowed')

    @property
    def locked(self) -> bool:
        """
        Returns whether the object is locked
        """
        return self._locked

    def __delitem__(self, key: object) -> None:
        self.__check_lock()
        super().__delitem__(key)

    def __setitem__(self, key: object, value: object):
        self.__check_lock()
        if isinstance(value, list):
            super().__setitem__(key, LockableList(value, recursive=self._recursive))
        elif isinstance(value, dict):
            super().__setitem__(key, LockableDict(value, recursive=self._recursive))
        else:
            super().__setitem__(key, value)

    def freeze(self) -> None:
        """
        Freezes the object. This prevents further modifications
        """
        if self._recursive:
            for key, val in self.items():
                if isinstance(val, (LockableDict, LockableList)):
                    val.freeze()

        self._locked = True

    def _unfreeze(self) -> None:

        if self._recursive:
            for key, val in self.items():
                if isinstance(val, (LockableList, LockableDict)):
                    val._unfreeze()

        self._locked = False

    def get_unlocked(self) -> dict:
        """
        Get copy of object with builtin lists and dicts
        """
        if self._recursive:
            ret_dict = {}
            for key, value in self.items():
                if isinstance(value, LockableDict):
                    ret_dict[key] = value.get_unlocked()
                elif isinstance(value, LockableList):
                    ret_dict[key] = cast(Any, value.get_unlocked())
                else:
                    ret_dict[key] = value
        else:
            ret_dict = dict(self)

        return ret_dict


class LockableList(UserList):
    """
    Subclass of UserList, which can prevent modifications to itself.
    Raises `RuntimeError` if modification is attempted.

    Use :py:meth:`LockableList.freeze()` to enforce. :py:meth:`LockableList.get_unlocked()`
    returns a copy of the locked object with builtin lists and dicts

    :param recursive: bool if True (default) all subitems (lists or dicts) are converted into their
                      lockable counterparts

    All other args or kwargs will be passed on to initialize the `UserList`

    IMPORTANT NOTE:
        This is not a direct subclass of list. So isinstance(a, list)
        will be False if a is an LockableList

    """

    def __init__(self, *args: Iterable[Any], recursive: bool = True, **kwargs: Iterable[Any]) -> None:
        self._locked = False
        self._recursive = recursive
        super().__init__(*args, **kwargs)
        if self._recursive:
            #Convert sublists and subdicts into Lockable counterparts (super__init__ just copies the values)
            for indx, item in enumerate(self):
                if isinstance(item, list):
                    super().__setitem__(indx, LockableList(item, recursive=self._recursive))
                elif isinstance(item, dict):
                    super().__setitem__(indx, LockableDict(item, recursive=self._recursive))

    def __check_lock(self) -> None:
        if self.locked:
            raise RuntimeError('Modification not allowed')

    @property
    def locked(self) -> bool:
        """
        Returns whether the object is locked
        """
        return self._locked

    def __delitem__(self, i: Union[int, slice]) -> None:
        self.__check_lock()
        super().__delitem__(i)

    def __setitem__(self, i: Union[int, slice], item: object) -> None:
        self.__check_lock()
        if isinstance(item, list):
            super().__setitem__(i, LockableList(item, recursive=self._recursive))
        elif isinstance(item, dict):
            super().__setitem__(i, LockableDict(item, recursive=self._recursive))
        else:
            super().__setitem__(i, item)  # type: ignore

    def __iadd__(self, other: Iterable[Any]) -> 'LockableList':
        self.__check_lock()
        return super().__iadd__(other)

    def __imul__(self, n: int) -> 'LockableList':
        self.__check_lock()
        return super().__imul__(n)

    def append(self, item: object) -> None:
        self.__check_lock()
        super().append(item)

    def insert(self, i: int, item: object) -> None:
        self.__check_lock()
        super().insert(i, item)

    def pop(self, i: int = -1) -> object:
        """
        return the value at index i (default last) and remove it from list
        """
        self.__check_lock()
        return super().pop(i=i)

    def remove(self, item: object) -> None:
        self.__check_lock()
        super().remove(item)

    def clear(self) -> None:
        """
        Clear the list
        """
        self.__check_lock()
        super().clear()

    def reverse(self) -> None:
        self.__check_lock()
        super().reverse()

    def sort(self, *args: object, **kwargs: object) -> None:
        self.__check_lock()
        super().sort(*args, **kwargs)

    def extend(self, other: Iterable[object]) -> None:
        self.__check_lock()
        super().extend(other)

    def freeze(self) -> None:
        """
        Freezes the object. This prevents further modifications
        """
        if self._recursive:
            for val in self:
                if isinstance(val, (LockableList, LockableDict)):
                    val.freeze()

        self._locked = True

    def _unfreeze(self) -> None:

        if self._recursive:
            for val in self:
                if isinstance(val, (LockableList, LockableDict)):
                    val._unfreeze()

        self._locked = False

    def get_unlocked(self) -> Iterable[Any]:
        """
        Get copy of object with builtin lists and dicts
        """
        if self._recursive:
            ret_list = []
            for value in self:
                if isinstance(value, LockableDict):
                    ret_list.append(cast(Any, value.get_unlocked()))
                elif isinstance(value, LockableList):
                    ret_list.append(value.get_unlocked())
                else:
                    ret_list.append(value)
        else:
            ret_list = list(self)

        return ret_list
