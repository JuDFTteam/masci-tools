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
import masci_tools.io.parsers.fleur.default_parse_tasks as default_tasks


class ParseTasks(object):

    PARSE_TYPES = {'attrib', 'text', 'numNodes', 'exists', 'allAttribs', 'singleValue'}

    REQUIRED_KEYS = {'parse_type', 'path_spec'}
    ALLOWED_KEYS = {'parse_type', 'path_spec', 'subdict', 'overwrite_last'}
    ALLOWED_KEYS_ALLATTRIBS = {'parse_type', 'path_spec', 'subdict', 'base_value', 'ignore', 'overwrite', 'flat'}

    _version = '0.1.0'

    def __init__(self, version):
        """
        Initialize the default parse tasks
        """
        if version not in default_tasks.__working_out_versions__:
            raise ValueError(f'Unsupported output version: {version}')
        self.tasks = default_tasks.TASKS_DEFINITION.copy()

    def add_task(self, task_name, task_definition, **kwargs):

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

            if definition['parse_type'] == 'allAttribs':
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

    def __getitem__(self, task):

        if task in self.tasks:
            return self.tasks[task]
        else:
            raise KeyError(f"Unknown Tasks: '{task}'")
