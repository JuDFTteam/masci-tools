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


@contextmanager
def LockContainer(lock_object):
    """
    Contextmanager for temporarily locking a lockable object. Object is unfrozen
    when exiting with block

    :param lock_object: lockable container (not yet frzen)
    """

    assert isinstance(lock_object, (LockableDict, LockableList)), f'Wrong type Got: {lock_object.__class__}'

    assert not lock_object._locked, f'{lock_object.__class__.__name__} was already locked before entering the contextmanager'

    lock_object.freeze()

    try:
        yield
    finally:
        if isinstance(lock_object, LockableDict):
            lock_object._LockableDict__unfreeze()
        elif isinstance(lock_object, LockableList):
            lock_object._LockableList__unfreeze()


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

    def __init__(self, *args, recursive=True, **kwargs):
        self._locked = False
        self._recursive = recursive
        super().__init__(*args, **kwargs)

    def __check_lock(self):
        if self._locked:
            raise RuntimeError('Modification not allowed')

    def __delitem__(self, key):
        self.__check_lock()
        super().__delitem__(key)

    def __setitem__(self, key, value):
        self.__check_lock()
        if isinstance(value, list):
            super().__setitem__(key, LockableList(value, recursive=self._recursive))
        elif isinstance(value, dict):
            super().__setitem__(key, LockableDict(value, recursive=self._recursive))
        else:
            super().__setitem__(key, value)

    def freeze(self):
        """
        Freezes the object. This prevents further modifications
        """
        self.__freeze()

    def __freeze(self):

        if self._recursive:
            for key, val in self.items():
                if isinstance(val, LockableDict):
                    val.__freeze()
                elif isinstance(val, LockableList):
                    val._LockableList__freeze()

        self._locked = True

    def __unfreeze(self):

        if self._recursive:
            for key, val in self.items():
                if isinstance(val, LockableDict):
                    val.__unfreeze()
                elif isinstance(val, LockableList):
                    val._LockableList__unfreeze()

        self._locked = False

    def get_unlocked(self):
        """
        Get copy of object with builtin lists and dicts
        """
        if self._recursive:
            ret_dict = {}
            for key, value in self.items():
                if isinstance(value, LockableDict):
                    ret_dict[key] = value.get_unlocked()
                elif isinstance(value, LockableList):
                    ret_dict[key] = value.get_unlocked()
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

    def __init__(self, *args, recursive=True, **kwargs):
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

    def __check_lock(self):
        if self._locked:
            raise RuntimeError('Modification not allowed')

    def __delitem__(self, i):
        self.__check_lock()
        super().__delitem__(i)

    def __setitem__(self, i, item):
        self.__check_lock()
        if isinstance(item, list):
            super().__setitem__(i, LockableList(item, recursive=self._recursive))
        elif isinstance(item, dict):
            super().__setitem__(i, LockableDict(item, recursive=self._recursive))
        else:
            super().__setitem__(i, item)

    def __iadd__(self, other):
        self.__check_lock()
        return super().__iadd__(other)

    def __imul__(self, n):
        self.__check_lock()
        return super().__imul__(n)

    def append(self, item):
        self.__check_lock()
        super().append(item)

    def insert(self, i, item):
        self.__check_lock()
        super().insert(i, item)

    def pop(self, i=-1):
        """
        return the value at index i (default last) and remove it from list
        """
        self.__check_lock()
        super().pop(i=i)

    def remove(self, item):
        self.__check_lock()
        super().remove(item)

    def clear(self):
        """
        Clear the list
        """
        self.__check_lock()
        super().clear()

    def reverse(self):
        self.__check_lock()
        super().reverse()

    def sort(self, *args, **kwargs):
        self.__check_lock()
        super().sort(*args, **kwargs)

    def extend(self, other):
        self.__check_lock()
        super().extend(other)

    def freeze(self):
        """
        Freezes the object. This prevents further modifications
        """
        self.__freeze()

    def __freeze(self):

        if self._recursive:
            for val in self:
                if isinstance(val, LockableList):
                    val.__freeze()
                elif isinstance(val, LockableDict):
                    val._LockableDict__freeze()

        self._locked = True

    def __unfreeze(self):

        if self._recursive:
            for val in self:
                if isinstance(val, LockableList):
                    val.__unfreeze()
                elif isinstance(val, LockableDict):
                    val._LockableDict__unfreeze()
        self._locked = False

    def get_unlocked(self):
        """
        Get copy of object with builtin lists and dicts
        """
        if self._recursive:
            ret_list = []
            for value in self:
                if isinstance(value, LockableDict):
                    ret_list.append(value.get_unlocked())
                elif isinstance(value, LockableList):
                    ret_list.append(value.get_unlocked())
                else:
                    ret_list.append(value)
        else:
            ret_list = list(self)

        return ret_list
