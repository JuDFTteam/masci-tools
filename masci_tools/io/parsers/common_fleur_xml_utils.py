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
from masci_tools.io.parsers.schema_dict_utils import get_tag_xpath


def clear_xml(tree, schema_dict=None):
    """
    Removes comments and executes xinclude tags of an
    xml tree.

    :param tree: an xml-tree which will be processes
    :return cleared_tree: an xml-tree without comments and with replaced xinclude tags
    """
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
            except (ValueError,KeyError):
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


def convert_xml_attribute(stringattribute, possible_types):

    if not isinstance(possible_types, list):
        possible_types = [possible_types]

    for value_type in possible_types:
        if value_type == 'float':
            converted_value, suc = convert_to_float(stringattribute)
        elif value_type == 'int':
            converted_value, suc = convert_to_int(stringattribute)
        elif value_type == 'switch':
            converted_value, suc = convert_from_fortran_bool(stringattribute)
        elif value_type == 'string':
            suc = True
            converted_value = str(stringattribute)
        if suc:
            return converted_value

    return None


def convert_to_float(value_string):
    """
    Tries to make a float out of a string. If it can't it logs a warning
    and returns True or False if convertion worked or not.

    :param value_string: a string
    :returns value: the new float or value_string: the string given
    :returns: True if convertation was successfull, False otherwise
    """
    try:
        value = float(value_string)
    except (TypeError, ValueError):
        return value_string, False
    return value, True


def convert_to_int(value_string):
    """
    Tries to make a int out of a string. If it can't it logs a warning
    and returns True or False if convertion worked or not.

    :param value_string: a string
    :returns value: the new int or value_string: the string given
    :returns: True or False
    """
    try:
        value = int(value_string)
    except (TypeError, ValueError):
        return value_string, False
    return value, True


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
            return False, True
        if stringbool in true_items:
            return True, True
        else:
            return stringbool, False
    elif isinstance(stringbool, bool):
        return stringbool, True  # no conversion needed...
    else:
        return stringbool, False


def delete_att(xmltree, xpath, attrib):
    """
    Deletes an xml tag in an xmletree.

    :param xmltree: an xmltree that represents inp.xml
    :param xpathn: a path to the attribute to be deleted
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
