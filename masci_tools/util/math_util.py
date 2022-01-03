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
"""Convenience tools only for mathematical operations (numpy etc.)."""

import typing as _typing

import numpy as _np


def set_zero_below_threshold(array: _np.ndarray,
                             threshold: float = None,
                             inplace: bool = True) -> _typing.Optional[_np.ndarray]:
    """Set array elements below threshold to zero.
    :param array: numpy array
    :param threshold: if None, use machine epsilon
    :param inplace: True: return None, False: return copy.
    """
    threshold = threshold or _np.finfo(float).eps
    if inplace:
        array[_np.abs(array) < threshold] = 0
    else:
        arr = _np.copy(array)
        arr[_np.abs(arr) < threshold] = 0
        return arr


def drop_values(array: _np.ndarray, *args, **kwargs) -> _np.ndarray:
    """Drop elements matching conditions (masks) from array, return cleaned array.

    All conditions are specified as 'masks', and concatenated with logical AND.

    Positional masks:

    - ``'zero'``: drop zeros.
    - ``'nan'``: drop NaN values.
    - ``'negative'``: drop negative values.
    - ``'positive'``: drop positive values.

    Keyword masks:

    - ``gt=number``: drop values ``x > number``.
    - ``ge=number``: drop values ``x >= number``.
    - ``lt=number``: drop values ``x < number``.
    - ``le=number``: drop values ``x <= number``.

    :param array: numpy array
    :param args:
    """

    masks = []
    positional = ['zero', 'nan', 'negative', 'positive']
    keyword = ['gt', 'ge', 'lt', 'le']

    unknown_positional = list(set(args) - set(positional))
    unknown_keyword = list(set(kwargs.keys()) - set(keyword))

    if unknown_positional:
        print(f'Skipping unknown positional arguments: {unknown_positional}')
    if unknown_keyword:
        print(f'Skipping unknown keyword arguments: {unknown_keyword}')

    if 'zero' in args:
        masks.append(array != 0)
    if 'negative' in args:
        masks.append(array >= 0)
    if 'positive' in args:
        masks.append(array <= 0)
    # 'positive', 'negative' also drop 'nan' values. but using 'positive' / 'negative' together with 'nan'
    # deactivates the former. so only apply 'nan' if they are not present.
    if 'negative' not in args and 'positive' not in args and 'nan' in args:
        masks.append(~_np.isnan(array))

    if 'gt' in kwargs:
        masks.append(array <= kwargs['gt'])
    if 'ge' in kwargs:
        masks.append(array < kwargs['ge'])
    if 'lt' in kwargs:
        masks.append(array >= kwargs['lt'])
    if 'le' in kwargs:
        masks.append(array > kwargs['le'])

    if not masks:
        return array
    if len(masks) == 1:
        return array[tuple(masks)]
    else:  # > 1
        return array[_np.logical_and(*masks)]
