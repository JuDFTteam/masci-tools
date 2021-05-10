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
This module contains helper functions for extracting information easily from the
schema_dicts defined for the Fleur input/output

Also provides convienient functions to use just a attribute name for extracting the
attribute from the right place in the given etree
"""
from masci_tools.util.parse_tasks_decorators import register_parsing_function
from masci_tools.util.lockable_containers import LockableList
from lxml import etree


def _find_paths(schema_dict, name, entries, contains=None, not_contains=None):
    """
    Find all paths in the schema_dict in the given entries for the given name
    and matching the contains/not_contains criteria

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path

    :returns: list of str, found xpaths matching the criteria
    """

    if contains is None:
        contains = []
    elif not isinstance(contains, (list, set)):
        contains = [contains]

    if not_contains is None:
        not_contains = []
    elif not isinstance(not_contains, (list, set)):
        not_contains = [not_contains]

    path_list = []
    for entry in entries:
        if name in schema_dict[entry]:
            entry_paths = schema_dict[entry][name]

            if not isinstance(entry_paths, LockableList):
                entry_paths = [entry_paths]
            else:
                entry_paths = entry_paths.get_unlocked()

            invalid_paths = set()
            for phrase in contains:
                for xpath in entry_paths:
                    if phrase not in xpath:
                        invalid_paths.add(xpath)

            for phrase in not_contains:
                for xpath in entry_paths:
                    if phrase in xpath:
                        invalid_paths.add(xpath)

            for invalid in invalid_paths:
                entry_paths.remove(invalid)

            path_list += entry_paths

    return path_list


def get_tag_xpath(schema_dict, name, contains=None, not_contains=None):
    """
    Tries to find a unique path from the schema_dict based on the given name of the tag
    and additional further specifications

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path

    :returns: str, xpath for the given tag

    :raises ValueError: If no unique path could be found
    """

    possible_lists = ['tag_paths']

    if 'iteration_tag_paths' in schema_dict:
        possible_lists += ['iteration_tag_paths']

    paths = _find_paths(schema_dict, name, possible_lists, contains=contains, not_contains=not_contains)

    if len(paths) == 1:
        return paths[0]
    elif len(paths) == 0:
        raise ValueError(f'The tag {name} has no possible paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}')
    else:
        raise ValueError(f'The tag {name} has multiple possible paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains} \n'
                         f'These are possible: {paths}')


def get_relative_tag_xpath(schema_dict, name, root_tag, contains=None, not_contains=None):
    """
    Tries to find a unique relative path from the schema_dict based on the given name of the tag
    name of the root, from which the path should be relative and additional further specifications

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param root_tag: str, name of the tag from which the path should be relative
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path

    :returns: str, xpath for the given tag

    :raises ValueError: If no unique path could be found
    """
    from masci_tools.util.xml.common_functions import abs_to_rel_xpath

    possible_lists = ['tag_paths']

    if 'iteration_tag_paths' in schema_dict:
        possible_lists += ['iteration_tag_paths']

    #The paths have to include the root_tag
    if contains is None:
        contains = [root_tag]
    else:
        contains = set(contains)
        contains.add(root_tag)

    paths = _find_paths(schema_dict, name, possible_lists, contains=contains, not_contains=not_contains)

    rel_paths = set()
    for xpath in paths:
        rel_paths.add(abs_to_rel_xpath(xpath, root_tag))

    if len(rel_paths) == 1:
        return rel_paths.pop()
    elif len(rel_paths) == 0:
        raise ValueError(f'The tag {name} has no possible relative paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag}')
    else:
        raise ValueError(f'The tag {name} has multiple possible relative paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag} \n'
                         f'These are possible: {rel_paths}')


def get_attrib_xpath(schema_dict, name, contains=None, not_contains=None, exclude=None, tag_name=None):
    """
    Tries to find a unique path from the schema_dict based on the given name of the attribute
    and additional further specifications

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the attribute
    :param root_tag: str, name of the tag from which the path should be relative
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

    paths = _find_paths(schema_dict, name, possible_lists, contains=contains, not_contains=not_contains)

    if len(paths) == 1:
        return paths[0]
    elif len(paths) == 0:
        raise ValueError(f'The attrib {name} has no possible paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}')
    else:
        raise ValueError(f'The attrib {name} has multiple possible paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}, exclude {exclude}\n'
                         f'These are possible: {paths}')


def get_relative_attrib_xpath(schema_dict,
                              name,
                              root_tag,
                              contains=None,
                              not_contains=None,
                              exclude=None,
                              tag_name=None):
    """
    Tries to find a unique relative path from the schema_dict based on the given name of the attribute
    name of the root, from which the path should be relative and additional further specifications

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the attribute
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path
    :param exclude: list of str, here specific types of attributes can be excluded
                    valid values are: settable, settable_contains, other
    :param tag_name: str, if given this name will be used to find a path to a tag with the
                     same name in :py:func:`get_relative_tag_xpath()`

    :returns: str, xpath for the given tag

    :raises ValueError: If no unique path could be found
    """
    from masci_tools.util.xml.common_functions import abs_to_rel_xpath

    if tag_name is not None:
        tag_xpath = get_relative_tag_xpath(schema_dict,
                                           tag_name,
                                           root_tag,
                                           contains=contains,
                                           not_contains=not_contains)

        tag_info = get_tag_info(schema_dict,
                                tag_name,
                                path_return=False,
                                multiple_paths=True,
                                contains=contains,
                                not_contains=not_contains)

        err_msg = f'No attribute {name} found at tag {tag_name}'
        if name not in tag_info['attribs']:
            raise ValueError(err_msg)

        if tag_xpath.endswith('/'):
            return f'{tag_xpath}@{name}'
        else:
            return f'{tag_xpath}/@{name}'

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

    #The paths have to include the root_tag
    if contains is None:
        contains = [root_tag]
    else:
        contains = set(contains)
        contains.add(root_tag)

    paths = _find_paths(schema_dict, name, possible_lists, contains=contains, not_contains=not_contains)

    rel_paths = set()
    for xpath in paths:
        rel_paths.add(abs_to_rel_xpath(xpath, root_tag))

    if len(rel_paths) == 1:
        return rel_paths.pop()
    elif len(rel_paths) == 0:
        raise ValueError(f'The attrib {name} has no possible relative paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag}')
    else:
        raise ValueError(f'The attrib {name} has multiple possible relative paths with the current specification.\n'
                         f'contains: {contains}, not_contains: {not_contains}, root_tag {root_tag} \n'
                         f'These are possible: {rel_paths}')


def get_tag_info(schema_dict,
                 name,
                 contains=None,
                 not_contains=None,
                 path_return=True,
                 convert_to_builtin=False,
                 multiple_paths=False,
                 parent=False):
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
    :param multiple_paths: bool, if True mulitple paths are allowed to match as long as they have the same tag_info
    :param parent: bool, if True the tag_info for the parent of the tag is returned

    :returns: dict, tag_info for the found xpath
    :returns: str, xpath to the tag if `path_return=True`
    """
    import copy
    from masci_tools.util.case_insensitive_dict import CaseInsensitiveFrozenSet
    from masci_tools.util.xml.common_functions import split_off_tag

    if multiple_paths:
        possible_lists = ['tag_paths']

        if 'iteration_tag_paths' in schema_dict:
            possible_lists += ['iteration_tag_paths']

        paths = _find_paths(schema_dict, name, possible_lists, contains=contains, not_contains=not_contains)
    else:
        paths = [get_tag_xpath(schema_dict, name, contains=contains, not_contains=not_contains)]

    tag_info = None
    for path in paths:

        if parent:
            path, _ = split_off_tag(path)

        err_msg = f'Could not fing tag_info for {path}'
        if path in schema_dict['tag_info']:
            entry = schema_dict['tag_info'][path]
        elif 'iteration_tag_info' in schema_dict:
            if path in schema_dict['iteration_tag_info']:
                entry = schema_dict['iteration_tag_info'][path]
            else:
                raise ValueError(err_msg)
        else:
            raise ValueError(err_msg)

        if tag_info is not None:
            if entry != tag_info:
                raise ValueError(f'Differing tag_info for the found paths {paths}')
        else:
            tag_info = entry

    if not multiple_paths:
        paths = paths[0]

    if convert_to_builtin:
        tag_info = {
            key: set(val.original_case.values()) if isinstance(val, CaseInsensitiveFrozenSet) else val
            for key, val in tag_info.items()
        }

    if path_return:
        return tag_info, paths
    else:
        return tag_info


def read_constants(root, schema_dict, logger=None):
    """
    Reads in the constants defined in the inp.xml
    and returns them combined with the predefined constants from
    fleur as a dictionary

    :param root: root of the etree of the inp.xml file
    :param schema_dict: schema_dictionary of the version of the file to read (inp.xml or out.xml)
    :param logger: logger object for logging warnings, errors

    :return: a python dictionary with all defined constants
    """
    from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS
    import copy
    import warnings

    defined_constants = copy.deepcopy(FLEUR_DEFINED_CONSTANTS)

    try:
        tag_exists(root, schema_dict, 'constant')
    except ValueError as err:
        if 'no possible' in str(err):
            warnings.warn('Cannot extract custom constants for the given root. Assuming defaults')
            return defined_constants
        else:
            raise

    if not tag_exists(root, schema_dict, 'constant', logger=logger):  #Avoid warnings for empty constants
        return defined_constants

    constants = evaluate_tag(root, schema_dict, 'constant', defined_constants, logger=logger)

    if constants['name'] is not None:
        if not isinstance(constants['name'], list):
            constants = {key: [val] for key, val in constants.items()}
        for name, value in zip(constants['name'], constants['value']):
            if name not in defined_constants:
                defined_constants[name] = value
            else:
                if logger is not None:
                    logger.error('Ambiguous definition of constant %s', name)
                raise KeyError(f'Ambiguous definition of constant {name}')

    return defined_constants


@register_parsing_function('attrib')
def evaluate_attribute(node, schema_dict, name, constants=None, logger=None, **kwargs):
    """
    Evaluates the value of the attribute based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the attribute
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other
        :param list_return: if True, the returned quantity is always a list even if only one element is in it
        :param optional: bool, if True and no logger given none or an empty list is returned

    :returns: list or single value, converted in convert_xml_attribute
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.converters import convert_xml_attribute

    list_return = kwargs.pop('list_return', False)
    optional = kwargs.pop('optional', False)

    attrib_xpath = None
    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            attrib_xpath = get_relative_attrib_xpath(schema_dict, name, node.tag, **kwargs)

    if attrib_xpath is None:
        attrib_xpath = get_attrib_xpath(schema_dict, name, **kwargs)

    stringattribute = eval_xpath(node, attrib_xpath, logger=logger, list_return=True)

    if len(stringattribute) == 0:
        if logger is None:
            if not optional:
                raise ValueError(f'No values found for attribute {name}')
        else:
            logger.warning('No values found for attribute %s', name)
        if list_return:
            return []
        else:
            return None

    possible_types = schema_dict['attrib_types'][name]

    converted_value, suc = convert_xml_attribute(stringattribute,
                                                 possible_types,
                                                 constants=constants,
                                                 logger=logger,
                                                 list_return=list_return)

    if not suc:
        if logger is None:
            raise ValueError(f'Failed to evaluate attribute {name}, Got value: {stringattribute}')
        else:
            logger.warning('Failed to evaluate attribute %s, Got value: %s', name, stringattribute)

    return converted_value


@register_parsing_function('text')
def evaluate_text(node, schema_dict, name, constants, logger=None, **kwargs):
    """
    Evaluates the text of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param list_return: if True, the returned quantity is always a list even if only one element is in it
        :param optional: bool, if True and no logger given none or an empty list is returned

    :returns: list or single value, converted in convert_xml_text
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.converters import convert_xml_text

    list_return = kwargs.pop('list_return', False)
    optional = kwargs.pop('optional', False)

    tag_xpath = None
    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            tag_xpath = get_relative_tag_xpath(schema_dict, name, node.tag, **kwargs)

    if tag_xpath is None:
        tag_xpath = get_tag_xpath(schema_dict, name, **kwargs)

    stringtext = eval_xpath(node, f'{tag_xpath}/text()', logger=logger, list_return=True)

    for text in stringtext.copy():
        if text.strip() == '':
            stringtext.remove(text)

    if len(stringtext) == 0:
        if logger is None:
            if not optional:
                raise ValueError(f'No text found for tag {name}')
        else:
            logger.warning('No text found for tag %s', name)
        if list_return:
            return []
        else:
            return None

    possible_definitions = schema_dict['simple_elements'][name]

    converted_value, suc = convert_xml_text(stringtext,
                                            possible_definitions,
                                            constants=constants,
                                            logger=logger,
                                            list_return=list_return)

    if not suc:
        if logger is None:
            raise ValueError(f'Failed to evaluate text for tag {name}, Got text: {stringtext}')
        else:
            logger.warning('Failed to evaluate text for tag %s, Got text: %s', name, stringtext)

    return converted_value


@register_parsing_function('allAttribs', all_attribs_keys=True)
def evaluate_tag(node, schema_dict, name, constants=None, logger=None, **kwargs):
    """
    Evaluates all attributes of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param only_required: bool (optional, default False), if True only required attributes are parsed
        :param ignore: list of str (optional), attributes not to parse
        :param list_return: if True, the returned quantity is always a list even if only one element is in it
        :param strict_missing_error: if True, and no logger is given an error is raised if any attribute is not found

    :returns: dict, with attribute values converted via convert_xml_attribute
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.converters import convert_xml_attribute

    only_required = kwargs.pop('only_required', False)
    strict_missing_error = kwargs.pop('strict_missing_error', False)
    ignore = kwargs.pop('ignore', None)
    list_return = kwargs.pop('list_return', False)

    tag_xpath = None
    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            kwargs['contains'] = set(kwargs.get('contains', []))
            kwargs['contains'].add(node.tag)
            tag_xpath = get_relative_tag_xpath(schema_dict, name, node.tag, **kwargs)

    if tag_xpath is None:
        tag_xpath = get_tag_xpath(schema_dict, name, **kwargs)

    #Which attributes are expected
    try:
        tag_info = get_tag_info(schema_dict, name, path_return=False, multiple_paths=True, **kwargs)
        attribs = tag_info['attribs']
        optional = tag_info['optional_attribs']
    except ValueError as err:
        if logger is None:
            raise ValueError(f'Failed to evaluate attributes from tag {name}: '
                             'No attributes to parse either the tag does not '
                             'exist or it has no attributes') from err
        else:
            logger.exception(
                'Failed to evaluate attributes from tag %s: '
                'No attributes to parse either the tag does not '
                'exist or it has no attributes', name)
        attribs = set()
        optional = set()

    if only_required:
        attribs = attribs.difference(optional)

    if ignore:
        attribs = attribs.difference(ignore)

    if not attribs:
        if logger is None:
            raise ValueError(f'Failed to evaluate attributes from tag {name}: '
                             'No attributes to parse either the tag does not '
                             'exist or it has no attributes')
        else:
            logger.error(
                'Failed to evaluate attributes from tag %s: '
                'No attributes to parse either the tag does not '
                'exist or it has no attributes', name)
    else:
        attribs = sorted(list(attribs.original_case.values()))

    out_dict = {}

    for attrib in attribs:

        stringattribute = eval_xpath(node, f'{tag_xpath}/@{attrib}', logger=logger, list_return=True)

        if len(stringattribute) == 0:
            if logger is None:
                if strict_missing_error and attrib not in optional:
                    raise ValueError(f'No values found for attribute {attrib} at tag {name}')
            else:
                logger.warning('No values found for attribute %s at tag %s', attrib, name)
            if list_return:
                out_dict[attrib] = []
            else:
                out_dict[attrib] = None
            continue

        possible_types = schema_dict['attrib_types'][attrib]

        out_dict[attrib], suc = convert_xml_attribute(stringattribute,
                                                      possible_types,
                                                      constants=constants,
                                                      logger=logger,
                                                      list_return=list_return)

        if not suc:
            if logger is None:
                raise ValueError(f'Failed to evaluate attribute {attrib}, Got value: {stringattribute}')
            else:
                logger.warning('Failed to evaluate attribute %s, Got value: %s', attrib, stringattribute)

    return out_dict


@register_parsing_function('singleValue', all_attribs_keys=True)
def evaluate_single_value_tag(node, schema_dict, name, constants=None, logger=None, **kwargs):
    """
    Evaluates the value and unit attribute of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param only_required: bool (optional, default False), if True only required attributes are parsed
        :param ignore: list of str (optional), attributes not to parse
        :param list_return: if True, the returned quantity is always a list even if only one element is in it
        :param strict_missing_error: if True, and no logger is given an error is raised if any attribute is not found

    :returns: value and unit, both converted in convert_xml_attribute
    """

    only_required = kwargs.get('only_required', False)
    ignore = kwargs.get('ignore', [])

    value_dict = evaluate_tag(node, schema_dict, name, constants=constants, logger=logger, **kwargs)

    if value_dict.get('value') is None:
        if logger is None:
            raise ValueError(f'Failed to evaluate singleValue from tag {name}: ' "Has no 'value' attribute")
        else:
            logger.warning('Failed to evaluate singleValue from tag %s: ' "Has no 'value' attribute", name)

    if value_dict.get('units') is None and not only_required and 'units' not in ignore:
        if logger is None:
            raise ValueError(f'Failed to evaluate singleValue from tag {name}: ' "Has no 'units' attribute")
        else:
            logger.warning('Failed to evaluate singleValue from tag %s: ' "Has no 'units' attribute", name)

    return value_dict


@register_parsing_function('parentAttribs', all_attribs_keys=True)
def evaluate_parent_tag(node, schema_dict, name, constants=None, logger=None, **kwargs):
    """
    Evaluates all attributes of the parent tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param only_required: bool (optional, default False), if True only required attributes are parsed
        :param ignore: list of str (optional), attributes not to parse
        :param list_return: if True, the returned quantity is always a list even if only one element is in it
        :param strict_missing_error: if True, and no logger is given an error is raised if any attribute is not found

    :returns: dict, with attribute values converted via convert_xml_attribute
    """
    from masci_tools.util.xml.common_functions import eval_xpath, get_xml_attribute
    from masci_tools.util.xml.converters import convert_xml_attribute

    strict_missing_error = kwargs.pop('strict_missing_error', False)
    list_return = kwargs.pop('list_return', False)
    only_required = kwargs.pop('only_required', False)
    ignore = kwargs.pop('ignore', None)

    tag_xpath = None
    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            kwargs['contains'] = set(kwargs.get('contains', []))
            kwargs['contains'].add(node.tag)
            tag_xpath = get_relative_tag_xpath(schema_dict, name, node.tag, **kwargs)

    if tag_xpath is None:
        tag_xpath = get_tag_xpath(schema_dict, name, **kwargs)

    #Which attributes are expected
    try:
        tag_info = get_tag_info(schema_dict, name, path_return=False, multiple_paths=True, parent=True, **kwargs)
        attribs = tag_info['attribs']
        optional = tag_info['optional_attribs']
    except ValueError as err:
        if logger is None:
            raise ValueError(f'Failed to evaluate attributes from parent tag of {name}: '
                             'No attributes to parse either the tag does not '
                             'exist or it has no attributes') from err
        else:
            logger.exception(
                'Failed to evaluate attributes from parent tag of %s: '
                'No attributes to parse either the tag does not '
                'exist or it has no attributes', name)
        attribs = set()
        optional = set()

    if only_required:
        attribs = attribs.difference(optional)

    if ignore is not None:
        attribs = attribs.difference(ignore)

    if not attribs:
        if logger is None:
            raise ValueError(f'Failed to evaluate attributes from parent tag of {name}: '
                             'No attributes to parse either the tag does not '
                             'exist or it has no attributes')
        else:
            logger.error(
                'Failed to evaluate attributes from parent tag of %s: '
                'No attributes to parse either the tag does not '
                'exist or it has no attributes', name)
    else:
        attribs = sorted(list(attribs.original_case.values()))

    elems = eval_xpath(node, tag_xpath, logger=logger, list_return=True)

    out_dict = {}
    for attrib in attribs:
        out_dict[attrib] = []

    for elem in elems:
        parent = elem.getparent()
        for attrib in attribs:

            stringattribute = get_xml_attribute(parent, attrib, logger=logger)

            if stringattribute is None:
                if logger is None:
                    if strict_missing_error and attrib not in optional:
                        raise ValueError(f'No values found for attribute {attrib} for parent tag of {name}')
                else:
                    logger.warning('No values found for attribute %s for parent tag of %s', attrib, name)
                out_dict[attrib].append(None)
                continue

            possible_types = schema_dict['attrib_types'][attrib]

            value, suc = convert_xml_attribute(stringattribute, possible_types, constants=constants, logger=logger)

            out_dict[attrib].append(value)

            if not suc:
                if logger is None:
                    raise ValueError(f'Failed to evaluate attribute {attrib}, Got value: {stringattribute}')
                else:
                    logger.warning('Failed to evaluate attribute %s, Got value: %s', attrib, stringattribute)

    if all(len(x) == 1 for x in out_dict.values()) and not list_return:
        out_dict = {key: val[0] for key, val in out_dict.items()}

    return out_dict


@register_parsing_function('attrib_exists')
def attrib_exists(node, schema_dict, name, logger=None, **kwargs):
    """
    Evaluates whether the attribute exists in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other

    :returns: bool, True if any tag with the attribute exists
    """
    from masci_tools.util.xml.common_functions import eval_xpath, split_off_attrib

    attrib_xpath = None
    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            attrib_xpath = get_relative_attrib_xpath(schema_dict, name, node.tag, **kwargs)

    if attrib_xpath is None:
        attrib_xpath = get_attrib_xpath(schema_dict, name, **kwargs)

    tag_xpath, attrib_name = split_off_attrib(attrib_xpath)

    tags = eval_xpath(node, tag_xpath, logger=logger, list_return=True)

    return any(attrib_name in tag.attrib for tag in tags)


@register_parsing_function('exists')
def tag_exists(node, schema_dict, name, logger=None, **kwargs):
    """
    Evaluates whether the tag exists in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: bool, True if any nodes with the path exist
    """
    return get_number_of_nodes(node, schema_dict, name, logger=logger, **kwargs) != 0


@register_parsing_function('numberNodes')
def get_number_of_nodes(node, schema_dict, name, logger=None, **kwargs):
    """
    Evaluates the number of occurences of the tag in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: bool, True if any nodes with the path exist
    """
    return len(eval_simple_xpath(node, schema_dict, name, logger=logger, list_return=True, **kwargs))


def eval_simple_xpath(node, schema_dict, name, logger=None, **kwargs):
    """
    Evaluates a simple xpath expression of the tag in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param list_return: bool, if True a list is always returned

    :returns: etree Elements obtained via the simple xpath expression
    """
    from masci_tools.util.xml.common_functions import eval_xpath

    list_return = kwargs.pop('list_return', False)

    tag_xpath = None
    if isinstance(node, etree._Element):
        if node.tag != schema_dict['root_tag'] and node.tag != 'iteration':
            tag_xpath = get_relative_tag_xpath(schema_dict, name, node.tag, **kwargs)

    if tag_xpath is None:
        tag_xpath = get_tag_xpath(schema_dict, name, **kwargs)

    return eval_xpath(node, tag_xpath, logger=logger, list_return=list_return)
