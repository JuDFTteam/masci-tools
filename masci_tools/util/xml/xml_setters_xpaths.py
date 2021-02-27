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


def create_tag_schema_dict(xmltree, schema_dict, xpath, base_xpath, element, create_parents=False):

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
            xmltree = create_tag_schema_dict(xmltree, schema_dict, '/'.join(xpath.split('/')[:-1]), parent_xpath,
                                             parent_name)
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
                                         parent_xpath,
                                         tag_name,
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
    from masci_tools.util.xml.common_xml_util import convert_attribute_to_xml

    if create:
        nodes = eval_xpath_create(xmltree, schema_dict, xpath, base_xpath, create_parents=True)
    else:
        nodes = eval_xpath(xmltree, xpath, list_return=True)

    if len(nodes) == 0:
        raise ValueError(f"Could not set attribute '{attributename}' on path '{xpath}'"
                         'because atleast one subtag is missing. '
                         'Use create=True to create the subtags')

    attribs = schema_dict['tag_info'][base_xpath]['attribs']
    if attributename not in attribs:
        raise ValueError(
            f"The key '{attributename}' is not expected for this version of the input for the '{base_xpath.split('/')[-1]}' tag. "
            f'Allowed attributes are: {attribs.original_case.values()}')
    attributename = attribs.original_case[attributename]

    warnings = []
    converted_attribv, suc = convert_attribute_to_xml(attribv,
                                                      schema_dict['attrib_types'][attributename],
                                                      conversion_warnings=warnings)

    if not suc:
        raise ValueError(f"Failed to convert attribute values '{attribv}': \n" '\n'.join(warnings))

    return xml_set_attrib_value_no_create(xmltree, xpath, attributename, converted_attribv, occurrences=occurences)


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
    from masci_tools.util.xml.common_xml_util import convert_text_to_xml

    if create:
        nodes = eval_xpath_create(xmltree, schema_dict, xpath, base_xpath, create_parents=True)
    else:
        nodes = eval_xpath(xmltree, xpath, list_return=True)

    if len(nodes) == 0:
        raise ValueError(f"Could not set text on path '{xpath}' because atleast one subtag is missing. "
                         'Use create=True to create the subtags')

    print(text)
    possible_definitions = schema_dict['simple_elements'][base_xpath.split('/')[-1]]
    warnings = []
    converted_text, suc = convert_text_to_xml(text, possible_definitions, conversion_warnings=warnings)

    if not suc:
        raise ValueError(f"Failed to convert text values '{text}': \n" '\n'.join(warnings))

    return xml_set_text_no_create(xmltree, xpath, converted_text, occurrences=occurences)


def xml_set_first_text(xmltree, schema_dict, xpath, base_xpath, text, create=False):

    return xml_set_text(xmltree, schema_dict, xpath, base_xpath, text, create=create, occurences=0)


def xml_set_simple_tag(xmltree, schema_dict, xpath, base_xpath, tag_name, changes, create_parents=False):

    from masci_tools.util.xml.xml_setters_basic import delete_tag

    tag_info = schema_dict['tag_info'][base_xpath]

    tag_xpath = f'{xpath}/{tag_name}'
    tag_base_xpath = f'{base_xpath}/{tag_name}'

    if tag_name in tag_info['several']:
        #change_dict can either be a list or a dict
        if isinstance(changes, dict):
            changes = [changes]

        # policy: we DELETE all existing tags, and create new ones from the given parameters.
        delete_tag(xmltree, tag_xpath)

        for indx in range(0, len(changes)):
            create_tag_schema_dict(xmltree, schema_dict, xpath, base_xpath, tag_name, create_parents=create_parents)

        for indx, change in enumerate(changes):
            for attrib, value in change.items():
                occurrences = [
                    k * len(changes) + indx
                    for k in range(len(eval_xpath(xmltree, tag_xpath, list_return=True)) // len(changes))
                ]
                xml_set_attrib_value(xmltree,
                                     schema_dict,
                                     tag_xpath,
                                     tag_base_xpath,
                                     attrib,
                                     value,
                                     occurences=occurrences)
    else:
        if not isinstance(changes, dict):
            raise ValueError(f"Tag '{tag_name}' can only occur once. But 'set_simple_tag' got a list")

        #eval and ggf. create tag
        eval_xpath_create(xmltree, schema_dict, tag_xpath, tag_base_xpath, create_parents=create_parents)

        for attrib, value in changes.items():
            xml_set_attrib_value(xmltree, schema_dict, tag_xpath, tag_base_xpath, attrib, value)

    return xmltree


def xml_set_complex_tag(xmltree, schema_dict, xpath, base_xpath, attributedict, create=False):
    """
    Recursive Function to correctly set tags/attributes for a given tag.
    Goes through the attributedict and decides based on the schema_dict, how the corresponding
    key has to be handled.

    Supports:

        - attributes (no type checking)
        - tags with text only
        - simple tags, i.e. only attributes (can be optional single/multiple)
        - complex tags, will recursively create/modify them

    :param xmltree: xml etree of the inp.xml
    :param schema_dict: dict, represents the inputschema
    :param base_xpath: string, xpath of the tag to set without complex syntax (to get info from the schema_dict)
    :param xpath: string, actual xpath to use
    :param attributedict: dict, changes to be made

    :return xmltree: xml etree of the new inp.xml
    """
    from masci_tools.util.xml.xml_setters_basic import delete_tag

    tag_info = schema_dict['tag_info'][base_xpath]

    if create:
        #eval complex tag and ggf create
        eval_xpath_create(xmltree, schema_dict, xpath, base_xpath, create_parents=True)

    for key, val in attributedict.items():

        if key not in tag_info['complex'] | tag_info['simple'] | tag_info['attribs']:
            raise ValueError(
                f"The key '{key}' is not expected for this version of the input for the '{base_xpath.split('/')[-1]}' tag. "
                f"Allowed tags are: {sorted((tag_info['complex']|tag_info['simple']).original_case.values())}"
                f"Allowed attributes are: {sorted(tag_info['attribs'].original_case.values())}")

        key = (tag_info['complex'] | tag_info['simple'] | tag_info['attribs']).original_case[key]

        sub_xpath = f'{xpath}/{key}'
        sub_base_xpath = f'{base_xpath}/{key}'
        if key in tag_info['attribs']:
            xml_set_attrib_value(xmltree, schema_dict, xpath, base_xpath, key, val, create=create)

        elif key in tag_info['text']:
            xml_set_text(xmltree, schema_dict, sub_xpath, sub_base_xpath, val, create=create)

        elif key in tag_info['simple']:
            xml_set_simple_tag(xmltree, schema_dict, xpath, base_xpath, key, val, create_parents=create)

        elif key not in tag_info['several']:  #Complex tag but only one (electronConfig)

            # eval and ggf create tag at right place.
            eval_xpath_create(xmltree, schema_dict, sub_xpath, sub_base_xpath, create_parents=create)

            xmltree = xml_set_complex_tag(xmltree, schema_dict, sub_xpath, sub_base_xpath, val)

        else:
            # policy: we DELETE all existing tags, and create new ones from the given parameters.
            delete_tag(xmltree, sub_xpath)

            if isinstance(val, dict):
                val = [val]

            for indx in range(0, len(val)):
                create_tag_schema_dict(xmltree, schema_dict, xpath, base_xpath, key, create_parents=create)

            for indx, tagdict in enumerate(val):
                for k in range(len(eval_xpath(xmltree, sub_xpath, list_return=True)) // len(val)):
                    current_elem_xpath = f'{sub_xpath}[{k*len(val)+indx}]'
                    xmltree = xml_set_complex_tag(xmltree,
                                                  schema_dict,
                                                  current_elem_xpath,
                                                  sub_base_xpath,
                                                  tagdict,
                                                  create=create)

    return xmltree


def xml_add_number_to_attrib(xmltree,
                             schema_dict,
                             xpath,
                             base_xpath,
                             attributename,
                             add_number,
                             mode='abs',
                             occurrences=None):

    from masci_tools.util.schema_dict_util import read_constants
    from masci_tools.util.xml.common_xml_util import convert_xml_attribute

    if attributename not in schema_dict['attrib_types']:
        raise ValueError(
            f"You try to shift the attribute:'{attributename}' , but the key is unknown to the fleur plug-in")

    possible_types = schema_dict['attrib_types'][attributename]

    if not etree.iselement(xmltree):
        constants = read_constants(xmltree.getroot(), schema_dict)
    else:
        constants = read_constants(xmltree, schema_dict)

    if 'float' not in possible_types and \
       'float_expression' not in possible_types and \
       'int' not in possible_types:
        raise ValueError(f"Given attribute name '{attributename}' is not float or int")

    if not xpath.endswith(f'/@{attributename}'):
        xpath = '/@'.join([xpath, attributename])

    stringattribute = eval_xpath(xmltree, xpath)

    if isinstance(stringattribute, list):
        if len(stringattribute) == 0:
            raise ValueError(f"No attribute values found for '{attributename}'. Cannot add number")

    attribvalues, suc = convert_xml_attribute(stringattribute, possible_types, constants=constants)

    if not suc or any(value is None for value in attribvalues):
        raise ValueError(f"Something went wrong finding values found for '{attributename}'. Cannot add number")

    if not isinstance(attribvalues, list):
        attribvalues = [attribvalues]

    if mode == 'abs':
        attribvalues = [value + float(add_number) for value in attribvalues]
    elif mode == 'rel':
        attribvalues = [value * float(add_number) for value in attribvalues]

    if 'float' in possible_types or 'float_expression' in possible_types:
        pass
    elif 'int' in possible_types:
        if any(not value.is_integer() for value in attribvalues):
            raise ValueError('You are trying to write a float to an integer attribute')
        attribvalues = [int(value) for value in attribvalues]

    xmltree = xml_set_attrib_value(xmltree,
                                   schema_dict,
                                   xpath,
                                   base_xpath,
                                   attributename,
                                   attribvalues,
                                   occurences=occurrences)

    return xmltree


def xml_add_number_to_first_attrib(xmltree, schema_dict, xpath, base_xpath, attributename, add_number, mode='abs'):
    return xml_add_number_to_attrib(xmltree,
                                    schema_dict,
                                    xpath,
                                    base_xpath,
                                    attributename,
                                    add_number,
                                    mode=mode,
                                    occurrences=0)
