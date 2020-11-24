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
This module contains helper functions for extracting information easily from the
schema_dicts defined for the Fleur input/output

Also provides convienient functions to use just a attribute name for extracting the
attribute from the right place in the given etree
"""

from masci_tools.util.xml.common_xml_util import eval_xpath, convert_xml_text, convert_xml_attribute

def get_tag_xpath(schema_dict, name, contains=None, not_contains=None):

    possible_lists = ['tag_paths']

    if 'iteration_tag_paths' in schema_dict:
        possible_lists += ['iteration_tag_paths']

    all_paths = []
    for list_name in possible_lists:
        if name in schema_dict[list_name]:
            paths = schema_dict[list_name][name]

            if not isinstance(paths, list):
                paths = [paths]
            paths = paths.copy()

            invalid_paths = []
            if contains is not None:
                for xpath in paths:
                    if contains not in xpath:
                        invalid_paths.append(xpath)

            if not_contains is not None:
                for xpath in paths:
                    if not_contains not in xpath and xpath not in invalid_paths:
                        invalid_paths.append(xpath)

            for invalid in invalid_paths:
                paths.remove(invalid)

            if len(paths) == 1:
                return paths[0]

            all_paths += paths

    raise ValueError(f'The tag {name} has multiple possible paths with the current specification.\n'
                     f'contains: {contains}, not_contains: {not_contains} \n'
                     f'These are possible: {all_paths}')


def get_attrib_xpath(schema_dict, name, contains=None, not_contains=None, exclude=None):


    possible_lists = ['settable_attribs', 'settable_contains_attribs', 'other_attribs']
    output = False
    if 'iteration_settable_attribs' in schema_dict:
        #outputschema
        output = True
        possible_lists += ['iteration_settable_attribs', 'iteration_settable_contains_attribs', 'iteration_other_attribs']

    if exclude is not None:
        for list_name in exclude:
            possible_lists.remove(f'{list_name}_attribs')
            if output:
                possible_lists.remove(f'iteration_{list_name}_attribs')
    all_paths = []
    for list_name in possible_lists:
        if name in schema_dict[list_name]:
            paths = schema_dict[list_name][name]

            if not isinstance(paths, list):
                paths = [paths]
            paths = paths.copy()

            invalid_paths = []
            if contains is not None:
                for xpath in paths:
                    if contains not in xpath:
                        invalid_paths.append(xpath)

            if not_contains is not None:
                for xpath in paths:
                    if not_contains not in xpath and xpath not in invalid_paths:
                        invalid_paths.append(xpath)

            for invalid in invalid_paths:
                paths.remove(invalid)

            if len(paths) == 1:
                return paths[0]

            all_paths += paths

    raise ValueError(f'The attrib {name} has multiple possible paths with the current specification.\n'
                     f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}\n'
                     f'These are possible: {all_paths}')

def evaluate_attribute(node,
                       schema_dict,
                       name,
                       constants,
                       contains=None,
                       not_contains=None,
                       exclude=None,
                       parser_info_out=None,
                       abspath=None):

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    attrib_xpath = get_attrib_xpath(schema_dict, name, contains=contains, not_contains=not_contains, exclude=exclude)

    if abspath is not None:
        attrib_xpath = f'{abspath}{attrib_xpath}'

    stringattribute = eval_xpath(node, f'{attrib_xpath}/@{name}', parser_info_out=parser_info_out)

    if isinstance(stringattribute, list):
        if len(stringattribute) == 0:
            parser_info_out['parser_warnings'].append(f'No values found for attribute {name}')
            return None

    possible_types = schema_dict['attrib_types'][name]

    warnings = []
    converted_value, suc = convert_xml_attribute(stringattribute,
                                                 possible_types,
                                                 constants,
                                                 conversion_warnings=warnings)

    if not suc:
        parser_info_out['parser_warnings'].append(f'Failed to evaluate attribute {name}: '
                                                  'Below are the warnings from convert_xml_attribute')
        for warning in warnings:
            parser_info_out['parser_warnings'].append(warning)

    return converted_value


def evaluate_text(node,
                  schema_dict,
                  name,
                  constants,
                  contains=None,
                  not_contains=None,
                  parser_info_out=None,
                  abspath=None):

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    tag_xpath = get_tag_xpath(schema_dict, name, contains=contains, not_contains=not_contains)

    if abspath is not None:
        tag_xpath = f'{abspath}{tag_xpath}'

    stringtext = eval_xpath(node, f'{tag_xpath}/text()', parser_info_out=parser_info_out)

    possible_definitions = schema_dict['simple_elements'][name]

    warnings = []
    converted_value, suc = convert_xml_text(stringtext, possible_definitions, constants, conversion_warnings=warnings)

    if not suc:
        parser_info_out['parser_warnings'].append(f'Failed to evaluate text for tag {name}: '
                                                  'Below are the warnings from convert_xml_text')
        for warning in warnings:
            parser_info_out['parser_warnings'].append(warning)

    return converted_value


def evaluate_single_value_tag(node,
                              schema_dict,
                              name,
                              constants,
                              contains=None,
                              not_contains=None,
                              parser_info_out=None,
                              abspath=None):

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    tag_xpath = get_tag_xpath(schema_dict, name, contains=contains, not_contains=not_contains)

    if abspath is not None:
        tag_xpath = f'{abspath}{tag_xpath}'

    value_dict = {}
    attribs_to_parse = ['value', 'units']
    for attrib in attribs_to_parse:

        stringattribute = eval_xpath(node, f'{tag_xpath}/@{attrib}', parser_info_out=parser_info_out)

        if isinstance(stringattribute, list):
            if len(stringattribute) == 0: #If unit is not available this is expected
                if attrib=='value':
                    parser_info_out['parser_warnings'].append(f'No values found for attribute {attrib} at tag {name}')
                value_dict[attrib] = None
                continue

        possible_types = schema_dict['attrib_types'][attrib]

        warnings = []
        value_dict[attrib], suc = convert_xml_attribute(stringattribute,
                                                        possible_types,
                                                        constants,
                                                        conversion_warnings=warnings)

        if not suc:
            parser_info_out['parser_warnings'].append(f'Failed to evaluate attribute {attrib}: '
                                                      'Below are the warnings from convert_xml_attribute')
            for warning in warnings:
                parser_info_out['parser_warnings'].append(warning)

    return value_dict['value'], value_dict['units']


def tag_exists(node, schema_dict, name, contains=None, parser_info_out=None, abspath=None):

    return get_number_of_nodes(
        node, schema_dict, name, contains=contains, parser_info_out=parser_info_out, abspath=abspath) != 0


def get_number_of_nodes(node, schema_dict, name, contains=None, parser_info_out=None, abspath=None):

    tag_xpath = get_tag_xpath(schema_dict, name, contains=contains)

    if abspath is not None:
        tag_xpath = f'{abspath}{tag_xpath}'

    return len(eval_xpath(node, tag_xpath, parser_info_out=parser_info_out, list_return=True))
