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
Common functions for parsing input/output files or XMLschemas from FLEUR
"""
from lxml import etree


def read_constants(xmltree, schema_dict, abspath=None):
    """
    Reads in the constants defined in the inp.xml
    and returns them combined with the predefined constants from
    fleur as a dictionary

    :param xmltree: xmltree of the inp.xml file
    :param schema_dict: schema_dictionary of the version of the inp.xml

    :return: a python dictionary with all defined constants
    """
    from masci_tools.util.schema_dict_util import get_tag_xpath
    import numpy as np

    #Predefined constants in the Fleur Code
    const_dict = {
        'Pi': np.pi,
        'Deg': 2 * np.pi / 360.0,
        'Ang': 1.8897261247728981,
        'nm': 18.897261247728981,
        'pm': 0.018897261247728981,
        'Bohr': 1.0
    }
    xpath_constants = get_tag_xpath(schema_dict, 'constant')
    if abspath is not None:
        xpath_constants = f'{abspath}{xpath_constants}'
    constant_elems = xmltree.xpath(xpath_constants)
    for const in constant_elems:
        name = const.attrib['name']
        value = const.attrib['value']
        if name not in const_dict:
            const_dict[name] = value
        else:
            raise KeyError(f'Ambiguous definition of key {name}')

    return const_dict


def clear_xml(tree, schema_dict=None):
    """
    Removes comments and executes xinclude tags of an
    xml tree.

    :param tree: an xml-tree which will be processes
    :return: cleared_tree, an xml-tree without comments and with replaced xinclude tags

    TODO: Currently what can be included is fleur specific.
    But this can probably easily generalized
    """
    from masci_tools.util.schema_dict_util import get_tag_xpath
    import copy

    possible_include = ['relaxation', 'atomGroups', 'atomSpecies', 'kPointLists', 'symmetryOperations']

    cleared_tree = copy.deepcopy(tree)

    # replace XInclude parts to validate against schema
    cleared_tree.xinclude()

    if schema_dict is not None:
        # get rid of xml:base attribute in the included parts
        for include_tag in possible_include:
            try:
                include_path = get_tag_xpath(schema_dict, include_tag)
            except (ValueError, KeyError):
                continue
            included_elem = tree.xpath(include_path)
            if included_elem != []:
                included_elem = included_elem[0]
                for attribute in included_elem.keys():
                    if 'base' in attribute:
                        cleared_tree = delete_att(cleared_tree, include_path, attribute)

    # remove comments from inp.xml
    comments = cleared_tree.xpath('//comment()')
    for comment in comments:
        com_parent = comment.getparent()
        com_parent.remove(comment)

    return cleared_tree


def convert_xml_attribute(stringattribute, possible_types, constants, suc_return=True, conversion_warnings=None):
    """
    Tries to converts a given string attribute to the types given in possible_types.
    First succeeded conversion will be returned

    :param stringattribute (str): Attribute to convert.
    :param possible_types (str, list of str): What types it will try to convert to
    :param constants: dict, of constants defined in fleur input
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

    if suc_return:
        return ret_value, all_success
    else:
        return ret_value


def convert_xml_text(tagtext, possible_definitions, constants, conversion_warnings=None, suc_return=True):
    """
    Tries to converts a given string text based on the definitions (length and type).
    First succeeded conversion will be returned

    :param tagtext (str): text to convert.
    :param possible_types (list of dicts): What types it will try to convert to
    :param constants: dict, of constants defined in fleur input
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
                                                         constants,
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

    if suc_return:
        return ret_value, all_success
    else:
        ret_value


def convert_to_float(value_string, conversion_warnings=None, suc_return=True):
    """
    Tries to make a float out of a string. If it can't it logs a warning
    and returns True or False if convertion worked or not.

    :param value_string: a string
    :return: value the new float or value_string: the string given
    :return: True if convertion was successfull, False otherwise
    """
    if conversion_warnings is None:
        conversion_warnings = []
    try:
        value = float(value_string)
    except TypeError:
        conversion_warnings.append(f"Could not convert: '{value_string}' to float, TypeError")
        if suc_return:
            return value_string, False
        else:
            return value_string
    except ValueError:
        conversion_warnings.append(f"Could not convert: '{value_string}' to float, ValueError")
        if suc_return:
            return value_string, False
        else:
            return value_string
    if suc_return:
        return value, True
    else:
        return value


def convert_to_int(value_string, conversion_warnings=None, suc_return=True):
    """
    Tries to make a int out of a string. If it can't it logs a warning
    and returns True or False if convertion worked or not.

    :param value_string: a string
    :return: value the new int or value_string: the string given
    :return: True or False
    """
    if conversion_warnings is None:
        conversion_warnings = []
    try:
        value = int(value_string)
    except TypeError:
        conversion_warnings.append(f"Could not convert: '{value_string}' to int, TypeError")
        if suc_return:
            return value_string, False
        else:
            return value_string
    except ValueError:
        conversion_warnings.append(f"Could not convert: '{value_string}' to int, ValueError")
        if suc_return:
            return value_string, False
        else:
            return value_string
    if suc_return:
        return value, True
    else:
        return value


def convert_from_fortran_bool(stringbool, conversion_warnings=None, suc_return=True):
    """
    Converts a string in this case ('T', 'F', or 't', 'f') to True or False

    :param stringbool: a string ('t', 'f', 'F', 'T')

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

    if suc_return:
        return converted_value, suc
    else:
        return converted_value


def eval_xpath(node, xpath, parser_info_out=None, list_return=False):
    """
    Tries to evaluate an xpath expression. If it fails it logs it.

    :param node: root node of an etree
    :param xpath: xpath expression (relative, or absolute)
    :param parser_info_out: dict with warnings, info, errors, ...
    :param list_return: if True, the returned quantity is always a list even if only one element is in it
    :returns: text, attribute or a node list
    """
    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    try:
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
            if parser_info_out:
                parser_info_out['parser_warnings'].append('Tried to get attribute: "{}" from element {}.\n '
                                                          'I recieved "{}", maybe the attribute does not exist'
                                                          ''.format(attributename, node, attrib_value))
            else:
                print(('Can not get attributename: "{}" from node "{}", '
                       'because node is not an element of etree.'
                       ''.format(attributename, node)))
            return None
    else:  # something doesn't work here, some nodes get through here
        if parser_info_out:
            parser_info_out['parser_warnings'].append('Can not get attributename: "{}" from node "{}", '
                                                      'because node is not an element of etree.'
                                                      ''.format(attributename, node))
        else:
            print(('Can not get attributename: "{}" from node "{}", '
                   'because node is not an element of etree.'
                   ''.format(attributename, node)))
        return None


def delete_att(xmltree, xpath, attrib):
    """
    Deletes an xml tag in an xmltree.

    :param xmltree: an xmltree that represents inp.xml
    :param xpath: a path to the attribute to be deleted
    :param attrib: the name of an attribute
    """
    root = xmltree.getroot()
    nodes = root.xpath(xpath)
    if nodes:
        for node in nodes:
            try:
                del node.attrib[attrib]
            except BaseException:
                pass
    return xmltree
