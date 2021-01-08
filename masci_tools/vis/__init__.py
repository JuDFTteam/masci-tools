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
from functools import wraps


def ensure_plotter_consistency(plotter_object):
    """
    Decorator for plot functions to ensure that the
    Parameters are reset even if an error occurs in the function
    Additionally checks are performed that the parameters are reset after execution
    and the defaults are never changed in a plot function

    :param plotter_object: Plotter instance to be checked for consistency
    """

    assert isinstance(plotter_object, Plotter), 'The ensure_plotter_consistency should only be used for Plotter objects'

    def ensure_plotter_consistency_decorator(func):
        """
        Decorator that adds checks on the Plotter object
        """

        @wraps(func)
        def ensure_consistency(*args, **kwargs):
            """
            If an error is encountered in the decorated function the parameters
            of the plotter object are reset to avoid unintended sideeffects

            Also after execution the defaults and parameters are checked to make sure
            they are consistent
            """
            defaults_before = copy.deepcopy(plotter_object._current_defaults)

            try:
                res = func(*args, **kwargs)
            except Exception:
                plotter_object.reset_parameters()
                raise  #We do not want to erase the exception only wedge in the call to reset_parameters
            else:
                plotter_object.reset_parameters()

            if plotter_object._current_defaults != defaults_before:
                #Reset the changes
                plotter_object._current_defaults = defaults_before
                plotter_object.reset_parameters()
                raise ValueError(f"Defaults have changed inside the plotting function '{func.__name__}'")

            assert plotter_object._plot_parameters == plotter_object._current_defaults, \
                  f"Parameters are not consistent with defaults after call to '{func.__name__}'"

            return res

        return ensure_consistency

    return ensure_plotter_consistency_decorator


class Plotter(object):

    def __init__(self, default_parameters, list_arguments=None, **kwargs):

        self._PLOT_DEFAULTS = copy.deepcopy(default_parameters)
        self._current_defaults = copy.deepcopy(default_parameters)
        self._plot_parameters = copy.deepcopy(default_parameters)

        self._single_plot = True
        self._num_plots = 1

        if list_arguments is not None:
            self._LIST_ARGS = list_arguments

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

    def _setkey(self, key, value, dict_to_change, force=False):

        if key not in dict_to_change and not force:
            raise KeyError(f'The key {key} is not a parameter key')
        elif key not in dict_to_change:
            dict_to_change[key] = None

        if isinstance(value, dict) and all([isinstance(key, int) for key in value]):
            if self.single_plot:
                raise ValueError(f"Got dict with integer indices for key '{key}' but only a single plot is allowed")
            #Convert to list with defaults for not specified keys
            value = [value[indx] if indx in value else None for indx in range(self.num_plots)]
        if isinstance(value, list) and key not in self._LIST_ARGS:
            if self.single_plot:
                raise ValueError(f"Got list for key '{key}' but only a single plot is allowed")

            if not self.single_plot and self.num_plots == 1:
                value = [value]
            if len(value) != self.num_plots:
                value = value.copy() + [None] * (self.num_plots - len(value))
            value = [val if val is not None else self._current_defaults[key] for val in value]

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
                self._setkey(key, value, self._current_defaults, force=kwargs.get('force', False))
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
                self._setkey(key, value, self._plot_parameters, force=kwargs.get('force', False))
            except KeyError:
                if not continue_on_error:
                    self._plot_parameters = params_before
                    raise

    def add_parameter(self, name, default_from=None):

        default_val = None
        if default_from is not None:
            default_val = self._current_defaults[default_from]
            if isinstance(default_val, (dict, list)):
                default_val = copy.deepcopy(default_val)

        self._setkey(name, default_val, self._plot_parameters, force=True)

    def reset_defaults(self):
        assert self._plot_parameters == self._current_defaults, \
               'Changing the defaults will reset changes to the current parameters'
        assert self.single_plot, 'Changing the defaults will reset changes to single_plot property'
        assert self.num_plots == 1, 'Changing the defaults will reset changes to num_plots property'

        self._current_defaults = copy.deepcopy(self._PLOT_DEFAULTS)
        self._plot_parameters = copy.deepcopy(self._current_defaults)

    def reset_parameters(self):
        self._plot_parameters = copy.deepcopy(self._current_defaults)
        #Reset number of plots properties
        self.single_plot = True
        self.num_plots = 1

    def get_dict(self):
        return self._plot_parameters

    @property
    def single_plot(self):
        """
        Boolean property if True only a single Plot parameter set is allowed
        """
        return self._single_plot

    @single_plot.setter
    def single_plot(self, boolean_value):
        """
        Setter for single_plot property
        """
        self._single_plot = boolean_value

    @property
    def num_plots(self):
        """
        Integer property for number of plots produced
        """
        return self._num_plots

    @num_plots.setter
    def num_plots(self, int_value):
        """
        Setter for num_plots property
        """
        self._num_plots = int_value
