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

Also provides convenient functions to use just a attribute name for extracting the
attribute from the right place in the given etree
"""
from __future__ import annotations

from masci_tools.io.parsers.fleur_schema import NoPathFound
from masci_tools.util.parse_tasks_decorators import register_parsing_function
from masci_tools.io.parsers import fleur_schema
from masci_tools.util.xml.common_functions import add_tag, check_complex_xpath
from masci_tools.util.xml.xpathbuilder import XPathBuilder, FilterType
from masci_tools.util.typing import XPathLike, XMLLike
from lxml import etree
from logging import Logger
import warnings
import copy
import os
from typing import Iterable, Any, overload
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore


def get_tag_xpath(schema_dict, name, contains=None, not_contains=None):
    """
    DEPRECATED

    Tries to find a unique path from the schema_dict based on the given name of the tag
    and additional further specifications

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path

    :returns: str, xpath for the given tag

    :raises ValueError: If no unique path could be found
    """
    warnings.warn('get_tag_xpath is deprecated. Use the tag_xpath method on the schema dictionary instead',
                  DeprecationWarning)
    return schema_dict.tag_xpath(name, contains=contains, not_contains=not_contains)


def get_relative_tag_xpath(schema_dict, name, root_tag, contains=None, not_contains=None):
    """
    DEPRECATED

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
    warnings.warn(
        'get_relative_tag_xpath is deprecated. Use the relative_tag_xpath method on the schema dictionary instead',
        DeprecationWarning)
    return schema_dict.relative_tag_xpath(name, root_tag, contains=contains, not_contains=not_contains)


def get_attrib_xpath(schema_dict, name, contains=None, not_contains=None, exclude=None, tag_name=None):
    """
    DEPRECATED

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
    warnings.warn('get_attrib_xpath is deprecated. Use the attrib_xpath method on the schema dictionary instead',
                  DeprecationWarning)
    return schema_dict.attrib_xpath(name,
                                    contains=contains,
                                    not_contains=not_contains,
                                    exclude=exclude,
                                    tag_name=tag_name)


def get_relative_attrib_xpath(schema_dict,
                              name,
                              root_tag,
                              contains=None,
                              not_contains=None,
                              exclude=None,
                              tag_name=None):
    """
    DEPRECATED

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
    warnings.warn(
        'get_relative_attrib_xpath is deprecated. Use the relative_attrib_xpath method on the schema dictionary instead',
        DeprecationWarning)
    return schema_dict.relative_attrib_xpath(name,
                                             root_tag,
                                             contains=contains,
                                             not_contains=not_contains,
                                             exclude=exclude,
                                             tag_name=tag_name)


def get_tag_info(schema_dict,
                 name,
                 contains=None,
                 not_contains=None,
                 path_return=True,
                 convert_to_builtin=False,
                 multiple_paths=False,
                 parent=False):
    """
    DEPRECATED

    Tries to find a unique path from the schema_dict based on the given name of the tag
    and additional further specifications and returns the tag_info entry for this tag

    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param contains: str or list of str, this string has to be in the final path
    :param not_contains: str or list of str, this string has to NOT be in the final path
    :param path_return: bool, if True the found path will be returned alongside the tag_info
    :param convert_to_builtin: bool, if True the CaseInsensitiveFrozenSets are converetd to normal sets
                               with the right case of the attributes
    :param multiple_paths: bool, if True multiple paths are allowed to match as long as they have the same tag_info
    :param parent: bool, if True the tag_info for the parent of the tag is returned

    :returns: dict, tag_info for the found xpath
    :returns: str, xpath to the tag if `path_return=True`
    """
    warnings.warn('get_tag_info is deprecated. Use the tag_info method on the schema dictionary instead',
                  DeprecationWarning)
    return schema_dict.tag_info(name,
                                contains=contains,
                                not_contains=not_contains,
                                path_return=path_return,
                                convert_to_builtin=convert_to_builtin,
                                multiple_paths=multiple_paths,
                                parent=parent)


def read_constants(root: XMLLike,
                   schema_dict: fleur_schema.SchemaDict,
                   logger: Logger | None = None) -> dict[str, float]:
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

    defined_constants = copy.deepcopy(FLEUR_DEFINED_CONSTANTS)

    try:
        tag_exists(root, schema_dict, 'constant')
    except NoPathFound:
        warnings.warn('Cannot extract custom constants for the given root. Assuming defaults')
        return defined_constants

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
def evaluate_attribute(node: XMLLike,
                       schema_dict: fleur_schema.SchemaDict,
                       name: str,
                       constants: dict[str, float] | None = None,
                       logger: Logger | None = None,
                       complex_xpath: XPathLike | None = None,
                       filters: FilterType | None = None,
                       iteration_path: bool = False,
                       **kwargs: Any) -> Any:
    """
    Evaluates the value of the attribute based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the attribute
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

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
    from masci_tools.util.xml.converters import convert_from_xml

    list_return = kwargs.pop('list_return', False)
    optional = kwargs.pop('optional', False)

    attrib_xpath = _select_attrib_xpath(node, schema_dict, name, iteration_path=iteration_path, **kwargs)

    if complex_xpath is None:
        complex_xpath = XPathBuilder(attrib_xpath, filters=filters, strict=True)
    elif filters is not None:
        if not isinstance(complex_xpath, XPathBuilder):
            raise ValueError(
                'Provide only one of filters or complex_xpath (Except when complx_xpath is given as a XPathBuilder)')
        for key, val in filters.items():
            complex_xpath.add_filter(key, val)
    check_complex_xpath(node, attrib_xpath, complex_xpath)

    stringattribute: list[str] = eval_xpath(node, complex_xpath, logger=logger, list_return=True)  #type:ignore

    if len(stringattribute) == 0:
        if logger is None:
            if not optional:
                raise ValueError(f'No values found for attribute {name}')
        else:
            logger.warning('No values found for attribute %s', name)
        if list_return:
            return []
        return None

    converted_value, suc = convert_from_xml(stringattribute,
                                            schema_dict,
                                            name,
                                            text=False,
                                            constants=constants,
                                            logger=logger,
                                            list_return=list_return)

    if not suc:
        if logger is None:
            raise ValueError(f'Failed to evaluate attribute {name}, Got value: {stringattribute}')
        logger.warning('Failed to evaluate attribute %s, Got value: %s', name, stringattribute)

    return converted_value


@register_parsing_function('text')
def evaluate_text(node: XMLLike,
                  schema_dict: fleur_schema.SchemaDict,
                  name: str,
                  constants: dict[str, float] | None = None,
                  logger: Logger | None = None,
                  complex_xpath: XPathLike | None = None,
                  iteration_path: bool = False,
                  filters: FilterType | None = None,
                  **kwargs: Any) -> Any:
    """
    Evaluates the text of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param list_return: if True, the returned quantity is always a list even if only one element is in it
        :param optional: bool, if True and no logger given none or an empty list is returned

    :returns: list or single value, converted in convert_xml_text
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.xml.converters import convert_from_xml

    list_return = kwargs.pop('list_return', False)
    optional = kwargs.pop('optional', False)

    tag_xpath = _select_tag_xpath(node, schema_dict, name, iteration_path=iteration_path, **kwargs)
    if complex_xpath is None:
        complex_xpath = XPathBuilder(tag_xpath, filters=filters, strict=True)
    elif filters is not None:
        if not isinstance(complex_xpath, XPathBuilder):
            raise ValueError(
                'Provide only one of filters or complex_xpath (Except when complx_xpath is given as a XPathBuilder)')
        for key, val in filters.items():
            complex_xpath.add_filter(key, val)

    check_complex_xpath(node, tag_xpath, complex_xpath)

    stringtext: list[str] = eval_xpath(node, add_tag(complex_xpath, 'text()'), logger=logger,
                                       list_return=True)  #type:ignore

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
        return None

    converted_value, suc = convert_from_xml(stringtext,
                                            schema_dict,
                                            name,
                                            text=True,
                                            constants=constants,
                                            logger=logger,
                                            list_return=list_return)

    if not suc:
        if logger is None:
            raise ValueError(f'Failed to evaluate text for tag {name}, Got text: {stringtext}')
        logger.warning('Failed to evaluate text for tag %s, Got text: %s', name, stringtext)

    return converted_value


@register_parsing_function('allAttribs', all_attribs_keys=True)
def evaluate_tag(node: XMLLike,
                 schema_dict: fleur_schema.SchemaDict,
                 name: str,
                 constants: dict[str, float] | None = None,
                 logger: Logger | None = None,
                 subtags: bool = False,
                 text: bool = True,
                 complex_xpath: XPathLike | None = None,
                 iteration_path: bool = False,
                 filters: FilterType | None = None,
                 **kwargs: Any) -> Any:
    """
    Evaluates all attributes of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :param subtags: optional bool, if True the subtags of the given tag are evaluated
    :param text: optional bool, if True the text of the tag is also parsed
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param only_required: bool (optional, default False), if True only required attributes are parsed
        :param ignore: list of str (optional), attributes not to parse
        :param list_return: if True, the returned quantity is always a list even if only one element is in it
        :param strict_missing_error: if True, and no logger is given an error is raised if any attribute is not found

    :returns: dict, with attribute values converted via convert_xml_attribute
    """
    from masci_tools.util.xml.common_functions import eval_xpath, split_off_tag
    from masci_tools.util.xml.converters import convert_from_xml

    only_required = kwargs.pop('only_required', False)
    strict_missing_error = kwargs.pop('strict_missing_error', False)
    ignore = kwargs.pop('ignore', None)
    list_return = kwargs.pop('list_return', False)

    tag_xpath = _select_tag_xpath(node, schema_dict, name, iteration_path=iteration_path, **kwargs)
    if complex_xpath is None:
        complex_xpath = XPathBuilder(tag_xpath, filters=filters, strict=True)
    elif filters is not None:
        if not isinstance(complex_xpath, XPathBuilder):
            raise ValueError(
                'Provide only one of filters or complex_xpath (Except when complx_xpath is given as a XPathBuilder)')
        for key, val in filters.items():
            complex_xpath.add_filter(key, val)

    check_complex_xpath(node, tag_xpath, complex_xpath)

    try:
        tag_info = _select_tag_info(node, schema_dict, name, iteration_path=iteration_path, **kwargs)
    except ValueError as err:
        if logger is None:
            raise ValueError(f'Failed to evaluate attributes from tag {name}: '
                             'No attributes to parse either the tag does not '
                             'exist or it has no attributes') from err
        logger.exception(
            'Failed to evaluate attributes from tag %s: '
            'No attributes to parse either the tag does not '
            'exist or it has no attributes', name)
        return {}

    attribs = tag_info['attribs']
    optional = tag_info['optional_attribs']
    tags = tag_info['simple'] | tag_info['complex']
    optional_tags = tag_info['optional']

    if only_required:
        attribs = attribs.difference(optional)
        tags = tags.difference(optional_tags)

    if ignore:
        attribs = attribs.difference(ignore)
        tags = tags.difference(ignore)

    parse_text = name in schema_dict['text_tags'] and text

    if not attribs and not parse_text and not tags:
        if subtags:
            return {}
        if logger is None:
            raise ValueError(f'Failed to evaluate attributes from tag {name}: '
                             'No attributes to parse either the tag does not '
                             'exist or it has no attributes')
        logger.error(
            'Failed to evaluate attributes from tag %s: '
            'No attributes to parse either the tag does not '
            'exist or it has no attributes', name)
    attrib_list = sorted(list(attribs.original_case.values()))

    out_dict: dict[str, Any] = {}

    for attrib in attrib_list:

        stringattribute: list[str] = eval_xpath(node,
                                                add_tag(complex_xpath, f'@{attrib}'),
                                                logger=logger,
                                                list_return=True)  #type:ignore

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

        out_dict[attrib], suc = convert_from_xml(stringattribute,
                                                 schema_dict,
                                                 attrib,
                                                 text=False,
                                                 constants=constants,
                                                 logger=logger,
                                                 list_return=list_return)
        if not suc:
            if logger is None:
                raise ValueError(f'Failed to evaluate attribute {attrib}, Got value: {stringattribute}')
            logger.warning('Failed to evaluate attribute %s, Got value: %s', attrib, stringattribute)

    if parse_text:

        _, name = split_off_tag(tag_xpath)
        stringtext: list[str] = eval_xpath(node, add_tag(complex_xpath, 'text()'), logger=logger,
                                           list_return=True)  #type:ignore

        for textval in stringtext.copy():
            if textval.strip() == '':
                stringtext.remove(textval)

        if len(stringtext) == 0:
            if logger is None:
                if not optional:
                    raise ValueError(f'No text found for tag {name}')
            else:
                logger.warning('No text found for tag %s', name)
            if list_return:
                out_dict[name] = []
            else:
                out_dict[name] = None

        out_dict[name], suc = convert_from_xml(stringtext,
                                               schema_dict,
                                               name,
                                               text=True,
                                               constants=constants,
                                               logger=logger,
                                               list_return=list_return)

    if subtags:
        for tag in tags:
            if tag in out_dict:
                if logger is None:
                    raise ValueError(f'Conflicting key {tag}: Key is already in the output dictionary')
                logger.error('Conflicting key %s: Key is already in the output dictionary', tag)
            out_dict[tag] = []

        sub_nodes: list[etree._Element] = eval_xpath(node, complex_xpath, logger=logger, list_return=True)  #type:ignore
        for sub_node in sub_nodes:
            for tag in tags:
                if tag_exists(sub_node, schema_dict, tag):
                    out_dict[tag].append(
                        evaluate_tag(sub_node,
                                     schema_dict,
                                     tag,
                                     constants=constants,
                                     logger=logger,
                                     subtags=True,
                                     ignore=ignore,
                                     only_required=only_required,
                                     strict_missing_error=strict_missing_error,
                                     list_return=list_return,
                                     text=text))

        for tag in tags:
            for indx, sub_dict in enumerate(out_dict[tag]):
                if not sub_dict:
                    out_dict[tag].remove(sub_dict)
                elif len(sub_dict) == 1 and tag in sub_dict:
                    out_dict[tag][indx] = sub_dict[tag]

        for tag in tags:
            if len(out_dict[tag]) == 1:
                out_dict[tag] = out_dict[tag][0]
            elif len(out_dict[tag]) == 0:
                out_dict.pop(tag)

    return out_dict


@register_parsing_function('singleValue', all_attribs_keys=True)
def evaluate_single_value_tag(node: XMLLike,
                              schema_dict: fleur_schema.SchemaDict,
                              name: str,
                              constants: dict[str, float] | None = None,
                              logger: Logger | None = None,
                              complex_xpath: XPathLike | None = None,
                              **kwargs: Any) -> Any:
    """
    Evaluates the value and unit attribute of the tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param only_required: bool (optional, default False), if True only required attributes are parsed
        :param ignore: list of str (optional), attributes not to parse
        :param list_return: if True, the returned quantity is always a list even if only one element is in it
        :param strict_missing_error: if True, and no logger is given an error is raised if any attribute is not found
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                               the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :returns: value and unit, both converted in convert_xml_attribute
    """

    only_required = kwargs.get('only_required', False)
    ignore = kwargs.pop('ignore', ['comment'])

    value_dict = evaluate_tag(node,
                              schema_dict,
                              name,
                              constants=constants,
                              logger=logger,
                              complex_xpath=complex_xpath,
                              ignore=ignore,
                              **kwargs)

    if value_dict.get('value') is None:
        if logger is None:
            raise ValueError(f"Failed to evaluate singleValue from tag {name}: Has no 'value' attribute")
        logger.warning("Failed to evaluate singleValue from tag %s: Has no 'value' attribute", name)

    if value_dict.get('units') is None and not only_required and 'units' not in ignore:
        if logger is None:
            raise ValueError(f"Failed to evaluate singleValue from tag {name}: Has no 'units' attribute")
        logger.warning("Failed to evaluate singleValue from tag %s: Has no 'units' attribute", name)

    return value_dict


@register_parsing_function('parentAttribs', all_attribs_keys=True)
def evaluate_parent_tag(node: XMLLike,
                        schema_dict: fleur_schema.SchemaDict,
                        name: str,
                        constants: dict[str, float] | None = None,
                        logger: Logger | None = None,
                        complex_xpath: XPathLike | None = None,
                        iteration_path: bool = False,
                        filters: FilterType | None = None,
                        **kwargs: Any) -> Any:
    """
    Evaluates all attributes of the parent tag based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param constants: dict, contains the defined constants
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :param complex_xpath: an optional xpath to use instead of the simple xpath for the evaluation
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

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
    from masci_tools.util.xml.converters import convert_from_xml

    strict_missing_error = kwargs.pop('strict_missing_error', False)
    list_return = kwargs.pop('list_return', False)
    only_required = kwargs.pop('only_required', False)
    ignore = kwargs.pop('ignore', None)

    tag_xpath = _select_tag_xpath(node, schema_dict, name, iteration_path=iteration_path, **kwargs)
    if complex_xpath is None:
        complex_xpath = XPathBuilder(tag_xpath, filters=filters, strict=True)
    elif filters is not None:
        if not isinstance(complex_xpath, XPathBuilder):
            raise ValueError(
                'Provide only one of filters or complex_xpath (Except when complx_xpath is given as a XPathBuilder)')
        for key, val in filters.items():
            complex_xpath.add_filter(key, val)

    check_complex_xpath(node, tag_xpath, complex_xpath)

    #Which attributes are expected
    try:
        tag_info = _select_tag_info(node, schema_dict, name, parent=True, iteration_path=iteration_path, **kwargs)
    except ValueError as err:
        if logger is None:
            raise ValueError(f'Failed to evaluate attributes from parent tag of {name}: '
                             'No attributes to parse either the tag does not '
                             'exist or it has no attributes') from err
        logger.exception(
            'Failed to evaluate attributes from parent tag of %s: '
            'No attributes to parse either the tag does not '
            'exist or it has no attributes', name)
        return {}

    attribs = tag_info['attribs']
    optional = tag_info['optional_attribs']

    if only_required:
        attribs = attribs.difference(optional)

    if ignore is not None:
        attribs = attribs.difference(ignore)

    if not attribs:
        if logger is None:
            raise ValueError(f'Failed to evaluate attributes from parent tag of {name}: '
                             'No attributes to parse either the tag does not '
                             'exist or it has no attributes')
        logger.error(
            'Failed to evaluate attributes from parent tag of %s: '
            'No attributes to parse either the tag does not '
            'exist or it has no attributes', name)
    attrib_list = sorted(list(attribs.original_case.values()))

    elems: list[etree._Element] = eval_xpath(node, complex_xpath, logger=logger, list_return=True)  #type:ignore

    out_dict: dict[str, Any] = {}
    for attrib in attrib_list:
        out_dict[attrib] = []

    for elem in elems:
        parent = elem.getparent()
        if parent is None:
            if logger is None:
                raise ValueError(f'No parent found tag {name}')
            logger.warning('No parent found tag %s', name)
            continue
        for attrib in attrib_list:

            try:
                stringattribute = get_xml_attribute(parent, attrib, logger=logger)
            except ValueError:
                stringattribute = None

            if stringattribute is None:
                if logger is None:
                    if strict_missing_error and attrib not in optional:
                        raise ValueError(f'No values found for attribute {attrib} for parent tag of {name}')
                else:
                    logger.warning('No values found for attribute %s for parent tag of %s', attrib, name)
                out_dict[attrib].append(None)
                continue

            value, suc = convert_from_xml(stringattribute,
                                          schema_dict,
                                          attrib,
                                          text=attrib in tag_info['text'],
                                          constants=constants,
                                          logger=logger,
                                          list_return=list_return)

            out_dict[attrib].append(value)

            if not suc:
                if logger is None:
                    raise ValueError(f'Failed to evaluate attribute {attrib}, Got value: {stringattribute}')
                logger.warning('Failed to evaluate attribute %s, Got value: %s', attrib, stringattribute)

    if all(len(x) == 1 for x in out_dict.values()) and not list_return:
        out_dict = {key: val[0] for key, val in out_dict.items()}

    return out_dict


@register_parsing_function('attrib_exists')
def attrib_exists(node: XMLLike,
                  schema_dict: fleur_schema.SchemaDict,
                  name: str,
                  logger: Logger | None = None,
                  iteration_path: bool = False,
                  filters: FilterType | None = None,
                  **kwargs: Any) -> bool:
    """
    Evaluates whether the attribute exists in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other

    :returns: bool, True if any tag with the attribute exists
    """
    from masci_tools.util.xml.common_functions import eval_xpath, split_off_attrib

    attrib_xpath = _select_attrib_xpath(node, schema_dict, name, iteration_path=iteration_path, **kwargs)
    tag_xpath, attrib_name = split_off_attrib(attrib_xpath)
    tag_xpath_builder = XPathBuilder(tag_xpath, filters=filters, strict=True)

    tags: list[etree._Element] = eval_xpath(node, tag_xpath_builder, logger=logger, list_return=True)  #type:ignore
    return any(attrib_name in tag.attrib for tag in tags)


@register_parsing_function('exists')
def tag_exists(node: XMLLike,
               schema_dict: fleur_schema.SchemaDict,
               name: str,
               logger: Logger | None = None,
               **kwargs: Any) -> bool:
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
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :returns: bool, True if any nodes with the path exist
    """
    return get_number_of_nodes(node, schema_dict, name, logger=logger, **kwargs) != 0


@register_parsing_function('numberNodes')
def get_number_of_nodes(node: XMLLike,
                        schema_dict: fleur_schema.SchemaDict,
                        name: str,
                        logger: Logger | None = None,
                        **kwargs: Any) -> int:
    """
    Evaluates the number of occurrences of the tag in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
        :param filters: Dict specifying constraints to apply on the xpath.
                        See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details

    :returns: bool, True if any nodes with the path exist
    """
    result = eval_simple_xpath(node, schema_dict, name, logger=logger, list_return=True, **kwargs)
    if not isinstance(result, list):
        raise ValueError(f'Invalid result for length determination: {str(result)}')
    return len(result)


@overload
def eval_simple_xpath(node: XMLLike,
                      schema_dict: fleur_schema.SchemaDict,
                      name: str,
                      logger: Logger | None = ...,
                      iteration_path: bool = ...,
                      filters: FilterType | None = ...,
                      list_return: Literal[True] = ...,
                      **kwargs: Any) -> list[etree._Element]:
    ...


@overload
def eval_simple_xpath(node: XMLLike,
                      schema_dict: fleur_schema.SchemaDict,
                      name: str,
                      logger: Logger | None = ...,
                      iteration_path: bool = ...,
                      filters: FilterType | None = ...,
                      list_return: Literal[False] = ...,
                      **kwargs: Any) -> etree._Element | list[etree._Element]:
    ...


def eval_simple_xpath(node: XMLLike,
                      schema_dict: fleur_schema.SchemaDict,
                      name: str,
                      logger: Logger | None = None,
                      iteration_path: bool = False,
                      filters: FilterType | None = None,
                      list_return: bool = False,
                      **kwargs: Any) -> etree._Element | list[etree._Element]:
    """
    Evaluates a simple xpath expression of the tag in the xmltree based on the given name
    and additional further specifications with the available type information

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param logger: logger object for logging warnings, errors, if not provided all errors will be raised
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
    :param filters: Dict specifying constraints to apply on the xpath.
                    See :py:class:`~masci_tools.util.xml.xpathbuilder.XPathBuilder` for details
    :param list_return: bool, if True a list is always returned

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: etree Elements obtained via the simple xpath expression
    """
    from masci_tools.util.xml.common_functions import eval_xpath

    tag_xpath = _select_tag_xpath(node, schema_dict, name, iteration_path=iteration_path, **kwargs)
    tag_xpath_builder = XPathBuilder(tag_xpath, strict=True, filters=filters)

    return eval_xpath(node, tag_xpath_builder, logger=logger, list_return=list_return)  #type: ignore[return-value]


def reverse_xinclude(xmltree: etree._ElementTree, schema_dict: fleur_schema.SchemaDict, included_tags: Iterable[str],
                     **kwargs: os.PathLike) -> tuple[etree._ElementTree, dict[os.PathLike | str, etree._ElementTree]]:
    """
    Split the xmltree back up according to the given included tags.
    The original xmltree will be returned with the corresponding xinclude tags
    and the included trees are returned in a dict mapping the inserted filename
    to the extracted tree

    Tags for which no known filename is known are returned under unknown-1.xml, ...
    The following tags have known filenames:

        - `relaxation`: ``relax.xml``
        - `kPointLists`: ``kpts.xml``
        - `symmetryOperations`: ``sym.xml``
        - `atomSpecies`: ``species.xml``
        - `atomGroups`: ``atoms.xml``

    Additional mappings can be given in the keyword arguments

    :param xmltree: an xml-tree which will be processed
    :param schema_dict: Schema dictionary containing all the necessary information
    :param included_tags: Iterable of str, containing the names of the tags to be excluded

    :returns: xmltree with the inseerted xinclude tags and a dict mapping the filenames
              to the excluded trees

    :raises ValueError: if the tag can not be found in the given xmltree
    """
    from masci_tools.util.xml.common_functions import eval_xpath

    INCLUDE_NSMAP = {'xi': 'http://www.w3.org/2001/XInclude'}
    INCLUDE_TAG = etree.QName(INCLUDE_NSMAP['xi'], 'include')
    FALLBACK_TAG = etree.QName(INCLUDE_NSMAP['xi'], 'fallback')

    excluded_tree = copy.deepcopy(xmltree)

    include_file_names: dict[str, os.PathLike | str] = {
        'relaxation': 'relax.xml',
        'kPointLists': 'kpts.xml',
        'symmetryOperations': 'sym.xml',
        'atomSpecies': 'species.xml',
        'atomGroups': 'atoms.xml'
    }

    include_file_names = {**include_file_names, **kwargs}

    unknown_file_names = 0
    included_trees = {}
    root = excluded_tree.getroot()

    if not all(isinstance(tag, str) for tag in included_tags):
        raise ValueError(f'included_tags is not made up of strings: {included_tags}')

    for tag in included_tags:
        if tag in include_file_names:
            file_name = include_file_names[tag]
        else:
            warnings.warn(f'No filename known for tag {tag}')
            unknown_file_names += 1
            file_name = f'unknown-{unknown_file_names}.xml'

        try:
            tag_xpath = schema_dict.tag_xpath(tag)
        except Exception as err:
            raise ValueError(f'Cannot determine place of included tag {tag}') from err
        included_tag_res: list[etree._Element] = eval_xpath(root, tag_xpath, list_return=True)  #type:ignore

        if len(included_tag_res) != 1:
            raise ValueError(f'Cannot determine place of included tag {tag}')
        included_tag = included_tag_res[0]

        included_trees[file_name] = etree.ElementTree(included_tag)

        parent = included_tag.getparent()
        if parent is None:
            raise ValueError('Could not find parent of included tag')

        xinclude_elem = etree.Element(INCLUDE_TAG, href=os.fspath(file_name), nsmap=INCLUDE_NSMAP)  #type:ignore
        xinclude_elem.append(etree.Element(FALLBACK_TAG))  #type:ignore

        parent.replace(included_tag, xinclude_elem)

    if 'relax.xml' not in included_trees:
        #The relax.xml include should always be there
        xinclude_elem = etree.Element(INCLUDE_TAG, href='relax.xml', nsmap=INCLUDE_NSMAP)  #type:ignore
        xinclude_elem.append(etree.Element(FALLBACK_TAG))  #type:ignore
        root.append(xinclude_elem)

    etree.indent(excluded_tree)
    for tree in included_trees.values():
        etree.indent(tree)

    return excluded_tree, included_trees


def _select_tag_xpath(node: XMLLike,
                      schema_dict: fleur_schema.SchemaDict,
                      name: str,
                      iteration_path: bool = False,
                      **kwargs: Any) -> str:
    """
    Select the simple tag xpath used for the evaluation function in this module
    based on the given node and the specifications

    1. If the node is an xmltree or an element with the tag of a root tag
       the normal tag_xpath method is used
    2. If the node is an etree Element not of an root tag the
       relative_tag_xpath method is used
    3. If iteration_path=True and the schema dict is an OutputSchemaDict
       use the iteration_tag_xpath/relative_iteration_tag_xpath according to
       the rules above

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    :returns: str of the tag xpath
    """
    if iteration_path:
        if not isinstance(schema_dict, fleur_schema.OutputSchemaDict):
            raise ValueError('iteration_path=True can only be used with OutputSchemaDict')

    root_tags: tuple[str, ...] = (schema_dict['root_tag'],)
    if isinstance(schema_dict, fleur_schema.OutputSchemaDict):
        root_tags += tuple(schema_dict['iteration_tags'])

    xpath = None
    if isinstance(node, etree._Element):
        if node.tag not in root_tags:
            if iteration_path:
                xpath = schema_dict.relative_iteration_tag_xpath(name, node.tag, **kwargs)  #type:ignore
            else:
                xpath = schema_dict.relative_tag_xpath(name, node.tag, **kwargs)

    if xpath is None:
        if iteration_path:
            xpath = schema_dict.iteration_tag_xpath(name, **kwargs)  #type:ignore
        else:
            xpath = schema_dict.tag_xpath(name, **kwargs)

    return xpath


def _select_attrib_xpath(node: XMLLike,
                         schema_dict: fleur_schema.SchemaDict,
                         name: str,
                         iteration_path: bool = False,
                         **kwargs: Any) -> str:
    """
    Select the simple attrib xpath used for the evaluation function in this module
    based on the given node and the specifications

    1. If the node is an xmltree or an element with the tag of a root tag
       the normal attrib_xpath method is used
    2. If the node is an etree Element not of an root tag the
       relative_attrib_xpath method is used
    3. If iteration_path=True and the schema dict is an OutputSchemaDict
       use the iteration_attrib_xpath/relative_iteration_attrib_xpath according to
       the rules above

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the attribute
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed

    Kwargs:
        :param tag_name: str, name of the tag where the attribute should be parsed
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path
        :param exclude: list of str, here specific types of attributes can be excluded
                        valid values are: settable, settable_contains, other

    :returns: str of the tag xpath
    """
    if iteration_path:
        if not isinstance(schema_dict, fleur_schema.OutputSchemaDict):
            raise ValueError('iteration_path=True can only be used with OutputSchemaDict')

    root_tags: tuple[str, ...] = (schema_dict['root_tag'],)
    if isinstance(schema_dict, fleur_schema.OutputSchemaDict):
        root_tags += tuple(schema_dict['iteration_tags'])

    xpath = None
    if isinstance(node, etree._Element):
        if node.tag not in root_tags:
            if iteration_path:
                xpath = schema_dict.relative_iteration_attrib_xpath(name, node.tag, **kwargs)  #type:ignore
            else:
                xpath = schema_dict.relative_attrib_xpath(name, node.tag, **kwargs)

    if xpath is None:
        if iteration_path:
            xpath = schema_dict.iteration_attrib_xpath(name, **kwargs)  #type:ignore
        else:
            xpath = schema_dict.attrib_xpath(name, **kwargs)

    return xpath


def _select_tag_info(node: XMLLike,
                     schema_dict: fleur_schema.SchemaDict,
                     name: str,
                     iteration_path: bool = False,
                     iteration_tag: str = 'iteration',
                     contains: str | Iterable[str] | None = None,
                     **kwargs: Any) -> fleur_schema.schema_dict.TagInfo:
    """
    Get the tag information used for the evaluation function in this module
    based on the given node and the specifications

    :param node: etree Element, on which to execute the xpath evaluations
    :param schema_dict: dict, containing all the path information and more
    :param name: str, name of the tag
    :param iteration_path: bool if True and the SchemaDict is of an output schema an absolute path into
                           the iteration element is constructed
    :param iteration_tag: name of the iteration tag. Onlt used for iteration_path=True

    Kwargs:
        :param contains: str, this string has to be in the final path
        :param not_contains: str, this string has to NOT be in the final path

    All other Kwargs are passed on to the tag_info method

    :returns: dict with the tag information
    """

    if contains is None:
        contains = set()
    elif isinstance(contains, str):
        contains = {contains}
    else:
        contains = set(contains)

    if iteration_path:
        if not isinstance(schema_dict, fleur_schema.OutputSchemaDict):
            raise ValueError('iteration_path=True can only be used with OutputSchemaDict')

    root_tags: tuple[str, ...] = (schema_dict['root_tag'],)
    if isinstance(schema_dict, fleur_schema.OutputSchemaDict):
        root_tags += tuple(schema_dict['iteration_tags'])

    if isinstance(node, etree._Element):
        if node.tag not in root_tags:
            if iteration_path:
                iteration_xpath = schema_dict.tag_xpath(iteration_tag)
                if f'/{node.tag}' not in iteration_xpath:
                    contains.add(node.tag)
            else:
                contains.add(node.tag)

    return schema_dict.tag_info(name, contains=contains, **kwargs)
