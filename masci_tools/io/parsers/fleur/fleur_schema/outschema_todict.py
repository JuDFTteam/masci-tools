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
import copy
from collections import UserList


def create_outschema_dict(path, inpschema_dict):
    """
    Creates dictionary with information about the FleurOutputSchema.xsd.
    The functions, whose results are added to the schema_dict and the corresponding keys
    are defined in schema_actions

    :param path: str path to the folder containing the FleurOutputSchema.xsd file
    :param inp_path: str path to the FleurInputSchema.xsd file (defaults to the same folder as path)
    """

    #Add new functionality to this dictionary here
    schema_actions = {
        'input_tag': get_input_tag,
        'root_tag': get_root_tag,
        '_basic_types': get_basic_types,
        'attrib_types': extract_attribute_types,
        'text_types': extract_text_types,
        'text_tags': get_text_tags,
        'tag_paths': get_tag_paths,
        'iteration_tag_paths': get_tag_paths,
        'unique_attribs': get_unique_attribs,
        'unique_path_attribs': get_unique_path_attribs,
        'other_attribs': get_other_attribs,
        'iteration_unique_attribs': get_unique_attribs,
        'iteration_unique_path_attribs': get_unique_path_attribs,
        'iteration_other_attribs': get_other_attribs,
        'tag_info': get_tag_info,
        'iteration_tag_info': get_tag_info,
        'omitt_contained_tags': get_omittable_tags,
    }

    #print(f'processing: {path}/FleurOutputSchema.xsd')
    xmlschema = etree.parse(path)
    xmlschema, _ = clear_xml(xmlschema)

    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    out_version = str(xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0])

    input_basic_types = inpschema_dict.get('_basic_types').get_unlocked()

    schema_dict = {}
    schema_dict['out_version'] = out_version
    for key, action in schema_actions.items():
        addargs = {'input_basic_types': input_basic_types}
        if key in ['unique_attribs', 'unique_path_attribs', 'other_attribs', 'tag_paths', 'tag_info']:
            addargs['stop_iteration'] = True
        elif key in [
                'iteration_unique_attribs', 'iteration_unique_path_attribs', 'iteration_other_attribs',
                'iteration_tag_paths', 'iteration_tag_info'
        ]:
            addargs['iteration_root'] = True
            addargs['iteration'] = True
        schema_dict[key] = action(xmlschema, namespaces, **schema_dict, **addargs)

    schema_dict['_input_basic_types'] = input_basic_types

    return schema_dict


def merge_schema_dicts(inputschema_dict, outputschema_dict):
    """
    Merge the information from the input schema into the outputschema
    This combines the type information and adjusts the paths from the inputschema
    to be valid in the out.xml file, i.e. `/fleurInput/cell` becomes `/fleurOutput/fleurInput/cell`
    or `/fleurOutput/inputData/cell` (depending on the version of the output)

    `_basic_types` and `_input_basic_types` stay untouched since they should not be used outside
    of the construction and are merely a informational entry

    :param inputschema_dict: schema dict for the input schema
    :param outputschema_dict: schema dict for the output schema

    :returns: schema dictionary with the information merged
    """
    merged_outschema_dict = copy.deepcopy(outputschema_dict)
    merged_outschema_dict['inp_version'] = inputschema_dict['inp_version']

    input_tag_path = outputschema_dict['tag_paths'][outputschema_dict['input_tag']]
    input_root_tag = inputschema_dict['root_tag']

    #
    # 1. Merge path entries and modify the input paths
    #
    path_entries = {'tag_paths', 'unique_attribs', 'unique_path_attribs', 'other_attribs'}
    for entry in path_entries:
        for key, val in inputschema_dict[entry].items():

            paths = merged_outschema_dict[entry].get(key, UserList())

            if not isinstance(paths, UserList):
                paths = [paths]
            paths = set(paths)

            if not isinstance(val, UserList):
                val = [val]
            new_paths = {f"{input_tag_path}{inp_path.replace(f'/{input_root_tag}','')}" for inp_path in val}

            new_paths = sorted(paths.union(new_paths))
            if len(new_paths) == 1:
                merged_outschema_dict[entry][key] = new_paths[0]
            else:
                merged_outschema_dict[entry][key] = new_paths

    #Remove the root_tag of the input if it is different from the input tag in the out.xml
    if input_root_tag != outputschema_dict['input_tag']:
        merged_outschema_dict['tag_paths'].pop(input_root_tag)

    #
    # 2. Insert tag_info paths (There is no possibility for overlap here)
    #
    new_tag_info_entries = {
        f"{input_tag_path}{path.replace(f'/{input_root_tag}','')}": info
        for path, info in inputschema_dict['tag_info'].items()
    }
    merged_outschema_dict['tag_info'].update(new_tag_info_entries)

    #
    # 3. Merge the attribute type information
    #
    for attrib, types in inputschema_dict['attrib_types'].items():
        out_types = set(merged_outschema_dict['attrib_types'].get(attrib, []))

        new_types = sorted(out_types.union(set(types)), key=type_order)

        merged_outschema_dict['attrib_types'][attrib] = new_types

    #
    # 4. Merge the definition information for text tags
    #
    for tag, types in inputschema_dict['text_types'].items():
        out_types = set(merged_outschema_dict['text_types'].get(tag, []))

        new_types = sorted(out_types.union(set(types)), key=type_order)

        merged_outschema_dict['text_types'][tag] = new_types

    merged_outschema_dict['text_tags'] = merged_outschema_dict['text_tags'] | inputschema_dict['text_tags']

    #
    # 5. Merge the omittable tags
    #
    merged_outschema_dict['omitt_contained_tags'] = sorted(
        set(merged_outschema_dict.get('omitt_contained_tags')).union(inputschema_dict.get('omitt_contained_tags')))

    return merged_outschema_dict
