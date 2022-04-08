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
and ensuring consistent values for these
"""
from __future__ import annotations

import copy
from functools import wraps
from contextlib import contextmanager
from collections import ChainMap
import warnings
import json

from typing import Any, Callable, Generator, TypeVar, cast, MutableMapping

from masci_tools.util.typing import FileLike


@contextmanager
def NestedPlotParameters(plotter_object: Plotter) -> Generator[None, None, None]:
    """
    Contextmanager for nested plot function calls
    Will reset function defaults and parameters to previous
    values after exiting

    :param plotter_object: Plotter instance
    """
    #pylint: disable=protected-access
    assert isinstance(plotter_object, Plotter), \
           'The NestedPlotParameters contextmanager should only be used for Plotter objects'

    function_defaults_before = copy.deepcopy(plotter_object._function_defaults)
    parameters_before = copy.deepcopy(plotter_object._given_parameters)
    single_plot_before = plotter_object.single_plot
    num_plots_before = plotter_object.num_plots

    try:
        yield
    finally:  #Also performed if exception is thrown??
        plotter_object._function_defaults = function_defaults_before
        plotter_object._given_parameters = parameters_before
        plotter_object.single_plot = single_plot_before
        plotter_object.num_plots = num_plots_before


F = TypeVar('F', bound=Callable[..., Any])
"""Generic Callable type"""


def ensure_plotter_consistency(plotter_object: Plotter) -> Callable[[F], F]:
    """
    Decorator for plot functions to ensure that the
    Parameters are reset even if an error occurs in the function
    Additionally checks are performed that the parameters are reset after execution
    and the defaults are never changed in a plot function

    :param plotter_object: Plotter instance to be checked for consistency
    """

    assert isinstance(plotter_object, Plotter), \
           'The ensure_plotter_consistency decorator should only be used for Plotter objects'

    def ensure_plotter_consistency_decorator(func: F) -> F:
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
            #pylint: disable=protected-access

            global_defaults_before = copy.deepcopy(plotter_object._user_defaults)

            try:
                res = func(*args, **kwargs)
            except Exception:
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()
                plotter_object._function_defaults = {}
                raise  #We do not want to erase the exception only wedge in the call to reset_parameters
            else:
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()
                plotter_object._function_defaults = {}

            if plotter_object._user_defaults != global_defaults_before:
                #Reset the changes
                plotter_object._user_defaults = global_defaults_before
                plotter_object.remove_added_parameters()
                plotter_object.reset_parameters()
                plotter_object._function_defaults = {}
                raise ValueError(f"Defaults have changed inside the plotting function '{func.__name__}'")

            return res

        return cast(F, ensure_consistency)

    return ensure_plotter_consistency_decorator


def _generate_plot_parameters_table(defaults: dict[str, Any], descriptions: dict[str, str]) -> str:
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
        descr = descr.replace('{',' ``{')
        descr = descr.replace('}','}`` ')

        table.extend([f'       * - ``{key}``',
                      f'         - {descr}'])

        if not isinstance(value, dict):
            table.append(f'         - {value}')
        else:
            string_value = [f"'{key}': '{val}'," if isinstance(val, str)
                            else f"'{key}': {val},"
                            for key, val in value.items()]
            if string_value:
                string_value[0] = '{' + string_value[0]
                string_value[-1] = string_value[-1].rstrip(',') + '}'
            else:
                string_value = ['{}']

            table.extend(['         - .. code-block::', ''] + \
                         [f'                {string}' for string in string_value])

    table.append('')
    #yapf: enable

    return '\n'.join(table)


class Plotter:
    """
    Base class for handling parameters for plotting methods. For different plotting backends
    a subclass can be created to represent the specific parameters of the backend.

    :param default_parameters: dict with hardcoded default parameters
    :param general_keys: set of str optional, defines parameters which are
                            not allowed to change for each entry in the plot data

    Kwargs in the __init__ method are forwarded to :py:func:`Plotter.set_defaults()`
    to change the current defaults away from the hardcoded parameters.

    The Plotter class creates a hierarchy of dictionaries for lookups on this object
    utilizing the `ChainMap` from the `collections` module.

    The hierarchy is as follows (First entries take precedence over later entries):
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

    def __init__(self,
                 default_parameters: dict[str, Any],
                 general_keys: set[str] | None = None,
                 key_descriptions: dict[str, str] | None = None,
                 type_kwargs_mapping: dict[str, set[str]] | None = None,
                 kwargs_postprocess_rename: dict[str, str] | None = None,
                 **kwargs: Any) -> None:

        self._PLOT_DEFAULTS = copy.deepcopy(default_parameters)

        self._type_kwargs_mapping = {}
        if type_kwargs_mapping is not None:
            self._type_kwargs_mapping = type_kwargs_mapping

        self._kwargs_postprocess_rename = {}
        if kwargs_postprocess_rename is not None:
            self._kwargs_postprocess_rename = kwargs_postprocess_rename

        #ChainMap with three dictionaries on top
        # 1. function parameters
        # 2. global defaults
        # 3. function defaults
        # 4. Hardcoded defaults
        self._params: ChainMap[str, Any] = ChainMap({}, {}, {}, self._PLOT_DEFAULTS)

        self._single_plot = True
        self._num_plots = 1
        self._added_parameters: set[str] = set()

        self._GENERAL_KEYS = set()
        if general_keys is not None:
            self._GENERAL_KEYS = general_keys

        self._DESCRIPTIONS = {}
        if key_descriptions is not None:
            self._DESCRIPTIONS = key_descriptions

        if kwargs:
            self.set_defaults(continue_on_error=True, **kwargs)

    def __getitem__(self, indices: str | tuple[str, int]) -> Any:
        """
        Get the current value for the key

        :param indices: either str (specifies the key) or
                        tuple of str and int (specifies the key and index to access)

        :returns: the current parameter for the given specification. If tuple is given
                  and the parameter is a list the second item is used for the list index
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
            if key not in self._given_parameters:
                if isinstance(self._function_defaults.get(key), list):
                    value = self._function_defaults[key]
            if isinstance(value, list):
                if index is None:
                    return value
                if index < len(value):
                    return value[index]
                return value[0]
            return value
        except KeyError:
            return None

    def get_multiple_kwargs(self, keys: set[str], ignore: str | list[str] | None = None) -> dict[str, Any]:
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

    def plot_kwargs(self,
                    plot_type: str = 'default',
                    ignore: str | list[str] | None = None,
                    extra_keys: set[str] | None = None,
                    post_process: bool = True,
                    list_of_dicts: bool = True,
                    **kwargs: str) -> Any:
        """
        Creates a dict or list of dicts (for multiple plots) with the defined parameters
        for the plotting calls of different types

        :param plot_type: type of plot
        :param ignore: str or list of str (optional), defines keys to ignore in the creation of the dict
        :param extra_keys: optional set for additional keys to retrieve
        :param post_process: bool, if True the parameters are cleaned up for inserting them directly into bokeh plotting functions

        Kwargs are used to replace values by custom parameters:

        Example for using a custom markersize::

            p = Plotter(type_kwargs_mapping={'default': {'marker'}})
            p.add_parameter('marker_custom', default_from='marker')
            p.plot_kwargs(marker='marker_custom')

        This code snippet will return the standard parameters for a plot, but the value
        for the marker will be taken from the key `marker_custom`
        """

        if plot_type not in self._type_kwargs_mapping:
            raise ValueError(
                f'Unknown plot type {plot_type}. The following are known: {list(self._type_kwargs_mapping.keys())}')

        kwargs_keys = self._type_kwargs_mapping[plot_type]
        if extra_keys is not None:
            kwargs_keys = kwargs_keys | extra_keys

        #Insert custom keys to retrieve
        kwargs_keys = kwargs_keys.copy()
        for key, replace_key in kwargs.items():
            kwargs_keys.remove(key)
            kwargs_keys.add(replace_key)

        plot_kwargs = self.get_multiple_kwargs(kwargs_keys, ignore=ignore)

        #Rename replaced keys back to standard names
        for key, replace_key in kwargs.items():
            custom_val = plot_kwargs.pop(replace_key, None)
            if custom_val is not None:
                plot_kwargs[key] = custom_val

        if not post_process:
            return plot_kwargs

        for old, new in self._kwargs_postprocess_rename.items():
            if old in plot_kwargs:
                plot_kwargs[new] = plot_kwargs.pop(old)

        if list_of_dicts:
            plot_kwargs = self.dict_of_lists_to_list_of_dicts(plot_kwargs, self.single_plot,
                                                              self.num_plots)  #type:ignore[assignment]

        return plot_kwargs

    @staticmethod
    def dict_of_lists_to_list_of_dicts(dict_of_lists: dict[str, list[Any]],
                                       single_plot: bool,
                                       num_plots: int,
                                       repeat_after: int | None = None,
                                       ignore_repeat: set[str] | None = None) -> list[dict[str, Any]]:
        """
        Converts dict of lists and single values to list of length num_plots
        or single dict for single_plot=True

        :param dict_of_lists: dict to be converted
        :param single_plot: boolean, if True only a single parameter set is allowed
        :param num_plots: int of the number of allowed plots

        :returns: list of dicts
        """

        if ignore_repeat is None:
            ignore_repeat = set()

        any_list = any(isinstance(val, (list, tuple)) for val in dict_of_lists.values())

        #Make sure that every entry is actually a list
        if any_list:
            for key, val in dict_of_lists.items():
                if not isinstance(val, (list, tuple)):
                    dict_of_lists[key] = [val] * num_plots
        elif not single_plot:
            dict_of_lists = {key: [value] for key, value in dict_of_lists.items()}

        list_of_dicts: list[dict[str,
                                 Any]] = dict_of_lists  #type:ignore[assignment] # For single plot these are equivalent
        if not single_plot:
            list_of_dicts = []
            # enforce that all lists of the same lengths
            maxlen = max(map(len, dict_of_lists.values()))
            if repeat_after is not None:
                maxlen = max(num_plots, maxlen)
            for index in range(maxlen):
                tempdict = {}
                # don't use comprehension here, otherwise the wrong key is caught
                for key, value in dict_of_lists.items():
                    try:
                        if repeat_after is not None and index >= repeat_after and key not in ignore_repeat:
                            tempdict[key] = value[index % repeat_after]
                        else:
                            tempdict[key] = value[index]
                    except IndexError as ex:
                        raise IndexError(f'List under key: {key} index: {index} out of range, '
                                         f'should have length: {maxlen}. '
                                         'It may also be that some other list is just to long.') from ex
                list_of_dicts.append(tempdict)

            if len(list_of_dicts) != num_plots:
                if len(list_of_dicts) == 1:
                    list_of_dicts = [copy.deepcopy(list_of_dicts[0]) for i in range(num_plots)]
                else:
                    raise ValueError('Length does not match number of plots')

        return list_of_dicts

    @staticmethod
    def convert_to_complete_list(given_value: Any,
                                 single_plot: bool,
                                 num_plots: int,
                                 default: Any = None,
                                 key: str = '') -> Any:
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

            if isinstance(default, list):
                ret_value = [val if val is not None else default[indx] for indx, val in enumerate(ret_value)]
            else:
                ret_value = [val if val is not None else default for val in ret_value]

        return ret_value

    def expand_parameters(self, original_length: int, **kwargs: Any) -> dict[str, Any]:
        """
        Expand parameters to a bigger number of plots.
        New length has to be a multiple of original length.
        Only lists of length <= orginal_length are expanded.
        Also expands function defaults

        :param orginal_length: int of the old length
        :param kwargs: arguments to expand

        :returns: expanded kwargs
        """
        if self.num_plots == original_length:
            return kwargs

        if self.num_plots % original_length != 0:
            raise ValueError(f"Cannot expand parameters from length '{original_length}' to '{self.num_plots}'")

        length_per_param = self.num_plots // original_length

        for key, val in kwargs.items():
            if self.is_general(key):
                continue

            if isinstance(val, list):
                if len(val) <= original_length:
                    new_val = []
                    for val_list in val:
                        new_val += [val_list] * length_per_param
                    kwargs[key] = new_val

        for key, val in self._function_defaults.items():
            if self.is_general(key):
                continue
            if isinstance(val, list):
                if len(val) == original_length:
                    new_val = []
                    for val_list in val:
                        new_val += [val_list] * length_per_param
                    self.set_single_default(key, new_val, default_type='function')

        return kwargs

    def set_single_default(self, key: str, value: Any, default_type: str = 'global') -> None:
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
            if not self.is_general(key):

                default_val = self._hardcoded_defaults.get(key)
                if key in self._user_defaults:
                    default_val = self._user_defaults[key]

                value = self.convert_to_complete_list(value,
                                                      self.single_plot,
                                                      self.num_plots,
                                                      default=default_val,
                                                      key=key)
            self.__update_map(self._params.parents.parents, key, value)

    def __setitem__(self, key: str, value: Any) -> None:
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

        if not self.is_general(key):
            value = self.convert_to_complete_list(value,
                                                  self.single_plot,
                                                  self.num_plots,
                                                  default=self._params.parents[key],
                                                  key=key)

        self.__update_map(self._params, key, value)

    @staticmethod
    def __update_map(map_to_change: MutableMapping[str, Any], key: str, value: Any) -> None:
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

    def set_defaults(self,
                     continue_on_error: bool = False,
                     default_type: str = 'global',
                     **kwargs: Any) -> dict[str, Any]:
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
            defaults_before = copy.deepcopy(self._user_defaults)
        elif default_type == 'function':
            defaults_before = copy.deepcopy(self._function_defaults)

        for key, value in kwargs.items():

            try:
                self.set_single_default(key, value, default_type=default_type)
                kwargs_unprocessed.pop(key)
            except KeyError as err:
                if not continue_on_error:
                    if default_type == 'global':
                        self._user_defaults = defaults_before
                    elif default_type == 'function':
                        self._function_defaults = defaults_before
                    raise KeyError(f'Unknown parameter: {key}') from err

        if 'extra_kwargs' in kwargs_unprocessed:
            extra_kwargs = kwargs_unprocessed.pop('extra_kwargs')
            kwargs_unprocessed.update(extra_kwargs)

        return kwargs_unprocessed

    def set_parameters(self, continue_on_error: bool = False, **kwargs: Any) -> dict[str, Any]:
        """
        Set the current parameters.

        :param continue_on_error: bool, if True unknown key are simply skipped and returned

        Kwargs are used to set the defaults.
        """
        params_before = copy.deepcopy(self._given_parameters)
        kwargs_unprocessed = copy.deepcopy(kwargs)

        for key, value in kwargs.items():
            try:
                self[key] = value
                kwargs_unprocessed.pop(key)
            except KeyError:
                if not continue_on_error:
                    self._given_parameters = params_before
                    raise

        if 'extra_kwargs' in kwargs_unprocessed:
            extra_kwargs = kwargs_unprocessed.pop('extra_kwargs')
            kwargs_unprocessed.update(extra_kwargs)

        return kwargs_unprocessed

    def add_parameter(self, name: str, default_from: str | None = None, default_val: Any = None) -> None:
        """
        Add a new parameter to the parameters dictionary.

        :param name: str name of the parameter
        :param default_from: str (optional), if given a entry is created in the current defaults
                             with the name and the default value of the key `default_from`

        """

        if default_val is not None:
            if default_from is not None:
                raise ValueError('Default value specified via default_val and default_from. Please choose one option')
        elif default_from is not None:
            default_val = self._params.parents[default_from]
            if isinstance(default_val, (dict, list)):
                default_val = copy.deepcopy(default_val)

        self._added_parameters.add(name)
        self._function_defaults[name] = default_val

    def save_defaults(self, filename: FileLike = 'plot_defaults.json', save_complete: bool = False) -> None:
        """
        Save the current defaults to a json file.

        :param filename: filename, where the defaults should be stored
        :param save_complete: bool if True not only the overwritten user defaults
                              but also the unmodified hardcoded defaults are stored
        """
        if save_complete:
            if self._function_defaults != {}:
                raise ValueError('Function defaults need to be empty before saving defaults')
            dict_to_save = dict(self._params.parents)
        else:
            dict_to_save = dict(self._user_defaults)

        with open(filename, 'w', encoding='utf-8') as file:  #type:ignore[arg-type]
            json.dump(dict_to_save, file, indent=4, sort_keys=True)

    def load_defaults(self, filename: FileLike = 'plot_defaults.json') -> None:
        """
        Load defaults from a json file.

        :param filename: filename,from  where the defaults should be taken
        """
        with open(filename, encoding='utf-8') as file:  #type:ignore[arg-type]
            param_dict = json.load(file)

        self.set_defaults(**param_dict)

    def remove_added_parameters(self) -> None:
        """
        Remove the parameters added via :py:func:`Plotter.add_parameter()`
        """

        for key in copy.deepcopy(self._added_parameters):
            self._function_defaults.pop(key, None)
            self._given_parameters.pop(key, None)

    def reset_defaults(self) -> None:
        """
        Resets the defaults to the hardcoded defaults in _PLOT_DEFAULTS.
        """
        self._params = ChainMap({}, {}, {}, self._PLOT_DEFAULTS)

    def reset_parameters(self) -> None:
        """
        Reset the parameters to the current defaults. The properties single_plot and num_plots
        are also set to default values
        """

        self._given_parameters = {}
        #Reset number of plots properties
        self.single_plot = True
        self.num_plots = 1

    def get_dict(self) -> dict[str, Any]:
        """
        Return the dictionary of the current defaults. For use of printing
        """
        return dict(self._params)

    def get_description(self, key: str) -> None:
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

    def is_general(self, key: str) -> bool:
        """
        Return, whether the key is general
        (meaning only related to the whole plots)

        :param key: str of the key to check

        :returns: bool, whether the key is general
        """
        return key in self._GENERAL_KEYS

    @property
    def _hardcoded_defaults(self) -> MutableMapping[str, Any]:
        """
        Alias for the lowest map in the _params ChainMap
        """
        return self._params.maps[3]

    @_hardcoded_defaults.setter
    def _hardcoded_defaults(self, dict_value: dict[str, Any]) -> None:
        """
        Setter for the _hardcoded_defaults property
        """
        self._params.maps[2] = dict_value

    @property
    def _function_defaults(self) -> MutableMapping[str, Any]:
        """
        Alias for the second lowest map in the _params ChainMap
        """
        return self._params.maps[2]

    @_function_defaults.setter
    def _function_defaults(self, dict_value: dict[str, Any]) -> None:
        """
        Setter for the _function_defaults property
        """
        self._params.maps[2] = dict_value

    @property
    def _user_defaults(self) -> MutableMapping[str, Any]:
        """
        Alias for the third lowest map in the _params ChainMap
        """
        return self._params.maps[1]

    @_user_defaults.setter
    def _user_defaults(self, dict_value: dict[str, Any]) -> None:
        """
        Setter for the _user_defaults property
        """
        self._params.maps[1] = dict_value

    @property
    def _given_parameters(self) -> MutableMapping[str, Any]:
        """
        Alias for the highest map in the _params ChainMap
        """
        return self._params.maps[0]

    @_given_parameters.setter
    def _given_parameters(self, dict_value: dict[str, Any]) -> None:
        """
        Setter for the _given_parameters property
        """
        self._params.maps[0] = dict_value

    @property
    def single_plot(self) -> bool:
        """
        Boolean property if True only a single Plot parameter set is allowed
        """
        return self._single_plot

    @single_plot.setter
    def single_plot(self, boolean_value: bool) -> None:
        """
        Setter for single_plot property
        """
        self._single_plot = boolean_value

    @property
    def num_plots(self) -> int:
        """
        Integer property for number of plots produced
        """
        return self._num_plots

    @num_plots.setter
    def num_plots(self, int_value: int) -> None:
        """
        Setter for num_plots property
        """
        self._num_plots = int_value
