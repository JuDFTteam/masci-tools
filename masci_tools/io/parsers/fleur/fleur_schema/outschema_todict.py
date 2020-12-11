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


def create_outschema_dict(path, save_to_file=True):
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
        'basic_types': get_basic_types,
        'attrib_types': extract_attribute_types,
        'simple_elements': get_basic_elements,
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

    print(f'processing: {path}/FleurOutputSchema.xsd')
    xmlschema = etree.parse(f'{path}/FleurOutputSchema.xsd')
    xmlschema = clear_xml(xmlschema)

    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    out_version = xmlschema.xpath('/xsd:schema/@version', namespaces=namespaces)[0]
    inpschema_dict = load_inpschema(out_version)  #Used to make type definitions available without reparsing inputSchema

    schema_dict = {}
    for key, action in schema_actions.items():
        addargs = {'input_basic_types': inpschema_dict['basic_types']}
        if key in ['unique_attribs', 'unique_path_attribs', 'other_attribs', 'tag_paths', 'tag_info']:
            addargs['stop_iteration'] = True
        elif key in [
                'iteration_unique_attribs', 'iteration_unique_path_attribs', 'iteration_other_attribs',
                'iteration_tag_paths', 'iteration_tag_info'
        ]:
            addargs['iteration_root'] = True
            addargs['iteration'] = True
        schema_dict[key] = action(xmlschema, namespaces, **schema_dict, **addargs)

    docstring = '\n'\
                'This file contains information parsed from the FleurOutputSchema.xsd\n'\
                f'for version {out_version}\n'\
                '\n'\
                'The keys contain the following information:\n'\
                '\n'\
                "    - 'tag_paths': simple xpath expressions to all valid tag names not in an iteration\n"\
                '                   Multiple paths or ambiguous tag names are parsed as a list\n'\
                "    - 'iteration_tag_paths': simple relative xpath expressions to all valid tag names\n"\
                '                             inside an iteration. Multiple paths or ambiguous tag names\n'\
                '                             are parsed as a list\n'\
                "    - 'basic_types': Parsed definitions of all simple Types with their respective\n"\
                '                     base type (int, float, ...) and evtl. length restrictions\n'\
                "    - 'attrib_types': All possible base types for all valid attributes. If multiple are\n"\
                "                      possible a list, with 'string' always last (if possible)\n"\
                "    - 'simple_elements': All elements with simple types and their type definition\n"\
                '                         with the additional attributes\n'\
                "    - 'unique_attribs': All attributes and their paths, which occur only once and\n"\
                '                        have a unique path outside of an iteration\n'\
                "    - 'unique_path_attribs': All attributes and their paths, which have a unique path\n"\
                '                             but occur in multiple places outside of an iteration\n'\
                "    - 'other_attribs': All attributes and their paths, which are not in 'unique_attribs' or\n"\
                "                       'unique_path_attribs' outside of an iteration\n"\
                "    - 'iteration_unique_attribs': All attributes and their relative paths, which occur\n"\
                '                                  only once and have a unique path inside of an iteration\n'\
                "    - 'iteration_unique_path_attribs': All attributes and their relative paths, which have\n"\
                '                                       a unique path but occur in multiple places inside\n'\
                '                                       of an iteration\n'\
                "    - 'iteration_other_attribs': All attributes and their relative paths, which are not\n"\
                "                                 in 'unique_attribs' or 'unique_path_attribs' inside\n"\
                '                                 of an iteration\n'\
                "    - 'omitt_contained_tags': All tags, which only contain a list of one other tag\n"\
                "    - 'tag_info': For each tag outside of an iteration (path), the valid attributes\n"\
                '                  and tags (optional, several, order, simple, text)\n'\
                "    - 'iteration_tag_info': For each tag inside of an iteration (relative path),\n"\
                '                            the valid attributes and tags (optional, several,\n'\
                '                            order, simple, text)\n'
    if save_to_file:
        with open(f'{path}/outschema_dict.py', 'w') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            f.write(f'"""{docstring}"""\n')
            f.write(f"__out_version__ = '{out_version}'\n")
            f.write('schema_dict = ')
            pprint(schema_dict, f)
    else:
        return schema_dict, out_version


def load_outschema(version, schema_return=False, create=True):
    """
    load the FleurInputSchema dict for the specified version
    """

    PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    fleur_schema_path = f'./{version}'

    path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))

    schema_file_path = os.path.join(path, 'FleurOutputSchema.xsd')
    schema_dict_path = os.path.join(path, 'outschema_dict.py')

    if not os.path.isfile(schema_file_path):
        message = f'No FleurOutputSchema.xsd found at {path}'
        raise FileNotFoundError(message)

    if not os.path.isfile(schema_dict_path):
        if create:
            print(f'Generating schema_dict file for given output schema: {schema_file_path}')
            create_outschema_dict(path)
        else:
            raise FileNotFoundError(f'No inpschema_dict generated for FleurOutputSchema.xsd at {path}')

    #import schema_dict
    spec = importlib.util.spec_from_file_location('schema', schema_dict_path)
    schema = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schema)
    schema_dict = schema.schema_dict

    if schema_return:
        xmlschema_doc = etree.parse(schema_file_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

    if schema_return:
        return schema_dict, xmlschema
    else:
        return schema_dict
