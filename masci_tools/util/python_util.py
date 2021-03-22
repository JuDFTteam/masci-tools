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
"""Convenience tools only related to Python Standard Library."""

import copy
import typing
from dataclasses import field
import json
import re


def now():
    """Get now time localized to UTC."""
    from datetime import datetime
    import pytz
    return datetime.now(tz=pytz.UTC)
    # same as: pytz.UTC.localize(datetime.now())
    # not same as: datetime.now(tz=timezone.utc)


def random_string(length: int, ascii_uppercase: bool = True, ascii_lowercase: bool = True,
                  digits: bool = True, whitespace: bool = False) -> str:
    """Generate a random string of length.

    :param length: random string length.
    :param ascii_uppercase: True: include ASCII uppercase letters.
    :param ascii_lowercase: True: include ASCII lowercase letters.
    :param digits: True: include digits.
    :param whitespace: True: include whitespaces `\t\n\r\x0b\x0c`.
    :return: random string of length.
    """
    import string
    import random

    character_sets = {string.ascii_uppercase: ascii_uppercase,
                      string.ascii_lowercase: ascii_lowercase,
                      string.digits: digits,
                      string.whitespace: whitespace}
    population = ''.join([characters for characters, included in character_sets.items() if included])
    return ''.join(random.choices(population=population, k=length))


def enforce_minimum_python_version(minimum_version: tuple = (3, 7)):
    """For some operation requiring a minimum version, enforce for interpreter.

    :param minimum_version:
    :return: 0 if satisfied, sys.exit if not
    """
    import sys
    current_version = sys.version_info
    if current_version[0] == minimum_version[0] and current_version[1] >= minimum_version[1]:
        pass
    else:
        sys.stderr.write('[%s] - Error: Your Python interpreter must be %d.%d or greater (within major version %d)\n' %
                         (sys.argv[0], minimum_version[0], minimum_version[1], minimum_version[0]))
        sys.exit(-1)
    return 0


def flatten_list_of_lists(list_of_lists: list):
    return [item for sublist in list_of_lists for item in sublist]


def split_list(lst: list, n: int):
    """Yield n-sized chunks/batches from lst. Last chunk has remainder size.

    :param lst: list
    :param n: chunk size
    :return: split list (copy)
    :rtype: generator

    DEVNOTES:
    - equivalent list comprehension: [lst[i:i + n] for i in range(0, len(lst), n)]
    - as soon as a function contains 'yield', it always returns a generator. so cannot add a switch 'as_list'.
      But can just wrap the call inside list().
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def sort_lists_by_list(lists: typing.List[typing.List], key_list_index: int = 0, desc: bool = False):
    """Sort multiple lists by one list.

    The key_list gets sorted. The other lists get sorted in the same order.

    Reference: https://stackoverflow.com/a/15611016/8116031

    :param lists: list of lists to be sorted
    :param key_list_index: index of list in lists to sort by
    :param desc: False: ascending order
    :return: sorted lists
    """
    # note: two-liner equivalent:
    # line1: convert (zip(a,b,c,...)) lists into list of tuples, and
    #        sort elements of this list by key_list elements, i.e. key_list-th
    #        element in each tuple.
    # line2: unpack tuple list back into orignal, sorted, lists using
    #        nested list comprehensions and tuple unpacking.
    # sorted_lists = sorted(zip(*lists), reverse=desc, key=lambda x: x[key_list])
    # return [[x[i] for x in sorted_lists] for i in range(len(lists))]

    return zip(*sorted(zip(*lists), reverse=desc, key=lambda x: x[key_list_index]))


class NoIndent(object):
    """ Value wrapper. """

    def __init__(self, value):
        self.value = value


class JSONEncoderTailoredIndent(json.JSONEncoder):
    FORMAT_SPEC = '@@{}@@'
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))

    def __init__(self, **kwargs):
        """JSONEncoder which allows to not indent items wrapped in 'NoIndent()'.

        Reference: https://stackoverflow.com/a/13252112/8116031

        :param kwargs:
        :type kwargs:

        >>> from masci_tools.util.python_util import JSONEncoderTailoredIndent, NoIndent
        >>> import json
        >>> from string import ascii_lowercase as letters
        >>> data_structure = {
        >>>     'layer1': {
        >>>         'layer2': {
        >>>             'layer3_1': NoIndent([{"x":1,"y":7}, {"x":0,"y":4}, {"x":5,"y":3},
        >>>                                   {"x":6,"y":9},
        >>>                                   {k: v for v, k in enumerate(letters)}]),
        >>>             'layer3_2': 'string',
        >>>             'layer3_3': NoIndent([{"x":2,"y":8,"z":3}, {"x":1,"y":5,"z":4},
        >>>                                   {"x":6,"y":9,"z":8}]),
        >>>             'layer3_4': NoIndent(list(range(20))),
        >>>         }
        >>>     }
        >>> }
        >>> print(json.dumps(data_structure, cls=JSONEncoderTailoredIndent, sort_keys=True, indent=2))
        """
        # Save copy of any keyword argument values needed for use here.
        self.__sort_keys = kwargs.get('sort_keys', None)
        super(JSONEncoderTailoredIndent, self).__init__(**kwargs)

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent) else super(
            JSONEncoderTailoredIndent, self).default(obj))

    def encode(self, obj):
        from _ctypes import PyObj_FromPtr

        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(JSONEncoderTailoredIndent, self).encode(obj)  # Default JSON.

        # Replace any marked-up object ids in the JSON repr with the
        # value returned from the json.dumps() of the corresponding
        # wrapped Python object.
        for match in self.regex.finditer(json_repr):
            # see https://stackoverflow.com/a/15012814/355230
            id = int(match.group(1))
            no_indent = PyObj_FromPtr(id)
            json_obj_repr = json.dumps(no_indent.value, sort_keys=self.__sort_keys)

            # Replace the matched id string with json formatted representation
            # of the corresponding Python object.
            json_repr = json_repr.replace('"{}"'.format(format_spec.format(id)), json_obj_repr)

        return json_repr


def dataclass_default_field(obj: typing.Any, deepcopy=True) -> typing.Any:
    """Abbreviator for defining mutable types as default values for fields of dataclasses.
    References:
    - https://stackoverflow.com/a/53870411/8116031
    - https://docs.python.org/3/library/dataclasses.html#mutable-default-values

    Use case for this: the default value is some class instance. If you just write,
    in dataclass X, y : Y = dc.field(default=Y()), all x, x2, ... instances of X's
    variables x.y will be the same object / instance of Y. Whereas with this method, all
    x.y, x2.y, ... will be different objects / instances of Y (if deepcopy). Apart from that,
    this method allows you to also define a non-default instance of Y (ie, non-empty constructor)
    like Y(foo='bar').

    :param obj: complex / mutable default value
    :param deepcopy: default True: perform deepcopy, False: perform shallow copy.
    :return: dataclass field default value

    >>> import dataclasses as dc
    >>> from typing import Dict, Tuple
    >>> @dc.dataclass
    >>> class C:
    >>>     complex_attribute: Dict[str, Tuple[int, str]] = \
    >>>     dataclass_default_field({"a": (1, "x"), "b": (1, "y")})
    """
    if deepcopy:
        return field(default_factory=lambda: copy.deepcopy(obj))
    else:
        return field(default_factory=lambda: copy.copy(obj))


class SizeEstimator:

    def __init__(self):
        """Container for various python in-memory object size estimation methods.

        Estimating Python object size is not straightforward.

        There are many solutions available online. This is just a small referenced collection of them.
        """
        import sys, humanfriendly
        self.sys = sys
        self.hf = humanfriendly

        # Custom objects know their class.
        # Function objects seem to know way too much, including modules.
        # Exclude modules as well.
        from types import ModuleType, FunctionType
        self.BLACKLIST = type, ModuleType, FunctionType

    def sizeof_simple(self, object) -> tuple:
        """For simple PSL data structures. Reference: https://stackoverflow.com/a/19865746/8116031

        :return: tuple of bytesize, humanfriendly bytesize
        """
        size = self.sys.getsizeof(object)
        return size, self.hf.format_size(size)

    def sizeof_via_blacklist(self, object):
        """sum size of object & members. Reference: https://stackoverflow.com/a/30316760/8116031."""
        from gc import get_referents

        if isinstance(object, self.BLACKLIST):
            raise TypeError('getsize() does not take argument of type: ' + str(type(object)))
        seen_ids = set()
        size = 0
        objects = [object]
        while objects:
            need_referents = []
            for object in objects:
                if not isinstance(object, self.BLACKLIST) and id(object) not in seen_ids:
                    seen_ids.add(id(object))
                    size += self.sys.getsizeof(object)
                    need_referents.append(object)
            objects = get_referents(*need_referents)

        return size, self.hf.format_size(size)

    def sizeof_via_whitelist(self, object):
        """Recursively iterate to sum size of object & members.

        'gives much more fine-grained control over the types we're going to count for memory usage,
        but has the danger of leaving types out'

        Reference: https://stackoverflow.com/a/30316760/8116031.
        """
        from numbers import Number
        from collections import Set, Mapping, deque

        zero_depth_bases = (str, bytes, Number, range, bytearray)
        _seen_ids = set()

        def inner(obj):
            obj_id = id(obj)
            if obj_id in _seen_ids:
                return 0
            _seen_ids.add(obj_id)
            size = self.sys.getsizeof(obj)
            if isinstance(obj, zero_depth_bases):
                pass  # bypass remaining control flow and return
            elif isinstance(obj, (tuple, list, Set, deque)):
                size += sum(inner(i) for i in obj)
            elif isinstance(obj, Mapping) or hasattr(obj, 'items'):
                size += sum(inner(k) + inner(v) for k, v in getattr(obj, 'items')())
            # Check for custom object instances - may subclass above too
            if hasattr(obj, '__dict__'):
                size += inner(vars(obj))
            if hasattr(obj, '__slots__'):  # can have __slots__ with __dict__
                size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
            return size

        size = inner(object)
        return size, self.hf.format_size(size)
