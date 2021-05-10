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
from masci_tools.util.parse_tasks import ParseTasks
from functools import wraps


def register_migration(base_version, target_version):
    """
    Decorator to add migration for task definition dictionary to the ParseTasks class
    The function should only take the dict of task definitions as an argument

    :param base_version: str of the version, from which the migration starts
    :param target_version: str or list of str with the versions that work after
                           the migration has been performed

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

        if not hasattr(ParseTasks, '_migrations'):
            ParseTasks._migrations = {}  # pylint: disable=protected-access
        if not base_version in ParseTasks._migrations:
            ParseTasks._migrations[base_version] = {}

        target_version_list = target_version
        if not isinstance(target_version_list, list):
            target_version_list = [target_version_list]
        for valid_version in target_version_list:
            ParseTasks._migrations[base_version][valid_version] = migration  # pylint: disable=protected-access

            for valid_version_2 in target_version_list:
                if valid_version == valid_version_2:
                    continue
                if int(valid_version.split('.')[1]) > int(valid_version_2.split('.')[1]):
                    if valid_version not in ParseTasks._migrations:
                        ParseTasks._migrations[valid_version] = {}
                    ParseTasks._migrations[valid_version][valid_version_2] = 'compatible'
                else:
                    if valid_version_2 not in ParseTasks._migrations:
                        ParseTasks._migrations[valid_version_2] = {}
                    ParseTasks._migrations[valid_version_2][valid_version] = 'compatible'

        return migration

    return migration_decorator


def register_parsing_function(parse_type_name, all_attribs_keys=False):
    """
    Decorator to add parse type for task definition dictionary.

    :param parse_type_name: str, the function can be selected in task defintions
                            via this string
    :param all_attribs_keys: bool, if True the arguments for parsing multiple attributes
                             are valid

    The decorated function has to have the following arguments:
        :param node: etree Element, on which to execute the xpath evaluations
        :param schema_dict: dict, containing all the path information and more
        :param name: str, name of the tag/attribute
        :param parser_info_out: dict, with warnings, info, errors, ...
        :param kwargs: here all other keyword arguments are collected

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

        if not hasattr(ParseTasks, '_parse_functions'):
            ParseTasks._parse_functions = {}  # pylint: disable=protected-access
            ParseTasks._all_attribs_function = set()

        ParseTasks._parse_functions[parse_type_name] = parse_type  # pylint: disable=protected-access
        if all_attribs_keys:
            ParseTasks._all_attribs_function.add(parse_type_name)

        return parse_type

    return parse_type_decorator


def conversion_function(func):
    """
    Marks a function as a conversion function, which can be called after
    performing a parsing task. The function can be specified via the _conversions
    control key in the task definitions.

    A conversion function has to have the following arguments:
        :param out_dict: dict with the previously parsed information
        :param parser_info_out: dict, with warnings, info, errors, ...

    and return only the modified output dict
    """

    @wraps(func)
    def convert_func(*args, **kwargs):
        """Decorator for parse_type function"""
        return func(*args, **kwargs)

    if not hasattr(ParseTasks, '_conversion_functions'):
        ParseTasks._conversion_functions = {}  # pylint: disable=protected-access

    ParseTasks._conversion_functions[func.__name__] = convert_func  # pylint: disable=protected-access

    return convert_func
