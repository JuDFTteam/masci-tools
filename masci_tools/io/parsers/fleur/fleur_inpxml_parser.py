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
This module contains functions to load an fleur inp.xml file, parse it with a schema
and convert its content to a dict
"""
from lxml import etree
from pprint import pprint
from itertools import groupby
from masci_tools.io.parsers.fleur.fleur_schema.schema_dict import InputSchemaDict
from masci_tools.util.xml.common_xml_util import clear_xml, convert_xml_attribute, convert_xml_text, eval_xpath
from masci_tools.util.schema_dict_util import read_constants


def inpxml_parser(inpxmlfile, version=None, parser_info_out=None):
    """
    Parses the given inp.xml file to a python dictionary utilizing the schema
    defined by the version number to validate and corretly convert to the dictionary

    :param inpxmlfile: either path to the inp.xml file, opened file handle or a xml etree to be parsed
    :param version: version string to enforce that a given schema is used
    :param parser_info_out: dict, with warnings, info, errors, ...

    :return: python dictionary with the parsed inp.xml

    :raises ValueError: If the validation against the schema failed, or an irrecoverable error
                        occured during parsing
    :raises FileNotFoundError: If no Schema file for the given version was found

    """

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    parser_version = '0.2.0'
    parser_info_out['parser_info'] = f'Masci-Tools Fleur inp.xml Parser v{parser_version}'

    if isinstance(inpxmlfile, etree._ElementTree):
        xmltree = inpxmlfile
    else:
        parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
        try:
            xmltree = etree.parse(inpxmlfile, parser)
        except etree.XMLSyntaxError as msg:
            raise ValueError(f'Failed to parse input file: {msg}') from msg

    if version is None:
        version = eval_xpath(xmltree, '//@fleurInputVersion', parser_info_out=parser_info_out)
        version = str(version)
        if version is None:
            raise ValueError('Failed to extract inputVersion')

    parser_info_out['fleur_inp_version'] = version
    schema_dict = InputSchemaDict.fromVersion(version, parser_info_out=parser_info_out)

    ignore_validation = schema_dict['inp_version'] != version

    xmltree = clear_xml(xmltree)
    root = xmltree.getroot()

    constants = read_constants(root, schema_dict)

    try:
        schema_dict.xmlschema.assertValid(xmltree)
    except etree.DocumentInvalid as err:

        error_log = sorted(schema_dict.xmlschema.error_log, key=lambda x: x.message)
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
        errmsg = f"Input file does not validate against the schema: \n{''.join(error_output)}"

        parser_info_out['parser_warnings'].append(errmsg)
        if not ignore_validation:
            raise ValueError(errmsg) from err

    if schema_dict.xmlschema.validate(xmltree) or ignore_validation:
        inp_dict = inpxml_todict(root, schema_dict, constants, parser_info_out=parser_info_out)
    else:
        parser_info_out['parser_warnings'].append('Input file does not validate against the schema: Reason is unknown')
        if not ignore_validation:
            raise ValueError('Input file does not validate against the schema: Reason is unknown')

    return inp_dict


def inpxml_todict(parent, schema_dict, constants, omitted_tags=False, base_xpath=None, parser_info_out=None):
    """
    Recursive operation which transforms an xml etree to
    python nested dictionaries and lists.
    Decision to add a list is if the tag name is in the given list tag_several

    :param parent: some xmltree, or xml element
    :param schema_dict: structure/layout of the xml file in python dictionary
    :param constants: dict with all the defined constants
    :param omitted_tags: switch. If True only a list of the contained tags is returned
                         Used to omitt useless tags like e.g ['atomSpecies']['species'][3]
                         becomes ['atomSpecies'][3]
    :param base_xpath: str, keeps track of the place in the inp.xml currently being processed
    :param parser_info_out: dict, with warnings, info, errors, ...

    :return: a python dictionary
    """

    if parser_info_out is None:
        parser_info_out = {'parser_warnings': []}

    #Check if this is the first call to this routine
    if base_xpath is None:
        base_xpath = f'/{parent.tag}'

    return_dict = {}
    if list(parent.items()):
        return_dict = dict(list(parent.items()))
        # Now we have to convert lazy fortan style into pretty things for the Database
        for key in return_dict:
            if key in schema_dict['attrib_types']:
                conversion_warnings = []
                return_dict[key], suc = convert_xml_attribute(return_dict[key],
                                                              schema_dict['attrib_types'][key],
                                                              constants,
                                                              conversion_warnings=conversion_warnings)
                if not suc:
                    parser_info_out['parser_warnings'].append(
                        f"Failed to convert attribute '{key}': "
                        'Below are the warnings raised from convert_xml_attribute')
                    for warning in conversion_warnings:
                        parser_info_out['parser_warnings'].append(warning)

    if parent.text:
        # has text, but we don't want all the '\n' s and empty stings in the database
        if parent.text.strip() != '':  # might not be the best solutions
            if parent.tag not in schema_dict['simple_elements']:
                raise ValueError(
                    f'Something is wrong in the schema_dict: {parent.tag} is not in simple_elements, but it has text')
            conversion_warnings = []
            converted_text, suc = convert_xml_text(parent.text,
                                                   schema_dict['simple_elements'][parent.tag],
                                                   constants,
                                                   conversion_warnings=conversion_warnings)
            if not suc:
                parser_info_out['parser_warnings'].append(f"Failed to convert text of '{parent.tag}': "
                                                          'Below are the warnings raised from convert_xml_text')
                for warning in conversion_warnings:
                    parser_info_out['parser_warnings'].append(warning)

            if not return_dict:
                return_dict = converted_text
            else:
                return_dict['text_value'] = converted_text
                if 'label' in return_dict:
                    return_dict['text_label'] = return_dict['label']
                    return_dict.pop('label')

    if base_xpath in schema_dict['tag_info']:
        tag_info = schema_dict['tag_info'][base_xpath]
    else:
        tag_info = {'several': []}

    for element in parent:

        new_base_xpath = f'{base_xpath}/{element.tag}'
        omitt_contained_tags = element.tag in schema_dict['omitt_contained_tags']
        new_return_dict = inpxml_todict(element,
                                        schema_dict,
                                        constants,
                                        base_xpath=new_base_xpath,
                                        omitted_tags=omitt_contained_tags,
                                        parser_info_out=parser_info_out)

        if element.tag in tag_info['several']:
            # make a list, otherwise the tag will be overwritten in the dict
            if element.tag not in return_dict:  # is this the first occurence?
                if omitted_tags:
                    if len(return_dict) == 0:
                        return_dict = []
                else:
                    return_dict[element.tag] = []
            if omitted_tags:
                return_dict.append(new_return_dict)
            elif 'text_value' in new_return_dict:
                for key, value in new_return_dict.items():
                    if key == 'text_value':
                        return_dict[element.tag].append(value)
                    elif key == 'text_label':
                        if 'labels' not in return_dict:
                            return_dict['labels'] = {}
                        return_dict['labels'][value] = new_return_dict['text_value']
                    else:
                        if key not in return_dict:
                            return_dict[key] = []
                        elif not isinstance(return_dict[key], list):  #Key seems to be defined already
                            raise ValueError(f'{key} cannot be extracted to the next level')
                        return_dict[key].append(value)
                for key in new_return_dict.keys():
                    if key in ['text_value', 'text_label']:
                        continue
                    if len(return_dict[key]) != len(return_dict[element.tag]):
                        raise ValueError(
                            f'Extracted optional argument {key} at the moment only label is supported correctly')
            else:
                return_dict[element.tag].append(new_return_dict)
        else:
            return_dict[element.tag] = new_return_dict

    return return_dict
