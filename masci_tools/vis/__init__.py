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
Here basic functionality is provided for setting default parameters for plotting
and ensuring consitent values for these
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

    assert isinstance(plotter_object, Plotter), \
           'The ensure_plotter_consistency decorator should only be used for Plotter objects'

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
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()
                raise  #We do not want to erase the exception only wedge in the call to reset_parameters
            else:
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()

            if plotter_object._current_defaults != defaults_before:
                #Reset the changes
                plotter_object._current_defaults = defaults_before
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()
                raise ValueError(f"Defaults have changed inside the plotting function '{func.__name__}'")

            assert plotter_object._plot_parameters == plotter_object._current_defaults, \
                  f"Parameters are not consistent with defaults after call to '{func.__name__}'"

            return res

        return ensure_consistency

    return ensure_plotter_consistency_decorator


class Plotter(object):
    """
    Base class for handling parameters for plotting methods. For different plotting backends
    a subclass can be created to represent the specific parameters of the backend.

    Args:
        :param default_parameters: dict with hardcoded default parameters
        :param list_arguments: set of str optional, defines parameters which
                               can be lists for single plots

    Kwargs in the __init__ method are forwarded to :py:func:`Plotter.set_defaults()`
    to change the current defaults away from the hardcoded parameters.

    The Plotter class creates 3 copies of the given parameter dict:
        :param _PLOT_DEFAULTS: exact copy of the given parameter dict. Will never be changed
        :param _current_defaults: represents defaults with applied changes via :py:func:`Plotter.set_defaults()`.
                                  Always corresponds to a single parameter set
        :param _plot_parameters: based on _current_defaults, can be changed via :py:func:`Plotter.set_parameters()`
                                 and is the dict from where the actual used parameters are provided. Can also contain
                                 multiple parameter sets if the single_plot and num_plots properties were set before


    The current parameters can be accessed by bracket indexing the class. A example of this is shown below.

    .. code-block:: python

        parameter_dict = {'fontsize': 16, 'linestyle': '-'}

        params = Plotter(parameter_dict)

        #Accessing a parameter
        print(params['fontsize']) # 16

        #Modifying a parameter
        params['fontsize'] = 20
        print(params['fontsize']) # 20

        #Creating a parameter set for multiple plots

        #1. Set the properties to the correct values
        params.single_plot = False
        params.num_plots = 3

        #2. Now we can set a property either by providing a list or a integer indexed dict
        #   Both of the following examples set the linestyle of the second and third plot to '--'
        params['linestyle'] = [None, '--', '--']
        params['linestyle'] = {1: '--', 2: '--'}

        # Not specified values are replaced with the default value for a single plot
        print(params['linestyle']) # ['-', '--', '--']

        #In lists properties can also be indexed via tuples
        print(params[('linestyle', 0)]) # '-'
        print(params[('linestyle', 1)]) # '--'

        #Changes to the parameters and properties are reset
        params.reset_parameters()

        print(params['linestyle']) # '-'

    """

    def __init__(self, default_parameters, list_arguments=None, **kwargs):

        self._PLOT_DEFAULTS = copy.deepcopy(default_parameters)
        self._current_defaults = copy.deepcopy(default_parameters)
        self._plot_parameters = copy.deepcopy(default_parameters)

        self._single_plot = True
        self._num_plots = 1
        self._plot_type = 'default'
        self._added_parameters = set()

        self._LIST_ARGS = set()
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

    def get_multiple_kwargs(self, keys, ignore=None):
        """
        Get multiple parameters and return them in a dictionary

        :param keys: set of keys to process
        :param ignore: str or list of str (optional), defines keys to ignore in the creation of the dict
        """

        keys_used = copy.deepcopy(keys)

        if ignore is not None:
            if not isinstance(ignore, list):
                ignore = [ignore]
            for key in ignore:
                keys_used.remove(key)

        ret_dict = {}
        for key in keys_used:
            if self[key] is not None:
                ret_dict[key] = self[key]

        return ret_dict

    @staticmethod
    def convert_to_complete_list(given_value, single_plot, num_plots, list_allowed=False, default=None, key=''):
        """
        Converts given value to list with length num_plots with None for the non-specified values

        :param given_value: value passed in, for multiple plots either list or dict with integer keys
        :param single_plot: bool, if True only a single parameter is allowed
        :param num_plots: int, if single_plot is False this defines the number of plots
        """

        if not isinstance(given_value, dict) and not isinstance(given_value, list):
            return given_value

        ret_value = copy.copy(given_value)
        if isinstance(given_value, dict) and all([isinstance(key, int) for key in given_value]):
            if single_plot:
                raise ValueError(f"Got dict with integer indices for '{key}' but only a single plot is allowed")
            #Convert to list with defaults for not specified keys
            ret_value = [ret_value[indx] if indx in ret_value else None for indx in range(num_plots)]

        if isinstance(ret_value, list) and not list_allowed:
            if single_plot:
                raise ValueError(f"Got list for key '{key}' but only a single plot is allowed")

            if len(ret_value) != num_plots:
                ret_value = ret_value.copy() + [None] * (num_plots - len(ret_value))
            ret_value = [val if val is not None else default for val in ret_value]

        return ret_value

    def _setkey(self, key, value, dict_to_change, force=False):

        if key not in dict_to_change and not force:
            raise KeyError(f'The key {key} is not a parameter key')
        elif key not in dict_to_change:
            dict_to_change[key] = None
        value = self.convert_to_complete_list(value,
                                              self.single_plot,
                                              self.num_plots,
                                              list_allowed=key in self._LIST_ARGS,
                                              default=self._current_defaults[key],
                                              key=key)

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

    def set_defaults(self, continue_on_error=False, return_unprocessed_kwargs=False, **kwargs):
        """
        Set the current defaults. This method will only work if the parameters
        are not changed from the defaults. Otherwise a error is raised. This is because
        after changing the defaults the changes will be propagated to the parameters to ensure
        consistency.

        :param continue_on_error: bool, if True unknown key are simply skipped
        :param return_unprocessed_kwargs: bool, if True the unknown keys are returned

        Special Kwargs:
            :param force: bool, if True checks are skipped in setting the key

        Kwargs are used to set the defaults.
        """
        assert self._plot_parameters == self._current_defaults, \
               'Changing the defaults will reset changes to the current parameters'
        assert self.single_plot, 'Changing the defaults will reset changes to single_plot property'
        assert self.num_plots == 1, 'Changing the defaults will reset changes to num_plots property'

        kwargs_unprocessed = copy.deepcopy(kwargs)
        defaults_before = copy.deepcopy(self._current_defaults)
        force = kwargs.pop('force', False)
        for key, value in kwargs.items():
            try:
                self._setkey(key, value, self._current_defaults, force=force)
                kwargs_unprocessed.pop(key)
            except KeyError:
                if not continue_on_error:
                    self._current_defaults = defaults_before
                    raise

        #Propagate changes to the parameters
        self.reset_parameters()

        if 'extra_kwargs' in kwargs_unprocessed:
            extra_kwargs = kwargs_unprocessed.pop('extra_kwargs')
            kwargs_unprocessed.update(extra_kwargs)

        if return_unprocessed_kwargs:
            return kwargs_unprocessed

    def set_parameters(self, continue_on_error=False, return_unprocessed_kwargs=False, **kwargs):
        """
        Set the current parameters.

        :param continue_on_error: bool, if True unknown key are simply skipped
        :param return_unprocessed_kwargs: bool, if True the unknown keys are returned

        Special Kwargs:
            :param force: bool, if True checks are skipped in setting the key

        Kwargs are used to set the defaults.
        """
        params_before = copy.deepcopy(self._plot_parameters)
        force = kwargs.pop('force', False)

        kwargs_unprocessed = copy.deepcopy(kwargs)
        for key, value in kwargs.items():
            try:
                self._setkey(key, value, self._plot_parameters, force=force)
                kwargs_unprocessed.pop(key)
            except KeyError:
                if not continue_on_error:
                    self._plot_parameters = params_before
                    raise

        if 'extra_kwargs' in kwargs_unprocessed:
            extra_kwargs = kwargs_unprocessed.pop('extra_kwargs')
            kwargs_unprocessed.update(extra_kwargs)

        if return_unprocessed_kwargs:
            return kwargs_unprocessed

    def add_parameter(self, name, default_from=None):
        """
        Add a new parameter to the parameters dictionary.

        :param name: str name of the parameter
        :param default_from: str (optional), if given a entry is created in the curent defaults
                             with the name and the default value of the key `default_from`

        """
        default_val = None
        if default_from is not None:
            default_val = self._current_defaults[default_from]
            if isinstance(default_val, (dict, list)):
                default_val = copy.deepcopy(default_val)

        self._setkey(name, default_val, self._current_defaults, force=True)
        self._added_parameters.add(name)

        self._setkey(name, default_val, self._plot_parameters, force=True)

    def remove_added_parameters(self):
        """
        Remove the parameters added via :py:func:`Plotter.add_parameter()`
        """

        for key in copy.deepcopy(self._added_parameters):
            self._current_defaults.pop(key, None)
            self._plot_parameters.pop(key, None)
            self._added_parameters.remove(key)

    def reset_defaults(self):
        """
        Resets the defaults to the hardcoded defaults in _PLOT_DEFAULTS. Will check beforehand
        if the parameters or properties differ from the defaults and will raise an error if this
        is the case
        """
        assert self._plot_parameters == self._current_defaults, \
               'Changing the defaults will reset changes to the current parameters'
        assert self.single_plot, 'Changing the defaults will reset changes to single_plot property'
        assert self.num_plots == 1, 'Changing the defaults will reset changes to num_plots property'
        assert self.plot_type == 'default', 'Changing the defaults will reset changes to plot_type property'

        self._current_defaults = copy.deepcopy(self._PLOT_DEFAULTS)
        self._plot_parameters = copy.deepcopy(self._current_defaults)

    def reset_parameters(self):
        """
        Reset the parameters to the current defaults. The properties single_plot and num_plots
        are also set to default values
        """

        self._plot_parameters = copy.deepcopy(self._current_defaults)
        #Reset number of plots properties
        self.single_plot = True
        self.num_plots = 1
        self.plot_type = 'default'

    def get_dict(self):
        """
        Return the dictionary of the current defaults. For use of printing
        """
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

    @property
    def plot_type(self):
        """
        String property for the type of plotting function
        """
        return self._plot_type

    @plot_type.setter
    def plot_type(self, str_value):
        """
        Setter for plot_type property
        """
        self._plot_type = str_value
