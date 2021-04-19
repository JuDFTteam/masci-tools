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
This module provides the functionality to create/load the schema_dict for the
FleurInputSchema.xsd
"""
from .fleur_schema_parser_functions import *  #pylint: disable=unused-wildcard-import
from masci_tools.util.xml.common_functions import clear_xml
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict
from lxml import etree


def create_inpschema_dict(path):
    """
    Creates dictionary with information about the FleurInputSchema.xsd.
    The functions, whose results are added to the schema_dict and the corresponding keys
    are defined in schema_actions

    :param path: str path to the folder containing the FleurInputSchema.xsd file

    """

    #Add new functionality to this dictionary here
    schema_actions = {
        'root_tag': get_root_tag,
        'tag_paths': get_tag_paths,
        '_basic_types': get_basic_types,
        'attrib_types': extract_attribute_types,
        'simple_elements': get_basic_elements,
        'unique_attribs': get_unique_attribs,
        'unique_path_attribs': get_unique_path_attribs,
        'other_attribs': get_other_attribs,
        'omitt_contained_tags': get_omittable_tags,
        'tag_info': get_tag_info,
    }

    #print(f'processing: {path}/FleurInputSchema.xsd')
    xmlschema = etree.parse(path)
    xmlschema = clear_xml(xmlschema)

    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    inp_version = str(xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0])

    schema_dict = {}
    schema_dict['inp_version'] = inp_version
    for key, action in schema_actions.items():
        schema_dict[key] = action(xmlschema, namespaces, **schema_dict)

    #We cannot do the conversion to CaseInsensitiveDict before since we need the correct case
    #For these attributes in the attrib_path functions
    schema_dict['simple_elements'] = CaseInsensitiveDict(schema_dict['simple_elements'])

    return schema_dict
