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
from masci_tools.util.parse_tasks_decorators import register_parsing_function
from masci_tools.util.lockable_containers import LockableList
from lxml import etree


def get_tag_xpath(schema_dict, name, contains=None, not_contains=None):
    """
    Tries to find a unique path from the schema_dict based on the given name of the tag
    and additional further specifications

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path

    :returns: str, xpath to the given tag

    :raises ValueError: If no unique path could be found
    """

    if contains is None:
        contains = []
    elif not isinstance(contains, list):
        contains = [contains]

    if not_contains is None:
        not_contains = []
    elif not isinstance(not_contains, list):
        not_contains = [not_contains]

    possible_lists = ['tag_paths']

    if 'iteration_tag_paths' in schema_dict:
        possible_lists += ['iteration_tag_paths']

    all_paths = []
    for list_name in possible_lists:
        if name in schema_dict[list_name]:
            paths = schema_dict[list_name][name]

            if not isinstance(paths, LockableList):
                paths = [paths]
            else:
                paths = paths.get_unlocked()

            invalid_paths = set()
            for phrase in contains:
                for xpath in paths:
                    if phrase not in xpath:
                        invalid_paths.add(xpath)

            for phrase in not_contains:
                for xpath in paths:
                    if phrase in xpath:
                        invalid_paths.add(xpath)

            for invalid in invalid_paths:
                paths.remove(invalid)

            all_paths += paths

    if len(all_paths) == 1:
        return all_paths[0]
    elif len(all_paths) == 0:
        raise ValueError(f'The tag {name} has no possible paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}')
    else:
        raise ValueError(f'The tag {name} has multiple possible paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains} \n'
                         f'These are possible: {all_paths}')


def get_tag_info(schema_dict, name, contains=None, not_contains=None, path_return=True, convert_to_builtin=False):
    """
    Tries to find a unique path from the schema_dict based on the given name of the tag
    and additional further specifications and returns the tag_info entry for this tag

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path
    :param path_return: bool, if True the found path will be returned alongside the tag_info
    :param convert_to_builtin: bool, if True the CaseInsensitiveFrozenSets are converetd to normal sets
                               with the rigth case of the attributes

    :returns: dict, tag_info for the found xpath
    :returns: str, xpath to the tag if `path_return=True`
    """
    import copy
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet

    tag_xpath = get_tag_xpath(schema_dict, name, contains=contains, not_contains=not_contains)
    tag_info = copy.deepcopy(schema_dict['tag_info'][tag_xpath])

    if convert_to_builtin:
        tag_info = {
            key: set(val.original_case.values()) if isinstance(val, CaseInsensitiveFrozenSet) else val
            for key, val in tag_info.items()
        }

    if path_return:
        return tag_info, tag_xpath
    else:
        return tag_info


def get_attrib_xpath(schema_dict, name, contains=None, not_contains=None, exclude=None, tag_name=None):
    """
    Tries to find a unique path from the schema_dict based on the given name of the attribute
    and additional further specifications

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the attribute
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path
    :param exclude: list of str, here specific types of attributes can be excluded
                    valid values are: settable, settable_contains, other
    :param tag_name: str, if given this name will be used to find a path to a tag with the
                     same name in :py:func:`get_tag_xpath()`

    :returns: str, xpath to the tag with the given attribute

    :raises ValueError: If no unique path could be found
    """

    if tag_name is not None:
        tag_xpath = get_tag_xpath(schema_dict, tag_name, contains=contains, not_contains=not_contains)

        err_msg = f'No attribute {name} found at tag {tag_name}'
        if tag_xpath in schema_dict['tag_info']:
            if name not in schema_dict['tag_info'][tag_xpath]['attribs']:
                raise ValueError(err_msg)
        else:
            if name not in schema_dict['iteration_tag_info'][tag_xpath]['attribs']:
                raise ValueError(err_msg)
        return f'{tag_xpath}/@{name}'

    if contains is None:
        contains = []
    elif not isinstance(contains, list):
        contains = [contains]

    if not_contains is None:
        not_contains = []
    elif not isinstance(not_contains, list):
        not_contains = [not_contains]

    possible_lists = ['unique_attribs', 'unique_path_attribs', 'other_attribs']
    output = False
    if 'iteration_unique_attribs' in schema_dict:
        #outputschema
        output = True
        possible_lists += ['iteration_unique_attribs', 'iteration_unique_path_attribs', 'iteration_other_attribs']

    if exclude is not None:
        for list_name in exclude:
            possible_lists.remove(f'{list_name}_attribs')
            if output:
                possible_lists.remove(f'iteration_{list_name}_attribs')
    all_paths = []
    for list_name in possible_lists:
        if name in schema_dict[list_name]:
            paths = schema_dict[list_name][name]

            if not isinstance(paths, LockableList):
                paths = [paths]
            else:
                paths = paths.get_unlocked()

            invalid_paths = set()
            for phrase in contains:
                for xpath in paths:
                    if phrase not in xpath:
                        invalid_paths.add(xpath)

            for phrase in not_contains:
                for xpath in paths:
                    if phrase in xpath:
                        invalid_paths.add(xpath)

            for invalid in invalid_paths:
                paths.remove(invalid)

            all_paths += paths

    if len(all_paths) == 1:
        return all_paths[0]
    elif len(all_paths) == 0:
        raise ValueError(f'The attrib {name} has no possible paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}')
    else:
        raise ValueError(f'The attrib {name} has multiple possible paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}\n'
                         f'These are possible: {all_paths}')


def read_constants(root, schema_dict):
    """
    Reads in the constants defined in the inp.xml
    and returns them combined with the predefined constants from
    fleur as a dictionary

    :param root: root of the etree of the inp.xml file
    :param schema_dict: schema_dictionary of the version of the file to read (inp.xml or out.xml)

    :return: a python dictionary with all defined constants
    """
    from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS
    import copy

    defined_constants = copy.deepcopy(FLEUR_DEFINED_CONSTANTS)

    constants = evaluate_tag(root, schema_dict, 'constant', defined_constants)

    if constants['name'] is not None:
        if not isinstance(constants['name'], list):
            constants = {key: [val] for key, val in constants.items()}
        for name, value in zip(constants['name'], constants['value']):
            if name not in defined_constants:
                defined_constants[name] = value
            else:
                raise KeyError(f'Ambiguous definition of key {name}')

    return defined_constants


@register_parsing_function('attrib')
def evaluate_attribute(node, schema_dict, name, constants, parser_info_out=None, **kwargs):
    """
    Evaluates the value of the attribute based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the attribute
    :param constants: dict, contains the defined constants
    :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other
        :param replace_root: str, replaces the root tag (used for inserting output root to input paths)

    :returns: list or single value, converted in convert_xml_attribute
    """
    from masci_tools.util.xml.common_xml_util import eval_xpath, convert_xml_attribute

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    contains = kwargs.get('contains', None)
    not_contains = kwargs.get('not_contains', None)
    exclude = kwargs.get('exclude', None)
    tag_name = kwargs.get('tag_name', None)

    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            if contains is None:
                contains = []
            contains = set(contains)
            contains.add(node.tag)
            contains = list(contains)

    attrib_xpath = get_attrib_xpath(schema_dict,
                                    name,
                                    contains=contains,
                                    not_contains=not_contains,
                                    exclude=exclude,
                                    tag_name=tag_name)

    stringattribute = eval_xpath(node, attrib_xpath, parser_info_out=parser_info_out)

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


@register_parsing_function('text')
def evaluate_text(node, schema_dict, name, constants, parser_info_out=None, **kwargs):
    """
    Evaluates the text of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param replace_root: str, replaces the root tag (used for inserting output root to input paths)


    :returns: list or single value, converted in convert_xml_text
    """
    from masci_tools.util.xml.common_xml_util import eval_xpath, convert_xml_text

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    contains = kwargs.get('contains', None)
    not_contains = kwargs.get('not_contains', None)

    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            if contains is None:
                contains = []
            contains = set(contains)
            contains.add(node.tag)
            contains = list(contains)

    tag_xpath = get_tag_xpath(schema_dict, name, contains=contains, not_contains=not_contains)

    stringtext = eval_xpath(node, f'{tag_xpath}/text()', parser_info_out=parser_info_out)

    if isinstance(stringtext, list):
        for text in stringtext.copy():
            if text.strip() == '':
                stringtext.remove(text)
    else:
        if stringtext.strip() == '':
            stringtext = []

    if isinstance(stringtext, list):
        if len(stringtext) == 0:
            parser_info_out['parser_warnings'].append(f'No text found for tag {name}')
            return None

    possible_definitions = schema_dict['simple_elements'][name]

    warnings = []
    converted_value, suc = convert_xml_text(stringtext, possible_definitions, constants, conversion_warnings=warnings)

    if not suc:
        parser_info_out['parser_warnings'].append(f'Failed to evaluate text for tag {name}: '
                                                  'Below are the warnings from convert_xml_text')
        for warning in warnings:
            parser_info_out['parser_warnings'].append(warning)

    return converted_value


@register_parsing_function('allAttribs', all_attribs_keys=True)
def evaluate_tag(node, schema_dict, name, constants, parser_info_out=None, **kwargs):
    """
    Evaluates all attributes of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param replace_root: str, replaces the root tag (used for inserting output root to input paths)
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param only_required: bool (optional, default False), if True only required attributes are parsed
        :param ignore: list of str (optional), attributes not to parse

    :returns: dict, with attribute values converted via convert_xml_attribute
    """
    from masci_tools.util.xml.common_xml_util import eval_xpath, convert_xml_attribute

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    contains = kwargs.get('contains', None)
    not_contains = kwargs.get('not_contains', None)
    only_required = kwargs.get('only_required', False)

    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            if contains is None:
                contains = []
            contains = set(contains)
            contains.add(node.tag)
            contains = list(contains)

    tag_xpath = get_tag_xpath(schema_dict, name, contains=contains, not_contains=not_contains)

    #Which attributes are expected
    attribs = set()
    if tag_xpath in schema_dict['tag_info']:
        attribs = schema_dict['tag_info'][tag_xpath]['attribs']
        optional = schema_dict['tag_info'][tag_xpath]['optional_attribs']
    elif 'iteration_tag_info' in schema_dict:
        if tag_xpath in schema_dict['iteration_tag_info']:
            attribs = schema_dict['iteration_tag_info'][tag_xpath]['attribs']
            optional = schema_dict['iteration_tag_info'][tag_xpath]['optional_attribs']

    if only_required:
        attribs = attribs.difference(optional)

    if 'ignore' in kwargs:
        attribs = attribs.difference(kwargs.get('ignore'))

    if not attribs:
        parser_info_out['parser_warnings'].append(f'Failed to evaluate attributes from tag {name}: '
                                                  'No attributes to parse either the tag does not '
                                                  'exist or it has no attributes')
    else:
        attribs = sorted(list(attribs.original_case.values()))

    out_dict = {}

    for attrib in attribs:

        stringattribute = eval_xpath(node, f'{tag_xpath}/@{attrib}', parser_info_out=parser_info_out)

        if isinstance(stringattribute, list):
            if len(stringattribute) == 0:
                parser_info_out['parser_warnings'].append(f'No values found for attribute {attrib} at tag {name}')
                out_dict[attrib] = None
                continue

        possible_types = schema_dict['attrib_types'][attrib]

        warnings = []
        out_dict[attrib], suc = convert_xml_attribute(stringattribute,
                                                      possible_types,
                                                      constants,
                                                      conversion_warnings=warnings)

        if not suc:
            parser_info_out['parser_warnings'].append(f'Failed to evaluate attribute {attrib}: '
                                                      'Below are the warnings from convert_xml_attribute')
            for warning in warnings:
                parser_info_out['parser_warnings'].append(warning)

    return out_dict


@register_parsing_function('singleValue', all_attribs_keys=True)
def evaluate_single_value_tag(node, schema_dict, name, constants, parser_info_out=None, **kwargs):
    """
    Evaluates the value and unit attribute of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param replace_root: str, replaces the root tag (used for inserting output root to input paths)
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param only_required: bool (optional, default False), if True only required attributes are parsed
        :param ignore: list of str (optional), attributes not to parse

    :returns: value and unit, both converted in convert_xml_attribute
    """
    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    only_required = kwargs.get('only_required', False)

    value_dict = evaluate_tag(node, schema_dict, name, constants, parser_info_out=parser_info_out, **kwargs)

    if 'value' not in value_dict:
        parser_info_out['parser_warnings'].append(f'Failed to evaluate singleValue from tag {name}: '
                                                  "Has no 'value' attribute")
    if 'units' not in value_dict and not only_required:
        parser_info_out['parser_warnings'].append(f'Failed to evaluate singleValue from tag {name}: '
                                                  "Has no 'units' attribute")

    return value_dict


@register_parsing_function('parentAttribs', all_attribs_keys=True)
def evaluate_parent_tag(node, schema_dict, name, constants, parser_info_out=None, **kwargs):
    """
    Evaluates all attributes of the parent tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param replace_root: str, replaces the root tag (used for inserting output root to input paths)
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param only_required: bool (optional, default False), if True only required attributes are parsed
        :param ignore: list of str (optional), attributes not to parse

    :returns: dict, with attribute values converted via convert_xml_attribute
    """
    from masci_tools.util.xml.common_xml_util import eval_xpath, convert_xml_attribute, get_xml_attribute

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    contains = kwargs.get('contains', None)
    not_contains = kwargs.get('not_contains', None)
    only_required = kwargs.get('only_required', False)

    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            if contains is None:
                contains = []
            contains = set(contains)
            contains.add(node.tag)
            contains = list(contains)

    tag_xpath = get_tag_xpath(schema_dict, name, contains=contains, not_contains=not_contains)

    parent_xpath = '/'.join(tag_xpath.split('/')[:-1])

    #Which attributes are expected
    attribs = set()
    if parent_xpath in schema_dict['tag_info']:
        attribs = schema_dict['tag_info'][parent_xpath]['attribs']
        optional = schema_dict['tag_info'][parent_xpath]['optional_attribs']
    elif 'iteration_tag_info' in schema_dict:
        if parent_xpath in schema_dict['iteration_tag_info']:
            attribs = schema_dict['iteration_tag_info'][parent_xpath]['attribs']
            optional = schema_dict['iteration_tag_info'][parent_xpath]['optional_attribs']

    if only_required:
        attribs = attribs.difference(optional)

    if 'ignore' in kwargs:
        attribs = attribs.difference(kwargs.get('ignore'))

    if not attribs:
        parser_info_out['parser_warnings'].append(f'Failed to evaluate attributes from parent tag of {name}: '
                                                  'No attributes to parse either the tag does not '
                                                  'exist or it has no attributes')
    else:
        attribs = sorted(list(attribs.original_case.values()))

    elems = eval_xpath(node, tag_xpath, parser_info_out=parser_info_out, list_return=True)

    out_dict = dict.fromkeys(attribs)
    for attrib in attribs:
        out_dict[attrib] = []

    for elem in elems:
        parent = elem.getparent()
        for attrib in attribs:

            stringattribute = get_xml_attribute(parent, attrib)

            if stringattribute == '':
                parser_info_out['parser_warnings'].append(
                    f'No values found for attribute {attrib} for parent tag of {name}')
                out_dict[attrib].append(None)
                continue

            possible_types = schema_dict['attrib_types'][attrib]

            warnings = []
            value, suc = convert_xml_attribute(stringattribute, possible_types, constants, conversion_warnings=warnings)

            out_dict[attrib].append(value)

            if not suc:
                parser_info_out['parser_warnings'].append(f'Failed to evaluate attribute {attrib}: '
                                                          'Below are the warnings from convert_xml_attribute')
                for warning in warnings:
                    parser_info_out['parser_warnings'].append(warning)

    if all([len(x) == 1 for x in out_dict.values()]):
        out_dict = {key: val[0] for key, val in out_dict.items()}

    return out_dict


@register_parsing_function('exists')
def tag_exists(node, schema_dict, name, parser_info_out=None, **kwargs):
    """
    Evaluates whether the tag exists in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param replace_root: str, replaces the root tag (used for inserting output root to input paths)
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: bool, True if any nodes with the path exist
    """
    return get_number_of_nodes(node, schema_dict, name, parser_info_out=parser_info_out, **kwargs) != 0


@register_parsing_function('numberNodes')
def get_number_of_nodes(node, schema_dict, name, parser_info_out=None, **kwargs):
    """
    Evaluates the number of occurences of the tag in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param replace_root: str, replaces the root tag (used for inserting output root to input paths)

    :returns: bool, True if any nodes with the path exist
    """
    return len(eval_simple_xpath(node, schema_dict, name, parser_info_out=parser_info_out, list_return=True, **kwargs))


def eval_simple_xpath(node, schema_dict, name, parser_info_out=None, **kwargs):
    """
    Evaluates a simple xpath expression of the tag in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param parser_info_out: dict, with warnings, info, errors, ...

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param replace_root: str, replaces the root tag (used for inserting output root to input paths)
        :param list_return: bool, if True a list is always returned

    :returns: etree Elements obtained via the simple xpath expression
    """
    from masci_tools.util.xml.common_xml_util import eval_xpath

    contains = kwargs.get('contains', None)
    not_contains = kwargs.get('not_contains', None)
    list_return = kwargs.get('list_return', False)

    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            if contains is None:
                contains = []
            contains = set(contains)
            contains.add(node.tag)
            contains = list(contains)

    tag_xpath = get_tag_xpath(schema_dict, name, contains=contains, not_contains=not_contains)

    return eval_xpath(node, tag_xpath, parser_info_out=parser_info_out, list_return=list_return)
