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
"""Convenience tools only for mathematical operations (numpy etc.)."""

import numpy as _np


def zero_below_eps(array: _np.ndarray):
    """Set array elements below machine epsilon to zero. In-place operation.
    :param array: numpy array
    """
    array[_np.abs(array) < _np.finfo(float).eps] = 0
