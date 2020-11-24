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
This module provides the functionality to create/load the schema_dict for the
FleurInputSchema.xsd
"""
from .fleur_schema_parser_functions import *
from .inpschema_todict import load_inpschema
from masci_tools.util.xml.common_xml_util import clear_xml
from lxml import etree
from pprint import pprint
import importlib.util
import os


def create_outschema_dict(path):
    """
    Creates dictionary with information about the FleurOutputSchema.xsd and writes
    it to the same folder in a file called outschema_dict.py. The FleurInputSchema.xsd
    corresponding to the same version is expected to be in the same folder.

    The functions, whose results are added to the schema_dict and the corresponding keys
    are defined in schema_actions

    :param path: str path to the folder containing the FleurOutputSchema.xsd file
    """

    #Add new functionality to this dictionary here
    schema_actions = {
        'group_tags': get_group_tags,
        'basic_types': get_basic_types,
        'attrib_types': extract_attribute_types,
        'simple_elements': get_basic_elements,
        'tag_paths': get_tag_paths,
        'iteration_tag_paths': get_tag_paths,
        'settable_attribs': get_settable_attributes,
        'settable_contains_attribs': get_settable_contains_attributes,
        'other_attribs': get_other_attributes,
        'iteration_settable_attribs': get_settable_attributes,
        'iteration_settable_contains_attribs': get_settable_contains_attributes,
        'iteration_other_attribs': get_other_attributes,
        'tags_info': get_tag_info,
    }

    print(f'processing: {path}/FleurOutputSchema.xsd')
    xmlschema = etree.parse(f'{path}/FleurOutputSchema.xsd')
    xmlschema = clear_xml(xmlschema)

    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    out_version = xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0]
    inpschema_dict = load_inpschema(out_version)  #Used to make type definitions available without reparsing inputSchema

    schema_dict = {}
    for key, action in schema_actions.items():
        addargs = {'input_basic_types': inpschema_dict['basic_types']}
        if key in ['settable_attribs', 'settable_contains_attribs', 'other_attribs', 'tag_paths']:
            addargs['stop_group'] = True
        elif key in [
                'iteration_settable_attribs', 'iteration_settable_contains_attribs', 'iteration_other_attribs',
                'iteration_tag_paths'
        ]:
            addargs['group_root'] = True
            addargs['iteration'] = True
        schema_dict[key] = action(xmlschema, namespaces, **schema_dict, **addargs)

    with open(f'{path}/outschema_dict.py', 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n')
        f.write(f"__out_version__ = '{out_version}'\n")
        f.write('schema_dict = ')
        pprint(schema_dict, f)


def load_outschema(version, schema_return=False, return_errmsg=False):
    """
    load the FleurInputSchema dict for the specified version
    """

    PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    fleur_schema_path = f'./{version}'

    path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))

    schema_file_path = os.path.join(path, 'FleurOutputSchema.xsd')
    schema_dict_path = os.path.join(path, 'outschema_dict.py')

    success = True
    message = ''
    if not os.path.isfile(schema_file_path):
        success = False
        message = f'No output schema found at {path}'
        if not return_errmsg:
            raise ValueError(message)

    schema_dict = None
    if success:
        if not os.path.isfile(schema_dict_path):
            print(f'Generating schema_dict file for given input schema: {schema_file_path}')
            create_outschema_dict(path)

        #import schema_dict
        spec = importlib.util.spec_from_file_location('schema', schema_dict_path)
        schema = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(schema)
        schema_dict = schema.schema_dict
        success = True

    if schema_return:
        xmlschema_doc = etree.parse(schema_file_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        if return_errmsg:
            return schema_dict, xmlschema, success, message
        else:
            return schema_dict, xmlschema
    else:
        if return_errmsg:
            return schema_dict, success, message
        else:
            return schema_dict
