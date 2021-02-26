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
Functions for modifying the xml input file of Fleur with explicit xpath arguments
These can still use the schema dict for finding information about the xpath
"""
from lxml import etree
from masci_tools.util.xml.common_xml_util import eval_xpath

######################CREATING/DELETING TAGS###############################################


def create_tag_schema_dict(xmltree, schema_dict, xpath, element, base_xpath, create_parents=False):

    from masci_tools.util.xml.xml_setters_basic import create_tag_xpath

    if not etree.iselement(element):
        element_name = element
        try:
            element = etree.Element(element)
        except ValueError as exc:
            raise ValueError(f"Failed to construct etree Element from '{element_name}'") from exc
    else:
        element_name = element.tag

    tag_order = schema_dict['tag_info'][base_xpath]['order']

    if len(tag_order) == 0:
        tag_order = None

    parent_nodes = eval_xpath(xmltree, xpath, list_return=True)

    if len(parent_nodes) == 0:
        if create_parents:
            parent_xpath, parent_name = '/'.join(base_xpath.split('/')[:-1]), base_xpath.split('/')[-1]
            xmltree = create_tag_schema_dict(xmltree, schema_dict, '/'.join(xpath.split('/')[:-1]), parent_name,
                                             parent_xpath)
        else:
            raise ValueError(f"Could not create tag '{element_name}' because atleast one subtag is missing. "
                             'Use create=True to create the subtags')

    return create_tag_xpath(xmltree, xpath, element, tag_order=tag_order)


def eval_xpath_create(xmltree, schema_dict, xpath, base_xpath, create_parents=False):

    nodes = eval_xpath(xmltree, xpath, list_return=True)

    if len(nodes) == 0:
        parent_xpath, tag_name = '/'.join(base_xpath.split('/')[:-1]), base_xpath.split('/')[-1]
        xmltree = create_tag_schema_dict(xmltree,
                                         schema_dict,
                                         '/'.join(xpath.split('/')[:-1]),
                                         tag_name,
                                         parent_xpath,
                                         create_parents=create_parents)
        nodes = eval_xpath(xmltree, xpath, list_return=True)

    return nodes


def xml_set_attrib_value(xmltree,
                         schema_dict,
                         xpath,
                         base_xpath,
                         attributename,
                         attribv,
                         occurences=None,
                         create=False):

    from masci_tools.util.xml.xml_setters_basic import xml_set_attrib_value_no_create

    if create:
        nodes = eval_xpath_create(xmltree, schema_dict, xpath, base_xpath, create_parents=True)
    else:
        nodes = eval_xpath(xmltree, xpath, list_return=True)

    if len(nodes) == 0:
        raise ValueError(f"Could not set attribute '{attributename}' on path '{xpath}'"
                         'because atleast one subtag is missing. '
                         'Use create=True to create the subtags')

    attribs = schema_dict['tag_info'][base_xpath]['attribs']
    attributename = attribs.original_case(attributename)

    return xml_set_attrib_value_no_create(xmltree, xpath, attributename, attribv, occurrences=occurences)


def xml_set_first_attrib_value(xmltree, schema_dict, xpath, base_xpath, attributename, attribv, create=False):

    return xml_set_attrib_value(xmltree,
                                schema_dict,
                                xpath,
                                base_xpath,
                                attributename,
                                attribv,
                                create=create,
                                occurences=0)


def xml_set_text(xmltree, schema_dict, xpath, base_xpath, text, occurences=None, create=False):

    from masci_tools.util.xml.xml_setters_basic import xml_set_text_no_create

    if create:
        nodes = eval_xpath_create(xmltree, schema_dict, xpath, base_xpath, create_parents=True)
    else:
        nodes = eval_xpath(xmltree, xpath, list_return=True)

    if len(nodes) == 0:
        raise ValueError(f"Could not set text on path '{xpath}' because atleast one subtag is missing. "
                         'Use create=True to create the subtags')

    return xml_set_text_no_create(xmltree, xpath, text, occurrences=occurences)


def xml_set_first_text(xmltree, schema_dict, xpath, base_xpath, text, create=False):

    return xml_set_text(xmltree, schema_dict, xpath, base_xpath, text, create=create, occurences=0)
