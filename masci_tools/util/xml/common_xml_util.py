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
Common functions for parsing input/output files or XMLschemas from FLEUR
"""
from lxml import etree


def clear_xml(tree):
    """
    Removes comments and executes xinclude tags of an
    xml tree.

    :param tree: an xml-tree which will be processed

    :returns: cleared_tree, an xmltree without comments and with replaced xinclude tags
    """
    import copy

    cleared_tree = copy.deepcopy(tree)

    #find any include tags
    include_tags = eval_xpath(cleared_tree,
                              '//xi:include',
                              namespaces={'xi': 'http://www.w3.org/2001/XInclude'},
                              list_return=True)

    parents = []
    known_tags = []
    for tag in include_tags:
        parent = tag.getparent()
        parents.append(parent)
        known_tags.append({elem.tag for elem in parent})

    # replace XInclude parts to validate against schema
    if len(include_tags) != 0:
        cleared_tree.xinclude()

    # get rid of xml:base attribute in the included parts
    for parent, old_tags in zip(parents, known_tags):
        new_tags = {elem.tag for elem in parent}

        #determine the elements not in old_tags, which are in tags
        #so what should have been included
        included_tag_names = new_tags.difference(old_tags)

        #Check for emtpy set (relax.xml include may not insert something)
        if not included_tag_names:
            continue

        for tag_name in included_tag_names:
            for elem in parent:
                if elem.tag == tag_name:
                    for attribute in elem.keys():
                        if 'base' in attribute:
                            try:
                                del elem.attrib[attribute]
                            except BaseException:
                                pass

    # remove comments from inp.xml
    comments = cleared_tree.xpath('//comment()')
    for comment in comments:
        com_parent = comment.getparent()
        com_parent.remove(comment)

    return cleared_tree


def validate_xml(xmltree, schema, error_header='File does not validate'):
    """
    Checks a given xmltree against a schema and produces a nice error message
    with all the validation errors collected

    :param xmltree: xmltree of the file to validate
    :param schema: etree.XMLSchema to validate against
    :param error_header: str to lead a evtl error message with

    :raises: etree.DocumentInvalid if the schema does not validate
    """
    from itertools import groupby

    try:
        schema.assertValid(clear_xml(xmltree))
    except etree.DocumentInvalid as exc:
        error_log = sorted(schema.error_log, key=lambda x: x.message)
        error_output = []
        first_occurence = []
        for message, group in groupby(error_log, key=lambda x: x.message):
            err_occurences = list(group)
            error_message = f'Line {err_occurences[0].line}: {message}'
            error_lines = ''
            if len(err_occurences) > 1:
                error_lines = f"; This error also occured on the lines {', '.join([str(x.line) for x in err_occurences[1:]])}"
            error_output.append(f'{error_message}{error_lines} \n')
            first_occurence.append(err_occurences[0].line)

        error_output = [line for _, line in sorted(zip(first_occurence, error_output))]
        errmsg = f"{error_header}: \n{''.join(error_output)}"
        raise etree.DocumentInvalid(errmsg) from exc


def convert_xml_attribute(stringattribute, possible_types, constants=None, conversion_warnings=None):
    """
    Tries to converts a given string attribute to the types given in possible_types.
    First succeeded conversion will be returned

    :param stringattribute: str, Attribute to convert.
    :param possible_types: list of str What types it will try to convert to
    :param constants: dict, of constants defined in fleur input
    :param conversion_warnings: dict with warings about failed conversions

    :return: The converted value of the first succesful conversion
    """
    from masci_tools.util.fleur_calculate_expression import calculate_expression

    if not isinstance(stringattribute, list):
        stringattribute = [stringattribute]

    if conversion_warnings is None:
        conversion_warnings = []

    converted_list = []
    all_success = True
    for attrib in stringattribute:
        suc = False
        for value_type in possible_types:
            if value_type == 'float':
                converted_value, suc = convert_to_float(attrib, conversion_warnings=conversion_warnings)
            elif value_type == 'float_expression':
                if constants is None:
                    raise ValueError(
                        "For calculating attributes of the type 'float_expression' constants have to be given")
                try:
                    converted_value = calculate_expression(attrib, constants)
                    suc = True
                except ValueError as errmsg:
                    suc = False
                    conversion_warnings.append(f"Could not evaluate expression '{attrib}' "
                                               f'The following error was raised: {errmsg}')
            elif value_type == 'int':
                converted_value, suc = convert_to_int(attrib, conversion_warnings=conversion_warnings)
            elif value_type == 'switch':
                converted_value, suc = convert_from_fortran_bool(attrib, conversion_warnings=conversion_warnings)
            elif value_type == 'string':
                suc = True
                converted_value = str(attrib)
            if suc:
                converted_list.append(converted_value)
                break
        if not suc:
            converted_list.append(attrib)
            all_success = False

    ret_value = converted_list
    if len(converted_list) == 1:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_attribute_to_xml(attributevalue, possible_types, conversion_warnings=None, float_format='.10'):
    """
    Tries to converts a given attributevalue to a string for a xml file according
    to the types given in possible_types.
    First succeeded conversion will be returned

    :param attributevalue: value to convert.
    :param possible_types: list of str What types it will try to convert from
    :param conversion_warnings: dict with warings about failed conversions

    :return: The converted str of the value of the first succesful conversion
    """

    if not isinstance(attributevalue, list):
        attributevalue = [attributevalue]

    if conversion_warnings is None:
        conversion_warnings = []

    possible_types = possible_types.copy()

    if 'int' in possible_types:  #Since it just converts to string
        possible_types.remove('int')
        possible_types.append('int')

    if 'string' in possible_types:
        possible_types.remove('string')
    possible_types.append('string')  #Always try string

    converted_list = []
    all_success = True
    for value in attributevalue:

        suc = False
        for value_type in possible_types:
            if value_type == 'float':
                try:
                    converted_value = f'{value:{float_format}f}'
                    suc = True
                except ValueError as errmsg:
                    suc = False
                    conversion_warnings.append(f"Could not convert to float string '{value}' "
                                               f'The following error was raised: {errmsg}')
            elif value_type == 'float_expression':
                try:
                    converted_value = f'{value:{float_format}f}'
                    suc = True
                except ValueError as errmsg:
                    suc = False
                    conversion_warnings.append(f"Could not convert to float string '{value}' "
                                               f'The following error was raised: {errmsg}')
            elif value_type == 'switch':
                converted_value, suc = convert_to_fortran_bool(value, conversion_warnings=conversion_warnings)
            elif value_type in ('string', 'int'):
                suc = True
                converted_value = str(value)
            if suc:
                converted_list.append(converted_value)
                break
        if not suc:
            converted_list.append(value)
            all_success = False

    ret_value = converted_list
    if len(converted_list) == 1:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_xml_text(tagtext, possible_definitions, constants=None, conversion_warnings=None):
    """
    Tries to converts a given string text based on the definitions (length and type).
    First succeeded conversion will be returned

    :param tagtext: str, text to convert.
    :param possible_defintions: list of dicts What types it will try to convert to
    :param constants: dict, of constants defined in fleur input
    :param conversion_warnings: dict with warings about failed conversions

    :return: The converted value of the first succesful conversion
    """

    if conversion_warnings is None:
        conversion_warnings = []

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
            conversion_warnings.append(f"Failed to convert '{text}', no matching definition found ")
            converted_list.append(text)
            all_success = False
            continue

        #Avoid splitting the text accidentally if there is no length restriction
        if text_definition['length'] == 1:
            split_text = [base_text]

        converted_text = []
        for value in split_text:
            warnings = []
            converted_value, suc = convert_xml_attribute(value,
                                                         text_definition['type'],
                                                         constants=constants,
                                                         conversion_warnings=warnings)
            converted_text.append(converted_value)
            if not suc:
                all_success = False
                for warning in warnings:
                    conversion_warnings.append(warning)

        if len(converted_text) == 1 and text_definition['length'] != 'unbounded':
            converted_text = converted_text[0]

        converted_list.append(converted_text)

    ret_value = converted_list
    if len(converted_list) == 1:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_text_to_xml(textvalue, possible_definitions, conversion_warnings=None, float_format='16.13'):
    """
    Tries to convert a given list of values to str for a xml file based on the definitions (length and type).
    First succeeded conversion will be returned

    :param textvalue: value to convert
    :param possible_definitions: list of dicts What types it will try to convert to
    :param conversion_warnings: dict with warings about failed conversions

    :return: The converted value of the first succesful conversion
    """

    if conversion_warnings is None:
        conversion_warnings = []

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
            conversion_warnings.append(f"Failed to convert '{text}', no matching definition found ")
            if isinstance(text, str):
                converted_list.append(text)
                continue
            converted_list.append('')
            all_success = False
            continue

        converted_text = []
        for value in text:
            warnings = []
            converted_value, suc = convert_attribute_to_xml(value,
                                                            text_definition['type'],
                                                            conversion_warnings=warnings,
                                                            float_format=float_format)
            converted_text.append(converted_value)
            if not suc:
                if isinstance(value, str):
                    converted_list.append(value)
                    continue
                all_success = False
                for warning in warnings:
                    conversion_warnings.append(warning)

        converted_list.append(' '.join(converted_text))

    ret_value = converted_list
    if len(converted_list) == 1:
        ret_value = converted_list[0]

    return ret_value, all_success


def convert_to_float(value_string, conversion_warnings=None):
    """
    Tries to make a float out of a string. If it can't it logs a warning
    and returns True or False if convertion worked or not.

    :param value_string: a string
    :param conversion_warnings: list with warings about failed conversions

    :return: value the new float or value_string: the string given
    :return: True if convertion was successfull, False otherwise
    """
    if conversion_warnings is None:
        conversion_warnings = []
    try:
        value = float(value_string)
    except TypeError:
        conversion_warnings.append(f"Could not convert: '{value_string}' to float, TypeError")
        return value_string, False

    except ValueError:
        conversion_warnings.append(f"Could not convert: '{value_string}' to float, ValueError")
        return value_string, False

    return value, True


def convert_to_int(value_string, conversion_warnings=None):
    """
    Tries to make a int out of a string. If it can't it logs a warning
    and returns True or False if convertion worked or not.

    :param value_string: a string
    :param conversion_warnings: list with warings about failed conversions

    :return: value the new int or value_string: the string given
    :return: True or False
    """
    if conversion_warnings is None:
        conversion_warnings = []
    try:
        value = int(value_string)
    except TypeError:
        conversion_warnings.append(f"Could not convert: '{value_string}' to int, TypeError")
        return value_string, False

    except ValueError:
        conversion_warnings.append(f"Could not convert: '{value_string}' to int, ValueError")
        return value_string, False

    return value, True


def convert_from_fortran_bool(stringbool, conversion_warnings=None):
    """
    Converts a string in this case ('T', 'F', or 't', 'f') to True or False

    :param stringbool: a string ('t', 'f', 'F', 'T')
    :param conversion_warnings: list with warings about failed conversions

    :return: boolean  (either True or False)
    """
    if conversion_warnings is None:
        conversion_warnings = []
    true_items = ['True', 't', 'T']
    false_items = ['False', 'f', 'F']
    if isinstance(stringbool, str):
        if stringbool in false_items:
            converted_value = False
            suc = True
        elif stringbool in true_items:
            converted_value = True
            suc = True
        else:
            suc = False
            converted_value = stringbool
            conversion_warnings.append(f"Could not convert: '{stringbool}' to boolean, "
                                       "which is not 'True', 'False', 't', 'T', 'F' or 'f'")
    elif isinstance(stringbool, bool):
        converted_value = stringbool  # no conversion needed...
        suc = True
    else:
        suc = False
        converted_value = stringbool
        conversion_warnings.append(f"Could not convert: '{stringbool}' to boolean, " 'only accepts str or boolean')

    return converted_value, suc


def convert_to_fortran_bool(boolean, conversion_warnings=None):
    """
    Converts a Boolean as string to the format defined in the input

    :param boolean: either a boolean or a string ('True', 'False', 'F', 'T')
    :param conversion_warnings: list with warings about failed conversions

    :return: a string (either 't' or 'f')
    """
    if conversion_warnings is None:
        conversion_warnings = []

    suc = False
    new_string = None
    if isinstance(boolean, bool):
        if boolean:
            new_string = 'T'
            suc = True
        else:
            new_string = 'F'
            suc = True
    elif isinstance(boolean, str):  # basestring):
        if boolean in ('True', 't', 'T'):
            new_string = 'T'
            suc = True
        elif boolean in ('False', 'f', 'F'):
            new_string = 'F'
            suc = True
        else:
            suc = False
            conversion_warnings.append(f"A string: {boolean} for a boolean was given, which is not 'True',"
                                       "'False', 't', 'T', 'F' or 'f'")
    else:
        suc = False
        conversion_warnings.append('convert_to_fortran_bool accepts only a string or '
                                   f'bool as argument, given {boolean} ')

    return new_string, suc


def eval_xpath(node, xpath, parser_info_out=None, list_return=False, namespaces=None):
    """
    Tries to evaluate an xpath expression. If it fails it logs it.
    If a absolute path is given (starting with '/') and the tag of the node
    does not match the root.
    It will try to find the tag in the path and convert it into a relative path

    :param node: root node of an etree
    :param xpath: xpath expression (relative, or absolute)
    :param parser_info_out: dict with warnings, info, errors, ...
    :param list_return: if True, the returned quantity is always a list even if only one element is in it
    :param namespaces: dict, passed to namespaces argument in xpath call

    :returns: text, attribute or a node list
    """
    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    assert isinstance(node, (etree._Element, etree._ElementTree)), f'Wrong Type for xpath eval; Got: {type(node)}'

    if isinstance(node, etree._Element):
        if node.tag != xpath.split('/')[1] and xpath.split('/')[0] != '.':
            #absolute path with a different root tag than node
            if node.tag in xpath:
                if '@' not in xpath:
                    xpath = xpath + '/'
                xpath = xpath.replace('/'.join(xpath.split(node.tag + '/')[:-1]) + node.tag, '.')
                xpath = xpath.rstrip('/')

    try:
        if namespaces is not None:
            return_value = node.xpath(xpath, namespaces=namespaces)
        else:
            return_value = node.xpath(xpath)
    except etree.XPathEvalError:
        parser_info_out['parser_warnings'].append(f'There was a XpathEvalError on the xpath: {xpath} \n Either it does '
                                                  'not exist, or something is wrong with the expression.')
        return []  # or rather None?
    if len(return_value) == 1 and not list_return:
        return return_value[0]
    else:
        return return_value


def get_xml_attribute(node, attributename, parser_info_out=None):
    """
    Get an attribute value from a node.

    :param node: a node from etree
    :param attributename: a string with the attribute name.
    :param parser_info_out: dict with warnings, info, errors, ...
    :returns: either attributevalue, or None
    """
    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    if etree.iselement(node):
        attrib_value = node.get(attributename)
        if attrib_value:
            return attrib_value
        else:
            parser_info_out['parser_warnings'].append('Tried to get attribute: "{}" from element {}.\n '
                                                      'I recieved "{}", maybe the attribute does not exist'
                                                      ''.format(attributename, node.tag, attrib_value))
            return None
    else:  # something doesn't work here, some nodes get through here
        parser_info_out['parser_warnings'].append('Can not get attributename: "{}" from node of type {}, '
                                                  'because node is not an element of etree.'
                                                  ''.format(attributename, type(node)))
        return None


def split_off_tag(xpath):
    """
    Splits off the last part of the given xpath

    :param xpath: str of the xpath to split up
    """
    split_xpath = xpath.split('/')
    if split_xpath[-1] == '':
        return '/'.join(split_xpath[:-2]), split_xpath[-2]
    else:
        return '/'.join(split_xpath[:-1]), split_xpath[-1]


def split_off_attrib(xpath):
    """
    Splits off attribute of the given xpath (part after @)

    :param xpath: str of the xpath to split up
    """
    split_xpath = xpath.split('/@')
    assert len(split_xpath) == 2, f"Splitting off attribute failed for: '{split_xpath}'"
    return tuple(split_xpath)


def check_complex_xpath(node, base_xpath, complex_xpath):
    """
    Check that the given complex xpath produces a subset of the results
    for the simple xpath

    :param node: root node of an etree
    :param base_xpath: str of the xpath without complex syntax
    :param complex_xpath: str of the xpath to check

    :raises ValueError: If the complex_xpath does not produce a subset of the results
                        of the base_xpath
    """

    results_base = set(eval_xpath(node, base_xpath, list_return=True))
    results_complex = set(eval_xpath(node, complex_xpath, list_return=True))

    if not results_base.issuperset(results_complex):
        raise ValueError(f"Complex xpath '{complex_xpath}' is not compatible with the base_xpath '{base_xpath}'")
