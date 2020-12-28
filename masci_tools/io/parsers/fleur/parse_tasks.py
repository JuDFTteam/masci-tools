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
This module contains a class which organizes the known parsing tasks for outxml files
and provides fuctionality for adding custom tasks easily
"""
from pprint import pprint
from functools import wraps
import importlib.util
import copy
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TASK_FILE = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, 'default_parse_tasks.py'))


def register_migration(base_version, target_version):
    """
    Decorator to add migration for task defintion dictionary
    The function should only take tasks_defintion as an argument
    """

    def migration_decorator(func):
        """
        Return decorated ParseTasks object with _migrations dict attribute
        Here all registered migrations are inserted
        """

        @wraps(func)
        def migration(*args):
            """Decorator for migration function"""
            return func(*args)

        setattr(ParseTasks, func.__name__, migration)

        if not hasattr(ParseTasks, '_migrations'):
            ParseTasks._migrations = {}  # pylint: disable=protected-access
        if not base_version in ParseTasks._migrations:
            ParseTasks._migrations[base_version] = {}
        ParseTasks._migrations[base_version][target_version] = getattr(ParseTasks, func.__name__)  # pylint: disable=protected-access

        return migration

    return migration_decorator


def register_parsing_function(parse_type_name, all_attribs_keys=False):
    """
    Decorator to add parse type for task defintion dictionary
    The function should only take tasks_defintion as an argument
    """

    def parse_type_decorator(func):
        """
        Return decorated ParseTasks object with _parse_functions dict attribute
        Here all registered migrations are inserted
        """

        @wraps(func)
        def parse_type(*args, **kwargs):
            """Decorator for parse_type function"""
            return func(*args, **kwargs)

        setattr(ParseTasks, func.__name__, parse_type)

        if not hasattr(ParseTasks, '_parse_functions'):
            ParseTasks._parse_functions = {}  # pylint: disable=protected-access
            ParseTasks._all_attribs_function = set()

        ParseTasks._parse_functions[parse_type_name] = getattr(ParseTasks, func.__name__)  # pylint: disable=protected-access
        if all_attribs_keys:
            ParseTasks._all_attribs_function.add(parse_type_name)

        return parse_type

    return parse_type_decorator


class ParseTasks(object):
    """
    Representation of all known parsing tasks for the out.xml file

    When set up it will initialize the known default tasks and check if they work
    for the given output version

    Accesing definition of task example

    .. code-block:: python

        from masci_tools.io.parsers.fleur import ParseTasks

        p = ParseTasks('0.33')
        totE_definition = p.tasks['total_energy']
    """

    CONTROL_KEYS = {'_general', '_modes', '_minimal', '_special', '_conversions'}
    REQUIRED_KEYS = {'parse_type', 'path_spec'}
    ALLOWED_KEYS = {'parse_type', 'path_spec', 'subdict', 'overwrite_last'}
    ALLOWED_KEYS_ALLATTRIBS = {
        'parse_type', 'path_spec', 'subdict', 'base_value', 'ignore', 'overwrite', 'flat', 'only_required'
    }

    _version = '0.2.0'

    def __init__(self, version, task_file=None, validate_defaults=False):
        """
        Initialize the default parse tasks
        Terminates if the version is not marked as working with the default tasks

        TODO: We need some way of versioning for the default tasks
        """

        if task_file is None:
            task_file = DEFAULT_TASK_FILE

        #import task definitions
        spec = importlib.util.spec_from_file_location('tasks', task_file)
        tasks = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tasks)

        self._iteration_tasks = []
        self._general_tasks = []

        tasks_dict = copy.deepcopy(tasks.TASKS_DEFINITION)
        if validate_defaults:
            #Manually add each task to make sure that there are no typos/inconsitencies in the keys
            self.tasks = {}
            for task_name, task in tasks_dict.items():
                self.add_task(task_name, task)
        else:
            self.tasks = tasks_dict

        #Look if the base version is compatible if not look for a migration
        if version not in tasks.__working_out_versions__:
            if version in self._migrations['0.33']:
                self.tasks = self._migrations['0.33'][version](self.tasks)
            else:
                raise ValueError(f'Unsupported output version: {version}')

    @property
    def iteration_tasks(self):
        """
        Tasks to perform for each iteration
        """
        return self._iteration_tasks

    @property
    def general_tasks(self):
        """
        Tasks to perform for the root node
        """
        return self._general_tasks

    @iteration_tasks.setter
    def iteration_tasks(self, task_list):
        """
        Setter for iteration_tasks
        """
        self._iteration_tasks = task_list

    @general_tasks.setter
    def general_tasks(self, task_list):
        """
        Setter for general_tasks
        """
        self._general_tasks = task_list

    def add_task(self, task_name, task_definition, **kwargs):
        """
        Add a new task definition to the tasks dictionary

        Will first check if the definition has all the required keys

        :param task_name: str, key in the tasks dict
        :param task_definition: dict with the defined tasks
        :param overwrite: bool (optional), if True and the key is present in the dictionary it will be
                          overwritten with the new definition
        :param append: bool (optional), if True and the key is present in the dictionary the new defintions
                       will be inserted into this dictionary (inner keys WILL BE OVERWRITTEN). Additionally
                       if an inner key is overwritten with an empty dict the inner key will be removed

        The following keys are expected in each entry of the task_definition dictionary:
            :param parse_type: str, defines which methods to use when extracting the information
            :param path_spec: dict with all the arguments that should be passed to get_tag_xpath
                              or get_attrib_xpath to get the correct path
            :param subdict: str, if present the parsed values are put into this key in the output dictionary
            :param overwrite_last: bool, if True no list is inserted and each entry overwrites the last

        For the allAttribs parse_type there are more keys that can appear:
            :param base_value: str, optional. If given the attribute
                               with this name will be inserted into the key from the task_definition
                               all other keys are formatted as {task_key}_{attribute_name}
            :param ignore: list of str, these attributes will be ignored
            :param overwrite: list of str, these attributes will not create a list and overwrite any value
                              that might be there
            :param flat: bool, if False the dict parsed from the tag is inserted as a dict into the correspondin key
                               if True the values will be extracted and put into the output dictionary with the
                               format {task_key}_{attribute_name}

        """

        append = kwargs.get('append', False)
        overwrite = kwargs.get('overwrite', False)

        if task_name in self.tasks and not (append or overwrite):
            raise ValueError(f"Task '{task_name}' is already defined."
                             'Use append=True to append them (conflicting keys are overwritten)'
                             'or overwrite=True to remove all existing tasks')

        for task_key, definition in task_definition.items():

            if task_key.startswith('_'):
                if task_key not in self.CONTROL_KEYS:
                    raise ValueError(f'Unknown control key: {task_key}')
                continue

            task_keys = set(definition.keys())

            if not task_keys and task_key in self.tasks[task_name]:
                continue

            missing_required = self.REQUIRED_KEYS.difference(task_keys)
            if missing_required:
                raise ValueError(f'Reqired Keys missing: {missing_required}')

            if not definition['parse_type'] in self._parse_functions.keys():
                raise ValueError(f"Unknown parse_type: {definition['parse_type']}")

            if definition['parse_type'] in self._all_attribs_function:
                extra_keys = task_keys.difference(self.ALLOWED_KEYS_ALLATTRIBS)
            else:
                extra_keys = task_keys.difference(self.ALLOWED_KEYS)

            if extra_keys:
                raise ValueError(f'Got extra Keys: {extra_keys}')

        if append:
            if task_name not in self.tasks:
                self.tasks[task_name] = {}
            for task_key, definition in task_definition.items():
                if definition:
                    self.tasks[task_name][task_key] = definition
                elif task_key in self.tasks[task_name]:
                    self.tasks[task_name].pop(task_key)
        else:
            self.tasks[task_name] = task_definition

    def determine_tasks(self, fleurmodes, minimal=False):
        """
        Determine, which tasks to perform based on the fleur_modes

        :param fleurmodes: dict with the calculation modes
        :param minimal: bool, whether to inly perform minimal tasks
        """

        for task_name, definition in self.tasks.items():

            if task_name == 'fleur_modes':
                continue

            if minimal:
                task_minimal = definition.get('_minimal', False)
                if not task_minimal:
                    continue

            #These tasks are always added manually
            special = definition.get('_special', False)
            if special:
                continue

            mode_req = definition.get('_modes', [])

            check = [fleurmodes[mode] == required_value for mode, required_value in mode_req]

            if not all(check):
                continue

            general_task = definition.get('_general', False)

            if general_task:
                self._general_tasks.append(task_name)
            else:
                self._iteration_tasks.append(task_name)

    def perform_task(self,
                     task_name,
                     node,
                     out_dict,
                     schema_dict,
                     constants,
                     parser_info_out=None,
                     replace_root=None,
                     use_lists=True):
        """
        Evaluates the task given in the tasks_definition dict

        :param task_name: str, specifies the task to perform
        :param node: etree.Element, the xpath expressions are evaluated from this node
        :param out_dict: dict, output will be put in this dictionary
        :param schema_dict: dict, here all paths and attributes are stored according to the
                            outputschema
        :param constants: dict with all the defined mathematical constants
        :param parser_info_out: dict, with warnings, info, errors, ...
        :param root_tag: str, this string will be appended in front of any xpath before it is evaluated
        :param use_lists: bool, if True lists are created for each key if not otherwise specified

        """
        from masci_tools.io.common_functions import camel_to_snake
        import masci_tools.util.fleur_outxml_conversions as convert_funcs

        if parser_info_out is None:
            parser_info_out = {'parser_warnings': []}

        try:
            tasks_definition = self.tasks[task_name]
        except KeyError as exc:
            raise KeyError(f'Unknown Task: {task_name}') from exc

        for task_key, spec in tasks_definition.items():

            if task_key.startswith('_'):
                continue

            action = self._parse_functions[spec['parse_type']]

            args = spec['path_spec'].copy()
            args['constants'] = constants

            if replace_root is not None:
                args['replace_root'] = replace_root

            if 'only_required' in spec:
                args['only_required'] = spec['only_required']

            if spec['parse_type'] == 'singleValue':
                args['ignore'] = ['comment']
            elif spec['parse_type'] in ['allAttribs', 'parentAttribs']:
                args['ignore'] = spec.get('ignore', [])

            parsed_dict = out_dict
            if 'subdict' in spec:
                parsed_dict = out_dict.get(spec['subdict'], {})

            parsed_value = action(node, schema_dict, parser_info_out=parser_info_out, **args)

            if isinstance(parsed_value, dict):

                if spec['parse_type'] == 'singleValue':
                    base_value = 'value'
                    no_list = ['units']
                    flat = True
                elif spec['parse_type'] in ['allAttribs', 'parentAttribs']:
                    base_value = spec.get('base_value', '')
                    no_list = spec.get('overwrite', [])
                    flat = spec.get('flat', True)

                if flat:
                    for key, val in parsed_value.items():

                        if key == base_value:
                            current_key = task_key
                        else:
                            current_key = f'{task_key}_{camel_to_snake(key)}'

                        if current_key not in parsed_dict and use_lists:
                            parsed_dict[current_key] = []

                        if key in no_list or not use_lists:
                            parsed_dict[current_key] = val
                        else:
                            parsed_dict[current_key].append(val)

                else:
                    parsed_dict[task_key] = {camel_to_snake(key): val for key, val in parsed_value.items()}

            else:
                overwrite = spec.get('overwrite_last', False)
                if task_key not in parsed_dict and use_lists:
                    if overwrite:
                        parsed_dict[task_key] = None
                    else:
                        parsed_dict[task_key] = []

                if use_lists and not overwrite:
                    parsed_dict[task_key].append(parsed_value)
                elif overwrite:
                    if parsed_value is not None:
                        parsed_dict[task_key] = parsed_value
                else:
                    if parsed_value is not None or\
                       task_key not in parsed_dict:
                        parsed_dict[task_key] = parsed_value

            if 'subdict' in spec:
                out_dict[spec['subdict']] = parsed_dict
            else:
                out_dict = parsed_dict

        conversions = tasks_definition.get('_conversions', [])
        for conversion in conversions:
            action = getattr(convert_funcs, conversion)
            out_dict = action(out_dict, parser_info_out=parser_info_out)

        return out_dict

    def show_available_tasks(self, show_definitions=False):
        """
        Print all currently available task keys.
        If show_definitions is True also the corresponding defintions will be printed
        """
        if show_definitions:
            pprint(self.tasks)
        else:
            pprint(self.tasks.keys())


@register_migration(base_version='0.33', target_version='0.31')
def migrate_033_to_031(definition_dict):
    """
    Migrate definitions for MaX5 release to MaX4 release

    Changes:
        - LDA+U density matrix distance output did not exist
        - forcetheorem units attribute did not exist (get from 'sumValenceSingleParticleEnergies')
    """

    new_dict = copy.deepcopy(definition_dict)

    new_dict.pop('nmmp_distances')

    force_units = {
        'parse_type': 'attrib',
        'path_spec': {
            'name': 'units',
            'tag_name': 'sumValenceSingleParticleEnergies'
        }
    }

    new_dict['forcetheorem_mae']['mae_force_units'] = copy.deepcopy(force_units)
    new_dict['forcetheorem_ssdisp']['spst_force_units'] = copy.deepcopy(force_units)
    new_dict['forcetheorem_jij']['jij_force_units'] = copy.deepcopy(force_units)
    new_dict['forcetheorem_dmi']['dmi_force_units'] = copy.deepcopy(force_units)

    return new_dict
