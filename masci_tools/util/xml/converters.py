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


def convert_xml_attribute(stringattribute, possible_types, constants=None, logger=None, list_return=False):
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
    from masci_tools.util.fleur_calculate_expression import calculate_expression

    if not isinstance(stringattribute, list):
        stringattribute = [stringattribute]

    exceptions = []

    converted_list = []
    all_success = True
    for attrib in stringattribute:
        for value_type in possible_types:
            if value_type == 'float':
                try:
                    converted_value = float(attrib)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'float_expression':
                if constants is None:
                    raise ValueError(
                        "For calculating attributes of the type 'float_expression' constants have to be given")
                try:
                    converted_value = calculate_expression(attrib, constants)
                except ValueError as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'int':
                try:
                    converted_value = int(attrib)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'switch':
                try:
                    converted_value = convert_from_fortran_bool(attrib)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'string':
                converted_value = str(attrib)

            converted_list.append(converted_value)
            break
        else:
            if logger is None:
                raise ValueError(f"Could not convert '{attrib}'. Tried: {possible_types}.\n"
                                 'The following errors occurred:\n   ' + '\n   '.join([str(exc) for exc in exceptions]))
            else:
                logger.warning("Could not convert '%s'. The following errors occurred:", attrib)

                for exc in exceptions:
                    logger.warning('   %s', str(exc))
                    logger.debug(exc, exc_info=exc)

            converted_list.append(attrib)
            all_success = False

    ret_value = converted_list
    if len(converted_list) == 1 and not list_return:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_attribute_to_xml(attributevalue, possible_types, logger=None, float_format='.10', list_return=False):
    """
    Tries to converts a given attributevalue to a string for a xml file according
    to the types given in possible_types.
    First succeeded conversion will be returned

    :param attributevalue: value to convert.
    :param possible_types: list of str What types it will try to convert from
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted str of the value of the first succesful conversion
    """

    if not isinstance(attributevalue, list):
        attributevalue = [attributevalue]

    possible_types = possible_types.copy()

    if 'int' in possible_types:  #Since it just converts to string
        possible_types.remove('int')
        possible_types.append('int')

    if 'string' in possible_types:  #Move string to back
        possible_types.remove('string')

    possible_types.append('string')  #Always try string

    converted_list = []
    exceptions = []
    all_success = True
    for value in attributevalue:

        for value_type in possible_types:
            if value_type in ('float', 'float_expression'):
                try:
                    converted_value = f'{value:{float_format}f}'
                except ValueError as exc:
                    exceptions.append(exc)
                    continue

            elif value_type == 'switch':
                try:
                    converted_value = convert_to_fortran_bool(value)
                except (ValueError, TypeError) as exc:
                    exceptions.append(exc)
                    continue

            elif value_type in ('string', 'int'):
                converted_value = str(value)

            converted_list.append(converted_value)
            break
        else:
            if logger is None:
                raise ValueError(f"Could not convert '{value}' to text. Tried: {possible_types}.\n"
                                 'The following errors occurred:\n   ' + '\n   '.join([str(exc) for exc in exceptions]))
            else:
                logger.warning("Could not convert '%s' to text. The following errors occurred:", value)

                for exc in exceptions:
                    logger.warning('   %s', str(exc))
                    logger.debug(exc, exc_info=exc)

            converted_list.append(value)
            all_success = False

    ret_value = converted_list
    if len(converted_list) == 1 and not list_return:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_xml_text(tagtext, possible_definitions, constants=None, logger=None, list_return=False):
    """
    Tries to converts a given string text based on the definitions (length and type).
    First succeeded conversion will be returned

    :param tagtext: str, text to convert.
    :param possible_defintions: list of dicts What types it will try to convert to
    :param constants: dict, of constants defined in fleur input
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted value of the first succesful conversion
    """

    if not isinstance(tagtext, list):
        tagtext = [tagtext]

    converted_list = []
    all_success = True
    for text in tagtext:

        base_text = text.strip()
        split_text = text.split(' ')
        while '' in split_text:
            split_text.remove('')

        text_definition = None
        for definition in possible_definitions:
            if definition['length'] == len(split_text):
                text_definition = definition

        if text_definition is None:
            for definition in possible_definitions:
                if definition['length'] == 'unbounded' or \
                   definition['length'] == 1:
                    text_definition = definition

        if text_definition is None:
            if logger is None:
                raise ValueError(f"Failed to convert '{text}', no matching definition found")
            else:
                logger.warning("Failed to convert '%s', no matching definition found", text)
            converted_list.append(text)
            all_success = False
            continue

        #Avoid splitting the text accidentally if there is no length restriction
        if text_definition['length'] == 1:
            split_text = [base_text]

        converted_text = []
        for value in split_text:
            converted_value, suc = convert_xml_attribute(value,
                                                         text_definition['type'],
                                                         constants=constants,
                                                         logger=logger)
            converted_text.append(converted_value)
            if not suc:
                all_success = False

        if len(converted_text) == 1 and text_definition['length'] != 'unbounded':
            converted_text = converted_text[0]

        converted_list.append(converted_text)

    ret_value = converted_list
    if len(converted_list) == 1 and not list_return:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_text_to_xml(textvalue, possible_definitions, logger=None, float_format='16.13', list_return=False):
    """
    Tries to convert a given list of values to str for a xml file based on the definitions (length and type).
    First succeeded conversion will be returned

    :param textvalue: value to convert
    :param possible_definitions: list of dicts What types it will try to convert to
    :param logger: logger object for logging warnings
                   if given the errors are logged and the list is returned with the unconverted values
                   otherwise a error is raised, when the first conversion fails
    :param list_return: if True, the returned quantity is always a list even if only one element is in it

    :return: The converted value of the first succesful conversion
    """

    if not isinstance(textvalue, list):
        textvalue = [textvalue]
    elif not isinstance(textvalue[0], list):
        textvalue = [textvalue]

    converted_list = []
    all_success = True
    for text in textvalue:

        if not isinstance(text, list):
            text = [text]

        text_definition = None
        for definition in possible_definitions:
            if definition['length'] == len(text):
                text_definition = definition

        if text_definition is None:
            for definition in possible_definitions:
                if definition['length'] == 'unbounded':
                    text_definition = definition

        if text_definition is None:
            if isinstance(text, str):
                converted_list.append(text)
                continue

            if logger is None:
                raise ValueError(f"Failed to convert '{text}', no matching definition found")
            else:
                logger.warning("Failed to convert '%s', no matching definition found", text)

            converted_list.append('')
            all_success = False
            continue

        converted_text = []
        for value in text:
            converted_value, suc = convert_attribute_to_xml(value,
                                                            text_definition['type'],
                                                            logger=logger,
                                                            float_format=float_format)
            converted_text.append(converted_value)
            if not suc:
                if isinstance(value, str):
                    converted_list.append(value)
                    continue
                all_success = False

        converted_list.append(' '.join(converted_text))

    ret_value = converted_list
    if len(converted_list) == 1 and not list_return:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_from_fortran_bool(stringbool):
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
        elif stringbool in true_items:
            return True
        else:
            raise ValueError(f"Could not convert: '{stringbool}' to boolean, "
                             "which is not 'True', 'False', 't', 'T', 'F' or 'f'")
    elif isinstance(stringbool, bool):
        return stringbool  # no conversion needed...

    raise TypeError(f"Could not convert: '{stringbool}' to boolean, " 'only accepts str or boolean')


def convert_to_fortran_bool(boolean):
    """
    Converts a Boolean as string to the format defined in the input

    :param boolean: either a boolean or a string ('True', 'False', 'F', 'T')

    :return: a string (either 't' or 'f')
    """

    if isinstance(boolean, bool):
        if boolean:
            return 'T'
        else:
            return 'F'
    elif isinstance(boolean, str):  # basestring):
        if boolean in ('True', 't', 'T'):
            return 'T'
        elif boolean in ('False', 'f', 'F'):
            return 'F'
        else:
            raise ValueError(f"A string: {boolean} for a boolean was given, which is not 'True',"
                             "'False', 't', 'T', 'F' or 'f'")

    raise TypeError('convert_to_fortran_bool accepts only a string or ' f'bool as argument, given {boolean} ')


def convert_fleur_lo(loelements):
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
        l_num = get_xml_attribute(element, 'l')
        n_num = get_xml_attribute(element, 'n')
        lostr = f'{n_num}{shell_map[int(l_num)]}'
        lo_string = lo_string + ' ' + lostr
    return lo_string.strip()


def convert_str_version_number(version_str):
    """
    Convert the version number as a integer for easy comparisons

    :param version_str: str of the version number, e.g. '0.33'

    :returns: tuple of ints representing the version str
    """

    version_numbers = version_str.split('.')

    if len(version_numbers) != 2:
        raise ValueError(f"Version number is malformed: '{version_str}'")

    return tuple(int(part) for part in version_numbers)
