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
from .fleur_schema_parser_functions import *  #pylint: disable=unused-wildcard-import
from masci_tools.util.xml.common_xml_util import clear_xml
from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict
from lxml import etree
from pprint import pprint
import importlib.util
import os


def create_inpschema_dict(path, save_to_file=True):
    """
    Creates dictionary with information about the FleurInputSchema.xsd and writes
    it to the same folder in a file called ```inpschema_dict.py```. The FleurInputSchema.xsd
    corresponding to the same version is expected to be in the same folder.

    The functions, whose results are added to the schema_dict and the corresponding keys
    are defined in schema_actions

    :param path: str path to the folder containing the FleurInputSchema.xsd file
    :param save_to_file: bool, if True the schema_dict is saved to a ```inpschema_dict.py```
                         file in the folder with the corresponding version number
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

    print(f'processing: {path}/FleurInputSchema.xsd')
    xmlschema = etree.parse(f'{path}/FleurInputSchema.xsd')
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

    docstring = '\n'\
                'This file contains information parsed from the FleurInputSchema.xsd\n'\
                f'for version {inp_version}\n'\
                '\n'\
                'The keys contain the following information:\n'\
                '\n'\
                "    - 'inp_version': Version string of the input schema represented in this file\n"\
                "    - 'tag_paths': simple xpath expressions to all valid tag names\n"\
                '                   Multiple paths or ambiguous tag names are parsed as a list\n'\
                "    - '_basic_types': Parsed definitions of all simple Types with their respective\n"\
                '                      base type (int, float, ...) and evtl. length restrictions\n'\
                '                     (Only used in the schema construction itself)\n'\
                "    - 'attrib_types': All possible base types for all valid attributes. If multiple are\n"\
                "                      possible a list, with 'string' always last (if possible)\n"\
                "    - 'simple_elements': All elements with simple types and their type definition\n"\
                '                         with the additional attributes\n'\
                "    - 'unique_attribs': All attributes and their paths, which occur only once and\n"\
                '                        have a unique path\n'\
                "    - 'unique_path_attribs': All attributes and their paths, which have a unique path\n"\
                '                             but occur in multiple places\n'\
                "    - 'other_attribs': All attributes and their paths, which are not in 'unique_attribs' or\n"\
                "                       'unique_path_attribs'\n"\
                "    - 'omitt_contained_tags': All tags, which only contain a list of one other tag\n"\
                "    - 'tag_info': For each tag (path), the valid attributes and tags (optional, several,\n"\
                '                  order, simple, text)\n'

    if save_to_file:
        with open(f'{path}/inpschema_dict.py', 'w') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            f.write(f'"""{docstring}"""\n')
            f.write(
                'from masci_tools.util.case_insensitive_dict import CaseInsensitiveDict, CaseInsensitiveFrozenSet\n')
            f.write(f"__inp_version__ = '{inp_version}'\n")
            f.write('schema_dict = ')
            pprint(schema_dict, f)
    else:
        return schema_dict, inp_version


def load_inpschema(version, schema_return=False, create=True, parser_info_out=None, show_help=False):
    """
    load the FleurInputSchema dict for the specified version

    :param version: str with the desired version, e.g. '0.33'
    :param schema_return: bool, if True also a etree XMLSchema object is returned
    :param create: bool, if True and the schema_dict does not exist it is created
                   via :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.create_inpschema_dict()`
    :param parser_info_out: dict with warnings, errors and information, ...
    :param show_help: bool, if True a explanation of the keys in the schema dictionary is printed

    :return: python dictionary with the schema information
    """
    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    fleur_schema_path = f'./{version}'

    path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))

    schema_file_path = os.path.join(path, 'FleurInputSchema.xsd')
    schema_dict_path = os.path.join(path, 'inpschema_dict.py')

    if not os.path.isfile(schema_file_path):
        latest_version = 0
        #Get latest version available
        for root, dirs, files in os.walk(PACKAGE_DIRECTORY):
            for folder in dirs:
                if '0.' in folder:
                    latest_version = max(latest_version, int(folder.split('.')[1]))

        if int(version.split('.')[1]) < latest_version:
            message = f'No FleurInputSchema.xsd found at {path}'
            raise FileNotFoundError(message)
        else:
            latest_version = f'0.{latest_version}'
            parser_info_out['parser_warnings'].append(
                f"No Input Schema available for version '{version}'; falling back to '{latest_version}'")

            fleur_schema_path = f'./{latest_version}'

            path = os.path.abspath(os.path.join(PACKAGE_DIRECTORY, fleur_schema_path))

            schema_file_path = os.path.join(path, 'FleurInputSchema.xsd')
            schema_dict_path = os.path.join(path, 'inpschema_dict.py')

    if not os.path.isfile(schema_dict_path):
        if create:
            parser_info_out['parser_warnings'].append(
                f'Generating schema_dict file for given input schema: {schema_file_path}')
            create_inpschema_dict(path)
        else:
            raise FileNotFoundError(f'No inpschema_dict generated for FleurInputSchema.xsd at {path}')

    #import schema_dict
    spec = importlib.util.spec_from_file_location('schema', schema_dict_path)
    schema = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(schema)
    schema_dict = schema.schema_dict

    if show_help:
        help(schema)

    if schema_return:
        xmlschema_doc = etree.parse(schema_file_path)
        xmlschema = etree.XMLSchema(xmlschema_doc)

    if schema_return:
        return schema_dict, xmlschema
    else:
        return schema_dict
