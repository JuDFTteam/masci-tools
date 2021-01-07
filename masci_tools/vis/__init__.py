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
        self._plot_parameters = copy.deepcopy(default_parameters)

        if kwargs:
            self.set_defaults(continue_on_error=True, **kwargs)

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
        if key not in dict_to_change and not force:
            raise KeyError(f'The key {key} is not a parameter key')
        elif key not in dict_to_change:
            dict_to_change[key] = None

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

        assert self._plot_parameters == self._current_defaults, \
               'Changing the defaults will reset changes to the current parameters'

        defaults_before = copy.deepcopy(self._current_defaults)
        for key, value in kwargs.items():
            try:
                self._setkey(key, value, self._current_defaults, force=kwargs.get('force',False))
            except KeyError:
                if not continue_on_error:
                    self._current_defaults = defaults_before
                    raise

        #Propagate changes to the parameters
        self._plot_parameters = copy.deepcopy(self._current_defaults)

    def set_parameters(self, continue_on_error=False, **kwargs):

        params_before = copy.deepcopy(self._plot_parameters)
        for key, value in kwargs.items():
            try:
                self._setkey(key, value, self._plot_parameters, force=kwargs.get('force',False))
            except KeyError:
                if not continue_on_error:
                    self._plot_parameters = params_before
                    raise

    def add_parameter(self, name, default_from=None):

        default_val = None
        if default_from is not None:
            default_val = self._current_defaults[default_from]
            if isinstance(default_val, dict) or isinstance(default_val, list):
                default_val = copy.deepcopy(default_val)

        self._setkey(name, default_val, self._plot_parameters, force=True)


    def reset_defaults(self):
        assert self._plot_parameters == self._current_defaults, \
               'Changing the defaults will reset changes to the current parameters'
        self._current_defaults = copy.deepcopy(self._PLOT_DEFAULTS)
        self._plot_parameters = copy.deepcopy(self._current_defaults)

    def reset_parameters(self):
        self._plot_parameters = copy.deepcopy(self._current_defaults)

    def get_dict(self):
        return self._plot_parameters

    def prepare_plot(self, *args, **kwargs):
        raise NotImplementedError

    def show_legend(self, *args, **kwargs):
        raise NotImplementedError

    def save_plot(self, *args, **kwargs):
        raise NotImplementedError
