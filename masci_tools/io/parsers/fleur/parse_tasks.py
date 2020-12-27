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


def register_migration(cls, base_version, target_version):
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

        setattr(cls, func.__name__, migration)

        if not hasattr(cls, '_migrations'):
            cls._migrations = {}  # pylint: disable=protected-access
        if not base_version in cls._migrations:
            cls._migrations[base_version] = {}
        cls._migrations[base_version][target_version] = getattr(cls, func.__name__)  # pylint: disable=protected-access

        return migration

    return migration_decorator


class ParseTasks(object):
    """
    Representation of all known parsing tasks for the out.xml file

    When set up it will initialize the known default tasks and check if they work
    for the given output version

    Accesing definition of task example

    .. code-block:: python

        from masci_tools.io.parsers.fleur import ParseTasks

        parse_tasks = ParseTasks('0.33')
        totE_definition = parse_tasks['total_energy']
    """

    PARSE_TYPES = {'attrib', 'text', 'numberNodes', 'exists', 'allAttribs', 'parentAttribs', 'singleValue'}

    REQUIRED_KEYS = {'parse_type', 'path_spec'}
    ALLOWED_KEYS = {'parse_type', 'path_spec', 'subdict', 'overwrite_last'}
    ALLOWED_KEYS_ALLATTRIBS = {
        'parse_type', 'path_spec', 'subdict', 'base_value', 'ignore', 'overwrite', 'flat', 'only_required'
    }

    GENERAL_TASKS = {
        'fleur_modes', 'general_inp_info', 'general_out_info', 'ldau_info', 'bulk_relax_info', 'film_relax_info'
    }

    _version = '0.1.1'

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

        self.incompatible_tasks = []
        self.append_tasks = []

        tasks_dict = copy.deepcopy(tasks.TASKS_DEFINITION)
        if validate_defaults:
            #Manually add each task to make sure that there are no typos/inconsitencies in the keys
            self.tasks = {}
            for task_name, task in tasks_dict.items():
                self.add_task(task_name, task, perform_default=False)
        else:
            self.tasks = tasks_dict

        #Look if the base version is compatible if not look for a migration
        if version not in tasks.__working_out_versions__:
            if version in self._migrations['0.33']:
                self.tasks, self.incompatible_tasks = self._migrations['0.33'][version](self.tasks,
                                                                                        self.incompatible_tasks)
            else:
                raise ValueError(f'Unsupported output version: {version}')

    def __getitem__(self, task):
        """
        Access tasks via [] index
        """
        if task in self.tasks:
            return self.tasks[task]
        else:
            raise KeyError(f"Unknown Tasks: '{task}'")

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
        :param perform_default: bool (optional), if True (default) the task is automatically appended to the
                                tasks to be performed each iteration

        """

        append = kwargs.get('append', False)
        overwrite = kwargs.get('overwrite', False)
        perform_default = kwargs.get('perform_default', True)

        if task_name in self.tasks and not (append or overwrite):
            raise ValueError(f"Task '{task_name}' is already defined."
                             'Use append=True to append them (conflicting keys are overwritten)'
                             'or overwrite=True to remove all existing tasks')

        for task_key, definition in task_definition.items():

            task_keys = set(definition.keys())

            if not task_keys and task_key in self.tasks[task_name]:
                continue

            missing_required = self.REQUIRED_KEYS.difference(task_keys)
            if missing_required:
                raise ValueError(f'Reqired Keys missing: {missing_required}')

            if not definition['parse_type'] in self.PARSE_TYPES:
                raise ValueError(f"Unknown parse_type: {definition['parse_type']}")

            if definition['parse_type'] in ['allAttribs', 'parentAttribs', 'singleValue']:
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

        if task_name not in self.GENERAL_TASKS and perform_default:
            self.append_tasks.append(task_name)

    def show_available_tasks(self, show_definitions=False):
        """
        Print all currently available task keys.
        If show_definitions is True also the corresponding defintions will be printed
        """
        if show_definitions:
            pprint(self.tasks)
        else:
            pprint(self.tasks.keys())


@register_migration(ParseTasks, base_version='0.33', target_version='0.31')
def migrate_033_to_031(definition_dict, incompatible_tasks):
    """
    Migrate definitions for MaX5 release to MaX4 release

    Changes:
        - LDA+U density matrix distance output did not exist
        - forcetheorem units attribute did not exist (get from 'sumValenceSingleParticleEnergies')
    """

    new_dict = copy.deepcopy(definition_dict)
    new_incompatible_tasks = copy.deepcopy(incompatible_tasks)

    new_dict.pop('nmmp_distances')
    new_incompatible_tasks.append('nmmp_distances')

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

    return new_dict, new_incompatible_tasks
