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
Common functions for converting types to and from XML files
"""

from typing import TYPE_CHECKING, Iterable, List, Tuple, Union, Dict, Any, cast
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore
from lxml import etree
from logging import Logger
if TYPE_CHECKING:
    from masci_tools.io.parsers import fleur_schema

BASE_TYPES = Union[Literal['int'], Literal['switch'], Literal['string'], Literal['float'], Literal['float_expression']]
CONVERTED_TYPES = Union[int, float, bool, str]


def convert_to_xml(value: Union[Any, List[Any]],
                   schema_dict: 'fleur_schema.SchemaDict',
                   name: str,
                   text: bool = False,
                   logger: Logger = None,
                   list_return: bool = False) -> Tuple[Union[str, List[str]], bool]:
    """
    Tries to converts a given string to the types specified in the schema_dict.
    First succeeded conversion will be returned

    If no logger is given and a attribute cannot be converted an error is raised

    :param stringattribute: str, Attribute to convert.
    :param schema_dict: Schema dictionary containing all the information
    :param name: name of the attribute or element
    :param text: bool, decides whether to take the definitions for text or attributes
    :param constants: dict, of constants defined in fleur input
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted value of the first successful conversion
    """

    if text:
        if name not in schema_dict['text_types']:
            raise KeyError(f'Unknown text tag: {name}')
        definitions = schema_dict['text_types'][name]
        float_format = '16.13'
    else:
        if name not in schema_dict['attrib_types']:
            raise KeyError(f'Unknown attibute name: {name}')
        definitions = schema_dict['attrib_types'][name]
        float_format = '.10'

    return convert_to_xml_explicit(value,
                                   definitions,
                                   logger=logger,
                                   list_return=list_return,
                                   float_format=float_format)


def convert_from_xml(
    xmlstring: Union[str, List[str]],
    schema_dict: 'fleur_schema.SchemaDict',
    name: str,
    text: bool = False,
    constants: Dict[str, float] = None,
    logger: Logger = None,
    list_return: bool = False
) -> Tuple[Union[CONVERTED_TYPES, List[CONVERTED_TYPES], List[Union[CONVERTED_TYPES, List[CONVERTED_TYPES]]]], bool]:
    """
    Tries to converts a given string to the types specified in the schema_dict.
    First succeeded conversion will be returned

    If no logger is given and a attribute cannot be converted an error is raised

    :param stringattribute: str, Attribute to convert.
    :param schema_dict: Schema dictionary containing all the information
    :param name: name of the attribute or element
    :param text: bool, decides whether to take the definitions for text or attributes
    :param constants: dict, of constants defined in fleur input
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted value of the first successful conversion
    """

    if not isinstance(xmlstring, list):
        xmlstring = [xmlstring]

    if text:
        if name not in schema_dict['text_types']:
            raise KeyError(f'Unknown text tag: {name}')
        definitions = schema_dict['text_types'][name]
        xmlstring = [string.strip() for string in xmlstring]
    else:
        if name not in schema_dict['attrib_types']:
            raise KeyError(f'Unknown attibute name: {name}')
        definitions = schema_dict['attrib_types'][name]

    return convert_from_xml_explicit(xmlstring,
                                     definitions,
                                     constants=constants,
                                     logger=logger,
                                     list_return=list_return)


def convert_from_xml_explicit(
    xmlstring: Union[str, List[str]],
    definitions: List['fleur_schema.AttributeType'],
    constants: Dict[str, float] = None,
    logger: Logger = None,
    list_return: bool = False
) -> Tuple[Union[CONVERTED_TYPES, List[CONVERTED_TYPES], List[Union[CONVERTED_TYPES, List[CONVERTED_TYPES]]]], bool]:
    """
    Tries to converts a given string to the types given in definitions.
    First succeeded conversion will be returned

    If no logger is given and a attribute cannot be converted an error is raised

    :param stringattribute: str, Attribute to convert.
    :param definitions: list of :py:class:`~masci_tools.io.parsers.fleur_schema.AttributeType` definitions
    :param constants: dict, of constants defined in fleur input
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted value of the first successful conversion
    """

    if not isinstance(xmlstring, list):
        xmlstring = [xmlstring]

    converted_list: List[Union[CONVERTED_TYPES, List[CONVERTED_TYPES]]] = []
    all_success = True
    for text in xmlstring:

        split_text = text.split(' ')
        while '' in split_text:
            split_text.remove('')

        text_definitions = []
        for definition in definitions:
            if definition.length == len(split_text):
                text_definitions.append(definition)

        if not text_definitions:
            for definition in definitions:
                if definition.length in ('unbounded', 1):
                    text_definitions.append(definition)

        if not text_definitions:
            if logger is None:
                raise ValueError(f"Could not convert '{text}', no matching definition found")
            logger.warning("Could not convert '%s', no matching definition found", text)
            converted_list.append(text)
            all_success = False
            continue

        types: Tuple[BASE_TYPES, ...] = tuple(definition.base_type for definition in text_definitions)  #type:ignore
        lengths = {definition.length for definition in text_definitions}

        if len(text_definitions) == 1:
            if text_definitions[0].length == 1:
                split_text = [text]

        converted_text, suc = convert_from_xml_single_values(split_text, types, constants=constants, logger=logger)

        all_success = all_success and suc

        if len(converted_text) == 1 and 'unbounded' not in lengths:
            converted_text = converted_text[0]  #type:ignore
        elif len(converted_text) == 0 and 'unbounded' not in lengths:
            converted_text = ''  #type:ignore

        converted_list.append(converted_text)

    ret_value = converted_list
    if len(converted_list) == 1 and not list_return:
        ret_value = converted_list[0]  #type:ignore

    return ret_value, all_success


def convert_to_xml_explicit(value: Union[Any, Iterable[Any]],
                            definitions: List['fleur_schema.AttributeType'],
                            logger: Logger = None,
                            float_format: str = '.10',
                            list_return: bool = False) -> Tuple[Union[str, List[str]], bool]:
    """
    Tries to convert a given list of values to str for a xml file based on the definitions (length and type).
    First succeeded conversion will be returned

    :param textvalue: value to convert
    :param definitions: list of :py:class:`~masci_tools.io.parsers.fleur_schema.AttributeType` definitions
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted value of the first succesful conversion
    """
    import numpy as np

    lengths = {definition.length for definition in definitions}

    if not isinstance(value, (list, np.ndarray)):
        value = [value]
    elif not isinstance(value[0], (list, np.ndarray)) and lengths != {1}:
        value = [value]

    converted_list = []
    all_success = True
    for val in value:

        if not isinstance(val, (list, np.ndarray)):
            val = [val]

        text_definitions = []
        for definition in definitions:
            if definition.length == len(val):
                text_definitions.append(definition)

        if not text_definitions:
            for definition in definitions:
                if definition.length == 'unbounded':
                    text_definitions.append(definition)

        if not text_definitions:
            if len(val) == 1 and isinstance(val[0], str):
                converted_list.append(val[0])
                continue

            if logger is None:
                raise ValueError(f"Could not convert '{val}', no matching definition found")
            logger.warning("Could not convert '%s', no matching definition found", val)

            converted_list.append('')
            all_success = False
            continue

        types: Tuple[BASE_TYPES, ...] = tuple(definition.base_type for definition in text_definitions)  #type:ignore

        converted_text, suc = convert_to_xml_single_values(val, types, logger=logger, float_format=float_format)
        all_success = all_success and suc

        converted_list.append(' '.join(converted_text))

    ret_value = converted_list
    if len(converted_list) == 1 and not list_return:
        ret_value = converted_list[0]  #type:ignore

    return ret_value, all_success


def convert_from_xml_single_values(xmlstring: Union[str, List[str]],
                                   possible_types: Tuple[BASE_TYPES, ...],
                                   constants: Dict[str, float] = None,
                                   logger: Logger = None) -> Tuple[List[CONVERTED_TYPES], bool]:
    """
    Tries to converts a given string attribute to the types given in possible_types.
    First succeeded conversion will be returned

    If no logger is given and a attribute cannot be converted an error is raised

    :param stringattribute: str, Attribute to convert.
    :param possible_types: list of str What types it will try to convert to
    :param constants: dict, of constants defined in fleur input
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted value of the first successful conversion
    """
    from masci_tools.util.fleur_calculate_expression import calculate_expression, MissingConstant

    if not isinstance(xmlstring, list):
        xmlstring = [xmlstring]

    converted_value: CONVERTED_TYPES
    converted_list = []
    all_success = True
    for text in xmlstring:

        exceptions: List[Exception] = []
        for value_type in possible_types:
            if value_type == 'float':
                try:
                    converted_value = float(text)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'float_expression':
                try:
                    converted_value = calculate_expression(text, constants=constants)
                except ValueError as exc:
                    exceptions.append(exc)
                    continue
                except MissingConstant as exc:
                    new_exc = MissingConstant(f'No value available for expression {exc}\n'
                                              'Please provide the value for this constant'
                                              ' by using the read_constants function for example')

                    exceptions.append(new_exc)
                    continue

            elif value_type == 'int':
                try:
                    converted_value = int(text)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'switch':
                try:
                    converted_value = convert_from_fortran_bool(text)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'string':
                converted_value = str(text)

            converted_list.append(converted_value)
            break
        else:
            if logger is None:
                raise ValueError(f"Could not convert '{text}'. Tried: {possible_types}.\n"
                                 'The following errors occurred:\n   ' +
                                 '\n   '.join([str(error) for error in exceptions]))
            logger.warning("Could not convert '%s'. The following errors occurred:", text)

            for error in exceptions:
                logger.warning('   %s', str(error))
                logger.debug(error, exc_info=error)

            converted_list.append(text)
            all_success = False

    return converted_list, all_success


def convert_to_xml_single_values(value: Union[Any, Iterable[Any]],
                                 possible_types: Tuple[BASE_TYPES, ...],
                                 logger: Logger = None,
                                 float_format: str = '.10') -> Tuple[List[str], bool]:
    """
    Tries to converts a given attributevalue to a string for a xml file according
    to the types given in possible_types.
    First succeeded conversion will be returned

    :param value: value to convert.
    :param possible_types: list of str What types it will try to convert from
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted str of the value of the first succesful conversion
    """
    import numpy as np

    if not isinstance(value, (list, np.ndarray)):
        value = [value]

    if 'string' not in possible_types:
        possible_types = possible_types + ('string',)  #Always try string

    converted_value: str
    converted_list = []
    exceptions: List[Exception] = []
    all_success = True
    for val in value:

        for value_type in possible_types:
            if value_type in ('float', 'float_expression'):
                try:
                    converted_value = f'{val:{float_format}f}'
                except ValueError as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'switch':
                try:
                    converted_value = convert_to_fortran_bool(val)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type in ('string', 'int'):
                converted_value = str(val)

            converted_list.append(converted_value)
            break
        else:
            if logger is None:
                raise ValueError(f"Could not convert '{val}' to text. Tried: {possible_types}.\n"
                                 'The following errors occurred:\n   ' +
                                 '\n   '.join([str(error) for error in exceptions]))
            logger.warning("Could not convert '%s' to text. The following errors occurred:", val)

            for error in exceptions:
                logger.warning('   %s', str(error))
                logger.debug(error, exc_info=error)

            converted_list.append(val)
            all_success = False

    return converted_list, all_success


def convert_from_fortran_bool(stringbool: Union[str, bool]) -> bool:
    """
    Converts a string in this case ('T', 'F', or 't', 'f') to True or False

    :param stringbool: a string ('t', 'f', 'F', 'T')

    :return: boolean  (either True or False)
    """

    true_items = ['True', 't', 'T']
    false_items = ['False', 'f', 'F']
    if isinstance(stringbool, str):
        if stringbool in false_items:
            return False
        if stringbool in true_items:
            return True
        raise ValueError(f"Could not convert: '{stringbool}' to boolean, "
                         "which is not 'True', 'False', 't', 'T', 'F' or 'f'")
    if isinstance(stringbool, bool):
        return stringbool  # no conversion needed...

    raise TypeError(f"Could not convert: '{stringbool}' to boolean, " 'only accepts str or boolean')


def convert_to_fortran_bool(boolean: Union[bool, str]) -> Literal['T', 'F']:
    """
    Converts a Boolean as string to the format defined in the input

    :param boolean: either a boolean or a string ('True', 'False', 'F', 'T')

    :return: a string (either 't' or 'f')
    """

    if isinstance(boolean, bool):
        if boolean:
            return 'T'
        return 'F'
    if isinstance(boolean, str):  # basestring):
        if boolean in ('True', 't', 'T'):
            return 'T'
        if boolean in ('False', 'f', 'F'):
            return 'F'
        raise ValueError(f"A string: {boolean} for a boolean was given, which is not 'True',"
                         "'False', 't', 'T', 'F' or 'f'")

    raise TypeError('convert_to_fortran_bool accepts only a string or ' f'bool as argument, given {boolean} ')


def convert_fleur_lo(loelements: List[etree._Element]) -> str:
    """
    Converts lo xml elements from the inp.xml file into a lo string for the inpgen
    """
    # Developer hint: Be careful with using '' and "", basestring and str are not the same...
    # therefore other conversion methods might fail, or the wrong format could be written.
    from masci_tools.util.xml.common_functions import get_xml_attribute

    shell_map = {0: 's', 1: 'p', 2: 'd', 3: 'f'}

    lo_string = ''
    for element in loelements:
        lo_type = get_xml_attribute(element, 'type')
        if lo_type != 'SCLO':  # non standard los not supported for now
            continue
        eDeriv = get_xml_attribute(element, 'eDeriv')
        if eDeriv != '0':  # LOs with higher derivatives are also dropped
            continue
        l_num = get_xml_attribute(element, 'l')
        n_num = get_xml_attribute(element, 'n')
        if l_num is None or n_num is None:
            raise ValueError('Failedto evaluate l and n attribute of LO element')
        lostr = f'{n_num}{shell_map[int(l_num)]}'
        lo_string = lo_string + ' ' + lostr
    return lo_string.strip()


def convert_fleur_electronconfig(econfig_element: etree._Element) -> str:
    """
    Convert electronConfig tag to eConfig string
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.util.econfig import convert_fleur_config_to_econfig

    core_config = eval_xpath(econfig_element, 'coreConfig/text()')
    valence_config = eval_xpath(econfig_element, 'valenceConfig/text()')

    if not core_config:
        core_config = ''

    if not valence_config:
        valence_config = ''

    core_config_str = convert_fleur_config_to_econfig(cast(str, core_config))
    valence_config_str = convert_fleur_config_to_econfig(cast(str, valence_config))

    return f'{core_config_str} | {valence_config_str}'


def convert_str_version_number(version_str: str) -> Tuple[int, int]:
    """
    Convert the version number as a integer for easy comparisons

    :param version_str: str of the version number, e.g. '0.33'

    :returns: tuple of ints representing the version str
    """

    version_numbers = version_str.split('.')

    if len(version_numbers) != 2:
        raise ValueError(f"Version number is malformed: '{version_str}'")

    return tuple(int(part) for part in version_numbers)  #type:ignore
