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
from contextlib import contextmanager
from collections import ChainMap
import warnings


@contextmanager
def NestedPlotParameters(plotter_object):
    """
    Contextmanager for nested plot function calls
    Will reset function defaults and parameters to previous
    values after exiting

    :param plotter_object: Plotter instance
    """
    assert isinstance(plotter_object, Plotter), \
           'The NestedPlotParameters contextmanager should only be used for Plotter objects'

    function_defaults_before = copy.deepcopy(plotter_object._params.maps[2])
    parameters_before = copy.deepcopy(plotter_object._params.maps[0])

    try:
        yield
    finally:  #Also performed if exception is thrown??
        plotter_object._params.maps[2] = function_defaults_before
        plotter_object._params.maps[0] = parameters_before


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

            global_defaults_before = copy.deepcopy(plotter_object._params.maps[1])

            try:
                res = func(*args, **kwargs)
            except Exception:
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()
                plotter_object._params.maps[2] = {}
                raise  #We do not want to erase the exception only wedge in the call to reset_parameters
            else:
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()
                plotter_object._params.maps[2] = {}

            if plotter_object._params.maps[1] != global_defaults_before:
                #Reset the changes
                plotter_object._params.maps[1] = global_defaults_before
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()
                plotter_object._params.maps[2] = {}
                raise ValueError(f"Defaults have changed inside the plotting function '{func.__name__}'")

            return res

        return ensure_consistency

    return ensure_plotter_consistency_decorator


def _generate_plot_parameters_table(defaults, descriptions):
    """
    Generate a table for the plotting parameters for the docstrings

    :param defaults: dict/chainmap with the defined defaults
    :param descriptions: dict with the description of the keys in defaults
    """

    #yapf: disable
    table = [
        '.. list-table:: Plot Parameters',
        '       :widths: 15 60 25',
        '       :header-rows: 1',
        '       :class: tight-table',
        '',
        '       * - Name',
        '         - Description',
        '         - Default value'
    ]

    for key, value in defaults.items():
        if value is None:
            value = 'No Default'
        elif not isinstance(value, dict):
            value = f'``{value}``'

        descr = descriptions.get(key, 'No Description available')

        table.extend([f'       * - ``{key}``',
                      f'         - {descr}',
                      f'         - {value}'])

    table.append('')
    #yapf: enable

    return '\n'.join(table)


class Plotter(object):
    """
    Base class for handling parameters for plotting methods. For different plotting backends
    a subclass can be created to represent the specific parameters of the backend.

    Args:
        :param default_parameters: dict with hardcoded default parameters
        :param general_keys: set of str optional, defines parameters which are
                             not allowed to change for each entry in the plot data

    Kwargs in the __init__ method are forwarded to :py:func:`Plotter.set_defaults()`
    to change the current defaults away from the hardcoded parameters.

    The Plotter class creates a hierachy of dictionaries for lookups on this object
    utilizing the `ChainMap` from the `collections` module.

    The hierachy is as follows (First entries take precedence over later entries):
        - `parameters`: set by :py:func:`~Plotter.set_parameters()` (usually arguments passed into function)
        - `user defaults`: set by :py:func:`~Plotter.set_defaults()`
        - `function defaults`: set by :py:func:`~Plotter.set_defaults()` with `default_type='function'`
        - `global defaults`: Hardcoded as fallback

    Only the `parameters` can represent parameters for multiple sets of plot calls.
    All others are used as fallback for specifying non-specified values for single plots

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

    def __init__(self, default_parameters, general_keys=None, key_descriptions=None, **kwargs):

        self._PLOT_DEFAULTS = copy.deepcopy(default_parameters)

        #ChainMap with three dictionaries on top
        # 1. function parameters
        # 2. global defaults
        # 3. function defaults
        # 4. Hardcoded defaults
        self._params = ChainMap({}, {}, {}, self._PLOT_DEFAULTS)

        self._single_plot = True
        self._num_plots = 1
        self._added_parameters = set()

        self._GENERAL_KEYS = set()
        if general_keys is not None:
            self._GENERAL_KEYS = general_keys

        self._DESCRIPTIONS = {}
        if key_descriptions is not None:
            self._DESCRIPTIONS = key_descriptions

        if kwargs:
            self.set_defaults(continue_on_error=True, **kwargs)

    def __getitem__(self, indices):
        """
        Get the current value for the key

        :param indices: either str (specifies the key) or
                        tuple of str and int (specifies the key and index to access)

        :returns: the current parameter for the given specification. If tuple is given
                  and the paramter is a list the second item is used for the list index
        """
        if isinstance(indices, tuple):
            if len(indices) != 2:
                raise ValueError('Only Key or (Key, Index) Indexing supported!')
            key, index = indices
        else:
            key = indices
            index = None

        try:
            value = self._params[key]
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
                keys_used.discard(key)

        ret_dict = {}
        for key in keys_used:
            if self[key] is not None:
                ret_dict[key] = self[key]

        return ret_dict

    @staticmethod
    def dict_of_lists_to_list_of_dicts(dict_of_lists, single_plot, num_plots):
        """
        Converts dict of lists and single values to list of length num_plots
        or single dict for single_plot=True

        :param dict_of_lists: dict to be converted
        :param single_plot: boolean, if True only a single parameter set is allowed
        :param num_plots: int of the number of allowed plots

        :returns: list of dicts
        """
        any_list = any(isinstance(val, (list, tuple)) for val in dict_of_lists.values())

        #Make sure that every entry is actually a list
        if any_list:
            for key, val in dict_of_lists.items():
                if not isinstance(val, (list, tuple)):
                    dict_of_lists[key] = [val] * num_plots
        elif not single_plot:
            dict_of_lists = {key: [value] for key, value in dict_of_lists.items()}

        list_of_dicts = dict_of_lists  #For single plot these are equivalent
        if not single_plot:
            list_of_dicts = [{key: value[index]
                              for key, value in dict_of_lists.items()}
                             for index in range(max(map(len, dict_of_lists.values())))]
            if len(list_of_dicts) != num_plots:
                if len(list_of_dicts) == 1:
                    list_of_dicts = [copy.deepcopy(list_of_dicts[0]) for i in range(num_plots)]
                else:
                    raise ValueError('Length does not match number of plots')

        return list_of_dicts

    @staticmethod
    def convert_to_complete_list(given_value, single_plot, num_plots, default=None, key=''):
        """
        Converts given value to list with length num_plots with None for the non-specified values

        :param given_value: value passed in, for multiple plots either list or dict with integer keys
        :param single_plot: bool, if True only a single parameter is allowed
        :param num_plots: int, if single_plot is False this defines the number of plots
        :param default: default value for unspecified entries
        :param key: str of the key to process
        """

        if not isinstance(given_value, dict) and not isinstance(given_value, list):
            return given_value

        ret_value = copy.copy(given_value)
        if isinstance(given_value, dict) and all(isinstance(key, int) for key in given_value):
            if single_plot:
                raise ValueError(f"Got dict with integer indices for '{key}' but only a single plot is allowed")
            #Convert to list with defaults for not specified keys
            ret_value = [ret_value[indx] if indx in ret_value else None for indx in range(num_plots)]

        if isinstance(ret_value, list):
            if single_plot:
                raise ValueError(f"Got list for key '{key}' but only a single plot is allowed")

            if len(ret_value) != num_plots:
                ret_value = ret_value.copy() + [None] * (num_plots - len(ret_value))
            ret_value = [val if val is not None else default for val in ret_value]

        return ret_value

    def set_single_default(self, key, value, default_type='global'):
        """
        Set default value for a single key/value pair

        :param key: str of the key to set
        :param value: value to set the key to
        :default_type: either 'global' or 'function'. Specifies, whether to
                       set the global defaults (not reset after function)
                       or the function defaults
        """
        if key not in self._params:
            raise KeyError(f'Unknown parameter: {key}')

        if default_type == 'global':
            self.__update_map(self._params.parents, key, value)
        elif default_type == 'function':
            self.__update_map(self._params.parents.parents, key, value)

    def __setitem__(self, key, value):
        """
        Set the given key value pair on the `Plotter._params` ChainMap
        (Always to the top layer).

        Unknown keys are forbidden.
        Keys allowed for multiple plot sets are converted to complete
        lists

        :param key: key to update
        :param value: value to use for updating
        """

        if key not in self._params:
            raise KeyError(f'Unknown parameter: {key}')

        if key not in self._GENERAL_KEYS:
            value = self.convert_to_complete_list(value,
                                                  self.single_plot,
                                                  self.num_plots,
                                                  default=self._params.parents[key],
                                                  key=key)

        self.__update_map(self._params, key, value)

    @staticmethod
    def __update_map(map_to_change, key, value):
        """
        Updates the given map with the given key value pair
        If the value is a dict it will be merged

        :param map_to_change: Mapping to change
        :param key: key to change
        :param value: value for updating the key

        """
        if isinstance(map_to_change[key], dict):
            dict_before = copy.deepcopy(map_to_change[key])
            if not isinstance(value, dict):
                if isinstance(value, list):
                    map_to_change[key] = dict_before
                else:
                    raise ValueError(f"Expected a dict for key {key} got '{value}'")
            else:
                dict_before.update(value)
                map_to_change[key] = dict_before
        else:
            map_to_change[key] = value

    def set_defaults(self, continue_on_error=False, default_type='global', **kwargs):
        """
        Set the current defaults. This method will only work if the parameters
        are not changed from the defaults. Otherwise a error is raised. This is because
        after changing the defaults the changes will be propagated to the parameters to ensure
        consistency.

        :param continue_on_error: bool, if True unknown key are simply skipped
        :default_type: either 'global' or 'function'. Specifies, whether to
                       set the global defaults (not reset after function)
                       or the function defaults

        Kwargs are used to set the defaults.
        """

        kwargs_unprocessed = copy.deepcopy(kwargs)
        if default_type == 'global':
            defaults_before = copy.deepcopy(self._params.maps[1])
        elif default_type == 'function':
            defaults_before = copy.deepcopy(self._params.maps[2])

        for key, value in kwargs.items():

            try:
                self.set_single_default(key, value, default_type=default_type)
                kwargs_unprocessed.pop(key)
            except KeyError as err:
                if not continue_on_error:
                    if default_type == 'global':
                        self._params.maps[1] = defaults_before
                    elif default_type == 'function':
                        self._params.maps[2] = defaults_before
                    raise KeyError(f'Unknown parameter: {key}') from err

        if 'extra_kwargs' in kwargs_unprocessed:
            extra_kwargs = kwargs_unprocessed.pop('extra_kwargs')
            kwargs_unprocessed.update(extra_kwargs)

        return kwargs_unprocessed

    def set_parameters(self, continue_on_error=False, **kwargs):
        """
        Set the current parameters.

        :param continue_on_error: bool, if True unknown key are simply skipped and returned

        Kwargs are used to set the defaults.
        """
        params_before = copy.deepcopy(self._params.maps[0])
        kwargs_unprocessed = copy.deepcopy(kwargs)

        for key, value in kwargs.items():
            try:
                self[key] = value
                kwargs_unprocessed.pop(key)
            except KeyError:
                if not continue_on_error:
                    self._params.maps[0] = params_before
                    raise

        if 'extra_kwargs' in kwargs_unprocessed:
            extra_kwargs = kwargs_unprocessed.pop('extra_kwargs')
            kwargs_unprocessed.update(extra_kwargs)

        return kwargs_unprocessed

    def add_parameter(self, name, default_from=None, default_val=None):
        """
        Add a new parameter to the parameters dictionary.

        :param name: str name of the parameter
        :param default_from: str (optional), if given a entry is created in the curent defaults
                             with the name and the default value of the key `default_from`

        """

        if default_val is not None:
            if default_from is not None:
                raise ValueError('Default value speciefied via default_val and default_from. Please choose one option')
        elif default_from is not None:
            default_val = self._params.parents[default_from]
            if isinstance(default_val, (dict, list)):
                default_val = copy.deepcopy(default_val)

        self._added_parameters.add(name)
        self._params.maps[2][name] = default_val

    def remove_added_parameters(self):
        """
        Remove the parameters added via :py:func:`Plotter.add_parameter()`
        """

        for key in copy.deepcopy(self._added_parameters):
            self._params.maps[2].pop(key, None)
            self._params.maps[0].pop(key, None)

    def reset_defaults(self):
        """
        Resets the defaults to the hardcoded defaults in _PLOT_DEFAULTS. Will check beforehand
        if the parameters or properties differ from the defaults and will raise an error if this
        is the case
        """
        self._params = ChainMap({}, {}, {}, self._PLOT_DEFAULTS)

    def reset_parameters(self):
        """
        Reset the parameters to the current defaults. The properties single_plot and num_plots
        are also set to default values
        """

        self._params.maps[0] = {}
        #Reset number of plots properties
        self.single_plot = True
        self.num_plots = 1

    def get_dict(self):
        """
        Return the dictionary of the current defaults. For use of printing
        """
        return dict(self._params)

    def get_description(self, key):
        """
        Get the description of the given key

        :param key: str of the key, for which the description should be printed
        """

        if key in self._DESCRIPTIONS:
            print(f'{key}:\n\n{self._DESCRIPTIONS[key]}')
        elif key in self._params:
            print(f'{key}:\n\nNo Description available')
        else:
            warnings.warn(f'{key} is not a known parameter')

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
