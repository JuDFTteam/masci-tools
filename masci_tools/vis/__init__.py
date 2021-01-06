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
Here are all plot varaiables/constants,

"""

import copy

class Plotter(object):

    def __init__(self, default_parameters, **kwargs):

        self._PLOT_DEFAULTS = copy.deepcopy(default_parameters)
        self._current_defaults = copy.deepcopy(default_parameters)

        if kwargs:
            self.set_defaults(continue_on_error=True, **kwargs)

        self._plot_parameters = copy.deepcopy(self._current_defaults)

    def __getitem__(self, indices):
        if isinstance(indices, tuple):
            if len(indices) != 2:
                raise ValueError('Only Key or (Key, Index) Indexing supported!')
            key, index = indices
        else:
            key = indices
            index = None

        try:
            value = self._plot_parameters[key]
            if isinstance(value, list):
                if index is None:
                    return value
                if index < len(value):
                    return value[index]
                else:
                    return value[0]
            else:
                return value
        except KeyError:
            return None

    @staticmethod
    def _setkey(key, value, dict_to_change, force=False):
        if key not in dict_to_change:
            raise KeyError(f'The key {key} is not a parameter key')

        if isinstance(dict_to_change[key], dict):
            if not isinstance(value, dict):
                if not force:
                    raise ValueError(f"Expected a dict for key {key} got '{value}'")
                dict_to_change[key] = value
            else:
                dict_to_change[key].update(value)
        else:
            dict_to_change[key] = value

    def __setitem__(self, key, value):
        self._setkey(key, value, self._plot_parameters)

    def set_defaults(self, continue_on_error=False, **kwargs):
        for key, value in kwargs.items():
            try:
                self._setkey(key, value, self._current_defaults, force=kwargs.get('force',False))
            except KeyError:
                if not continue_on_error:
                    raise

    def set_parameters(self, continue_on_error=False, **kwargs):
        for key, value in kwargs.items():
            try:
                self._setkey(key, value, self._plot_parameters, force=kwargs.get('force',False))
            except KeyError:
                if not continue_on_error:
                    raise

    def reset_defaults(self):
        self._current_defaults = copy.deepcopy(self._PLOT_DEFAULTS)

    def reset_parameters(self):
        self._plot_parameters = copy.deepcopy(self._current_defaults)

    def get_dict(self):
        return self._plot_parameters

    def prepare_figure(self, *args, **kwargs):
        raise NotImplementedError

    def show_legend(self, *args, **kwargs):
        raise NotImplementedError

    def save_figure(self, *args, **kwargs):
        raise NotImplementedError
