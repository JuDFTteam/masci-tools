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
from __future__ import absolute_import
from .default_parse_tasks import TASKS_DEFINITION, __working_out_versions__
from pprint import pprint
import copy
from functools import wraps

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

    PARSE_TYPES = {'attrib', 'text', 'numNodes', 'exists', 'allAttribs', 'parentAttribs', 'singleValue'}

    REQUIRED_KEYS = {'parse_type', 'path_spec'}
    ALLOWED_KEYS = {'parse_type', 'path_spec', 'subdict', 'overwrite_last'}
    ALLOWED_KEYS_ALLATTRIBS = {'parse_type', 'path_spec', 'subdict', 'base_value', 'ignore', 'overwrite', 'flat'}

    _version = '0.1.0'

    def __init__(self, version):
        """
        Initialize the default parse tasks
        Terminates if the version is not marked as working with the default tasks

        TODO: We need some way of versioning for the default tasks
        """
        self.tasks = TASKS_DEFINITION.copy()

        #Look if the base version is compatible if not look for a migration
        if version not in __working_out_versions__:
            if version in self._migrations['0.33'][version]:
                self.tasks = self._migrations['0.33'][version](self.tasks)
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
                       will be inserted into this dictionary (inner keys WILL BE OVERWRITTEN)

        """

        append = kwargs.get('append', False)
        overwrite = kwargs.get('overwrite', False)

        if task_name in self.tasks and not append:
            raise ValueError(f"Task '{task_name}' is already defined."
                             'Use append=True to append them (conflicting keys are overwritten)'
                             'or overwrite=True to remove all existing tasks')

        for task_key, definition in task_definition.items():

            task_keys = set(definition.keys())

            missing_required = task_keys.difference(self.REQUIRED_KEYS)
            if missing_required:
                raise ValueError(f'Reqired Keys missing: {missing_required}')

            if not definition['parse_type'] in self.PARSE_TYPES:
                raise ValueError(f"Unknown parse_type: {definition['parse_type']}")

            if definition['parse_type'] in ['allAttribs', 'parentAttribs']:
                extra_keys = self.ALLOWED_KEYS_ALLATTRIBS.difference(task_keys)
            else:
                extra_keys = self.ALLOWED_KEYS.difference(task_keys)

            if extra_keys:
                raise ValueError(f'Got extra Keys: {extra_keys}')

        if append:
            if task_name not in self.tasks:
                self.tasks[task_name] = {}
            for task_key, definition in task_definition.items():
                self.tasks[task_name][task_key] = definition
        else:
            self.tasks[task_name] = task_definition

    def show_available_tasks(self, show_definitions=False):
        """
        Print all currently available task keys.
        If show_definitions is True also the corresponding defintions will be printed
        """
        if show_definitions:
            pprint(self.tasks)
        else:
            pprint(self.tasks.keys())


@register_migration(ParseTasks,'0.33', '0.27')
def migrate_033_to027(definition_dict):
    """
    Test migration from 0.33 to 0.27
    Will not work at the moment only to show the concept
    """
    new_dict = copy.deepcopy(definition_dict)

    new_dict['general_out_info'].pop('number_of_atom_types')
    new_dict['general_inp_info']['number_of_atom_types'] = {
        'parse_type': 'numberNodes',
        'path_spec': {
            'name': 'atomGroup'
        }
    }

    return new_dict
