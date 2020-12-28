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
This module defines decorators for the ParseTasks class to make extending/modifying the parser
more convenient

Up till now 3 decorators are defined:
    - ```register_migration``` marks a function of making backwards incompatible changes
      to the parsing tasks
    - ```register_parsing_function``` gives a mappimg between available parsing functions
      and the keywords in the parsing tasks
    - ```conversion_function``` makes the decorated function available to be called easily
      after a certain parsing task has occured
"""
from masci_tools.io.parsers.fleur.parse_tasks import ParseTasks
from functools import wraps


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


def conversion_function(func):
    """
    Return decorated ParseTasks object with _conversion_functions dict attribute
    Here all registered conversion functions are inserted
    """

    @wraps(func)
    def convert_func(*args, **kwargs):
        """Decorator for parse_type function"""
        return func(*args, **kwargs)

    setattr(ParseTasks, func.__name__, convert_func)

    if not hasattr(ParseTasks, '_conversion_functions'):
        ParseTasks._conversion_functions = {}  # pylint: disable=protected-access

    ParseTasks._conversion_functions[func.__name__] = getattr(ParseTasks, func.__name__)  # pylint: disable=protected-access

    return convert_func
