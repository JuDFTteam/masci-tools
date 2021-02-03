# -*- coding: utf-8 -*-

from collections import UserDict, UserList


class LockableDict(UserDict):

    def __init__(self, *args, **kwargs):
        self._locked = False
        self._entered = False
        super().__init__(*args, **kwargs)

    def __check_lock(self):
        if self._locked:
            raise RuntimeError('Modification not allowed')

    def __enter__(self):
        if self._locked:
            raise RuntimeError(f'{self.__class__.__name__} was already locked before entering the contextmanager')
        self.__freeze()
        return self

    def __exit__(self, *args):
        self.__unfreeze()

    def __delitem__(self, key):
        self.__check_lock()
        super().__delitem__(key)

    def __setitem__(self, key, value):
        self.__check_lock()
        if isinstance(value, (dict, UserDict)):
            super().__setitem__(key, LockableDict(value))
        elif isinstance(value, (list, UserList)):
            super().__setitem__(key, LockableList(value))
        else:
            super().__setitem__(key, value)

    def freeze(self, recursive=True):
        self.__freeze(recursive=recursive)

    def __freeze(self, recursive=True):

        if recursive:
            for key, val in self.items():
                if isinstance(val, LockableDict):
                    val.__freeze(recursive=recursive)
                elif isinstance(val, LockableList):
                    val._LockableList__freeze(recursive=recursive)

        self._locked = True

    def __unfreeze(self, recursive=True):

        if recursive:
            for key, val in self.items():
                if isinstance(val, LockableDict):
                    val.__unfreeze(recursive=recursive)
                elif isinstance(val, LockableList):
                    val._LockableList__unfreeze(recursive=recursive)

        self._locked = False


    def get_unlocked(self, recursive=True):

        if recursive:
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

    def __init__(self, *args, **kwargs):
        self._locked = False
        super().__init__(*args, **kwargs)

    def __enter__(self):
        if self._locked:
            raise RuntimeError(f'{self.__class__.__name__} was already locked before entering the contextmanager')
        self.__freeze()
        return self

    def __exit__(self, *args):
        self.__unfreeze()

    def __check_lock(self):
        if self._locked:
            raise RuntimeError('Modification not allowed')

    def __delitem__(self):
        self.__check_lock()
        super().__delitem__()

    def __setitem__(self, i, item):
        self.__check_lock()
        if isinstance(item, (dict, UserDict)):
            super().__setitem__(i, LockableDict(item))
        elif isinstance(item, (list, UserList)):
            super().__setitem__(i, LockableList(item))
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
        self.__check_lock()
        super().pop(i=i)

    def clear(self):
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

    def freeze(self, recursive=True):
        self.__freeze(recursive=recursive)

    def __freeze(self, recursive=True):

        if recursive:
            for val in self:
                if isinstance(val, LockableList):
                    val.__freeze(recursive=recursive)
                elif isinstance(val, LockableDict):
                    val._LockableDict__freeze(recursive=recursive)

        self._locked = True

    def __unfreeze(self, recursive=True):

        if recursive:
            for val in self:
                if isinstance(val, LockableList):
                    val.__unfreeze(recursive=recursive)
                elif isinstance(val, LockableDict):
                    val._LockableDict__unfreeze(recursive=recursive)
        self._locked = False

    def get_unlocked(self, recursive=True):

        if recursive:
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
