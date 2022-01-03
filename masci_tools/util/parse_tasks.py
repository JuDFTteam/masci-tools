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
This module contains a class which organizes the known parsing tasks for outxml files
and provides fuctionality for adding custom tasks easily
"""
from __future__ import annotations

from pprint import pprint
import importlib.util
from importlib import import_module
import copy
import os
from pathlib import Path
from typing import Callable, Iterable, Any
try:
    from typing import Literal, TypeAlias  #type: ignore
except ImportError:
    from typing_extensions import Literal, TypeAlias  #type:ignore
import warnings
from lxml import etree
from logging import Logger, LoggerAdapter
from masci_tools.io.parsers import fleur_schema

from masci_tools.util.xml.converters import convert_str_version_number
from masci_tools.util.typing import XMLLike
import masci_tools

PACKAGE_DIRECTORY = Path(masci_tools.__file__).parent.resolve()
DEFAULT_TASK_FILE = PACKAGE_DIRECTORY / Path('io/parsers/fleur/default_parse_tasks.py')

MigrationDict: TypeAlias = "dict[str, dict[str, Literal['compatible'] | Callable]]"
"""
Type describing the dictionary defining the migration pathways
"""


def find_migration(start: str, target: str, migrations: MigrationDict) -> list[Callable] | None:
    """
    Tries to find a migration path from the start to the target version
    via the defined migration functions

    :param start: str of the starting version
    :param target: str of the target version
    :param migrations: dict of funcs registered via the register_migration_function decorator

    :returns: list of migration functions to be called to go from start to target
    """

    if start == target:
        return []

    if start not in migrations:
        return None

    if target in migrations[start]:
        if isinstance(migrations[start][target], str):
            if migrations[start][target] == 'compatible':
                return []
            return None
        return [migrations[start][target]]

    for possible_stop in migrations[start].keys():
        new_call_list = find_migration(possible_stop, target, migrations)

        if new_call_list is None:
            continue

        if isinstance(migrations[start][possible_stop], str):
            if migrations[start][possible_stop] == 'compatible':
                call_list = []
        else:
            call_list = [migrations[start][possible_stop]]
        call_list += new_call_list
        return call_list
    return None


class ParseTasks:
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

    CONTROL_KEYS = {'_general', '_modes', '_minimal', '_special', '_conversions', '_optional', '_minimum_version'}
    REQUIRED_KEYS = {'parse_type', 'path_spec'}
    ALLOWED_KEYS = {'parse_type', 'path_spec', 'subdict', 'overwrite_last'}
    ALLOWED_KEYS_ALLATTRIBS = {
        'parse_type', 'path_spec', 'subdict', 'base_value', 'ignore', 'overwrite', 'flat', 'only_required', 'subtags',
        'text'
    }

    _version = '0.2.0'
    _migrations: MigrationDict = {}
    _all_attribs_function: set[str] = set()
    _conversion_functions: dict[str, Callable] = {}
    _parse_functions: dict[str, Callable] = {}

    def __init__(self, version: str, task_file: os.PathLike | None = None, validate_defaults: bool = False) -> None:
        """
        Initialize the default parse tasks
        Terminates if the version is not marked as working with the default tasks

        :param version: str of the wanted ouput version
        :param task_file: optional, file to override default_parse_tasks
        :param validate_defaults: bool, if True all tasks from the default tasks
                                  are added one by one and are checked for
                                  inconsistent keys
        """

        if task_file is None:
            task_file = DEFAULT_TASK_FILE

        #import task definitions
        spec = importlib.util.spec_from_file_location('tasks', task_file)
        if spec is None:
            raise ValueError(f'Module not found {task_file}')
        tasks = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tasks)  #type:ignore

        self._iteration_tasks: list[str] = []
        self._general_tasks: list[str] = []
        self.version = convert_str_version_number(version)

        tasks_dict: dict[str, dict[str, Any]] = copy.deepcopy(tasks.TASKS_DEFINITION)
        if validate_defaults:
            #Manually add each task to make sure that there are no typos/inconsitencies in the keys
            self.tasks = {}
            for task_name, task in tasks_dict.items():
                self.add_task(task_name, task)
        else:
            self.tasks = tasks_dict

        working: set[str] = tasks.__working_out_versions__
        #Look if the base version is compatible if not look for a migration
        if version not in working:

            working_version_tuples = {convert_str_version_number(v) for v in working}
            version_tuple = convert_str_version_number(version)

            if all(working_version < version_tuple for working_version in working_version_tuples):
                warnings.warn(
                    f"Output version '{version}' is not explicitely stated as 'working'\n"
                    'with the current version of the outxml_parser.\n'
                    'Since the given version is newer than the latest working version\n'
                    'I will continue. Errors and warnings can occur!', UserWarning)
            else:
                base: str = tasks.__base_version__
                migration_list = find_migration(base, version, self.migrations)

                if migration_list is None:
                    raise ValueError(f'Unsupported output version: {version}')

                for migration in migration_list:
                    self.tasks = migration(self.tasks)

    @property
    def iteration_tasks(self) -> list[str]:
        """
        Tasks to perform for each iteration
        """
        return self._iteration_tasks

    @iteration_tasks.setter
    def iteration_tasks(self, val: list[str]) -> None:
        """
        Setter for iteration_tasks
        """
        self._iteration_tasks = val

    @property
    def general_tasks(self) -> list[str]:
        """
        Tasks to perform for the root node
        """
        return self._general_tasks

    @general_tasks.setter
    def general_tasks(self, val: list[str]) -> None:
        """
        Setter for general_tasks
        """
        self._general_tasks = val

    @property
    def migrations(self) -> MigrationDict:
        """
        Return the registered migrations
        """
        if getattr(self, '_migrations', None) is None:
            import_module('masci_tools.io.parsers.fleur.task_migrations')
        return self._migrations

    @property
    def conversion_functions(self) -> dict[str, Callable]:
        """
        Return the registered conversion functions
        """
        if getattr(self, '_conversion_functions', None) is None:
            import_module('masci_tools.io.parsers.fleur.outxml_conversion')
        return self._conversion_functions

    @property
    def parse_functions(self) -> dict[str, Callable]:
        """
        Return the registered parse functions
        """
        if getattr(self, '_parse_functions', None) is None:
            import_module('masci_tools.util.schema_dict_util')
        return self._parse_functions

    @property
    def all_attribs_function(self) -> set[str]:
        """
        Return the registered parse functions for parsing multipl attributes
        """
        if getattr(self, '_all_attribs_function', None) is None:
            import_module('masci_tools.util.schema_dict_util')
        return self._all_attribs_function

    @property
    def optional_tasks(self) -> set[str]:
        """
        Return a set of the available optional defined tasks
        """
        return {key for key, val in self.tasks.items() if val.get('_optional', False)}

    def add_task(self,
                 task_name: str,
                 task_definition: dict[str, Any],
                 append: bool = False,
                 overwrite: bool = False) -> None:
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
            :param path_spec: dict with all the arguments that should be passed to tag_xpath
                              or attrib_xpath to get the correct path
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

            if not definition['parse_type'] in self.parse_functions:
                raise ValueError(f"Unknown parse_type: {definition['parse_type']}")

            if definition['parse_type'] in self.all_attribs_function:
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

    def determine_tasks(self,
                        fleurmodes: dict[str, Any],
                        optional_tasks: Iterable[str] | None = None,
                        minimal: bool = False) -> None:
        """
        Determine, which tasks to perform based on the fleur_modes

        :param fleurmodes: dict with the calculation modes
        :param minimal: bool, whether to only perform minimal tasks
        """

        if optional_tasks is None:
            optional_tasks = set()

        unknown = {name for name in optional_tasks if name not in self.optional_tasks}
        if unknown:
            raise ValueError(f"Unknown optional task(s): '{unknown}'\n"
                             f'The following are available: {self.optional_tasks}')

        for task_name, definition in self.tasks.items():

            if '_minimum_version' in definition:
                min_version = convert_str_version_number(definition['_minimum_version'])
                if self.version < min_version:
                    continue

            optional = definition.get('_optional', False)
            if optional and task_name not in optional_tasks:
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
                     task_name: str,
                     node: XMLLike,
                     out_dict: dict,
                     schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                     constants: dict[str, float],
                     logger: Logger | LoggerAdapter | None = None,
                     use_lists: bool = True) -> dict:
        """
        Evaluates the task given in the tasks_definition dict

        :param task_name: str, specifies the task to perform
        :param node: etree.Element, the xpath expressions are evaluated from this node
        :param out_dict: dict, output will be put in this dictionary
        :param schema_dict: dict, here all paths and attributes are stored according to the
                            outputschema
        :param constants: dict with all the defined mathematical constants
        :param logger: logger object for logging warnings, errors
        :param root_tag: str, this string will be appended in front of any xpath before it is evaluated
        :param use_lists: bool, if True lists are created for each key if not otherwise specified

        """
        from masci_tools.io.common_functions import camel_to_snake

        try:
            tasks_definition = self.tasks[task_name]
        except KeyError as exc:
            raise KeyError(f'Unknown Task: {task_name}') from exc

        for task_key, spec in tasks_definition.items():

            if task_key.startswith('_'):
                continue

            action = self.parse_functions[spec['parse_type']]

            args = spec['path_spec'].copy()

            if spec['parse_type'] in ['attrib', 'text', 'allAttribs', 'parentAttribs', 'singleValue']:
                args['constants'] = constants

            if 'only_required' in spec:
                args['only_required'] = spec['only_required']

            if 'subtags' in spec:
                args['subtags'] = spec['subtags']

            if spec['parse_type'] == 'singleValue':
                args['ignore'] = ['comment']
            elif spec['parse_type'] in ['allAttribs', 'parentAttribs']:
                args['ignore'] = spec.get('ignore', [])

            parsed_dict = out_dict
            if 'subdict' in spec:
                parsed_dict = out_dict.get(spec['subdict'], {})

            parsed_value = action(node, schema_dict, logger=logger, **args)

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
            action = self.conversion_functions[conversion]
            out_dict = action(out_dict, logger=logger)

        return out_dict

    def show_available_tasks(self, show_definitions: bool = False) -> None:
        """
        Print all currently available task keys.
        If show_definitions is True also the corresponding defintions will be printed
        """
        if show_definitions:
            pprint(self.tasks)
        else:
            pprint(self.tasks.keys())
