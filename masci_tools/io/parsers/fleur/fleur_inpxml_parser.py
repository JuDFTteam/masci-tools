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
This module contains functions to load an fleur inp.xml file, parse it with a schema
and convert its content to a dict
"""
from __future__ import annotations

from lxml import etree

from masci_tools.io.fleur_xml import get_constants, load_inpxml
from masci_tools.util.xml.common_functions import clear_xml
from masci_tools.util.xml.converters import convert_from_xml
from masci_tools.util.schema_dict_util import evaluate_attribute
from masci_tools.util.logging_util import DictHandler
from masci_tools.util.typing import XMLFileLike
import logging
from typing import Any
from masci_tools.io.parsers.fleur_schema import InputSchemaDict, EMPTY_TAG_INFO


def inpxml_parser(inpxmlfile: XMLFileLike,
                  parser_info_out: dict[str, Any] | None = None,
                  strict: bool = False,
                  debug: bool = False,
                  base_url: str | None = None) -> dict[str, Any]:
    """
    Parses the given inp.xml file to a python dictionary utilizing the schema
    defined by the version number to validate and correctly convert to the dictionary

    :param inpxmlfile: either path to the inp.xml file, opened file handle (in bytes modes i.e. rb)
                       or a xml etree to be parsed
    :param parser_info_out: dict, with warnings, info, errors, ...
    :param strict: bool if True  and no parser_info_out is provided any encountered error will immediately be raised

    :return: python dictionary with the parsed inp.xml

    :raises ValueError: If the validation against the schema failed, or an irrecoverable error
                        occurred during parsing
    :raises FileNotFoundError: If no Schema file for the given version was found

    """

    __parser_version__ = '0.3.0'
    logger: logging.Logger | None = logging.getLogger(__name__)

    if strict:
        logger = None

    parser_log_handler = None
    if logger is not None:
        if parser_info_out is None:
            parser_info_out = {}

        logging_level = logging.INFO
        if debug:
            logging_level = logging.DEBUG
        logger.setLevel(logging_level)

        parser_log_handler = DictHandler(parser_info_out,
                                         WARNING='parser_warnings',
                                         ERROR='parser_errors',
                                         INFO='parser_info',
                                         DEBUG='parser_debug',
                                         CRITICAL='parser_critical',
                                         ignore_unknown_levels=True,
                                         level=logging_level)

        logger.addHandler(parser_log_handler)

    if logger is not None:
        logger.info('Masci-Tools Fleur inp.xml Parser v%s', __parser_version__)

    xmltree, schema_dict = load_inpxml(inpxmlfile, logger=logger, base_url=base_url)
    actual_inp_version = evaluate_attribute(xmltree, schema_dict, 'fleurInputVersion', logger=logger)
    ignore_validation = schema_dict['inp_version'] != actual_inp_version

    xmltree, _ = clear_xml(xmltree)
    root = xmltree.getroot()

    constants = get_constants(root, schema_dict, logger=logger)

    try:
        schema_dict.validate(xmltree, logger=logger)
    except ValueError as err:
        if not ignore_validation:
            if logger is not None:
                logger.exception(err)
            raise

    inp_dict = inpxml_todict(root, schema_dict, constants, logger=logger)

    if parser_log_handler is not None:
        if logger is not None:
            logger.removeHandler(parser_log_handler)

    return inp_dict


def inpxml_todict(parent: etree._Element,
                  schema_dict: InputSchemaDict,
                  constants: dict[str, float],
                  omitted_tags: bool = False,
                  base_xpath: str | None = None,
                  logger: logging.Logger | None = None) -> dict[str, Any]:
    """
    Recursive operation which transforms an xml etree to
    python nested dictionaries and lists.
    Decision to add a list is if the tag name is in the given list tag_several

    :param parent: some xmltree, or xml element
    :param schema_dict: structure/layout of the xml file in python dictionary
    :param constants: dict with all the defined constants
    :param omitted_tags: switch. If True only a list of the contained tags is returned
                         Used to omit useless tags like e.g ['atomSpecies']['species'][3]
                         becomes ['atomSpecies'][3]
    :param base_xpath: str, keeps track of the place in the inp.xml currently being processed
    :param parser_info_out: dict, with warnings, info, errors, ...

    :return: a python dictionary
    """
    #These keys have to never appear as an attribute/tag name
    #The underscores should guarantee that
    _TEXT_PLACEHOLDER = '__text__'
    _OMIT_PLACEHOLDER = '__omit__'

    #Check if this is the first call to this routine
    if base_xpath is None:
        base_xpath = f'/{parent.tag}'

    content: dict[str, Any] = {}
    # Now we have to convert lazy fortran style into pretty things for the Database
    for key, value in parent.items():
        attrib_name, value = str(key), str(value)
        if attrib_name in schema_dict['attrib_types']:
            content[attrib_name], suc = convert_from_xml(value,
                                                         schema_dict,
                                                         attrib_name,
                                                         text=False,
                                                         constants=constants,
                                                         logger=logger)
            if not suc and logger is not None:
                logger.warning("Failed to convert attribute '%s' Got: '%s'", attrib_name, value)

    # has text, but we don't want all the '\n' s and empty strings in the database
    if parent.text and parent.text.strip() != '':

        if parent.tag not in schema_dict['text_tags']:
            if logger is not None:
                logger.error('Something is wrong in the schema_dict: %s is not in text_tags, but it has text',
                             parent.tag)
            raise ValueError(
                f'Something is wrong in the schema_dict: {parent.tag} is not in text_tags, but it has text')

        converted_text, suc = convert_from_xml(str(parent.text),
                                               schema_dict,
                                               parent.tag,
                                               text=True,
                                               constants=constants,
                                               logger=logger)

        if not suc and logger is not None:
            logger.warning("Failed to text of '%s' Got: '%s'", parent.tag, parent.text)

        content[_TEXT_PLACEHOLDER] = converted_text

    tag_info = schema_dict['tag_info'].get(base_xpath, EMPTY_TAG_INFO)
    for element in parent:

        child_content = inpxml_todict(element,
                                      schema_dict,
                                      constants,
                                      base_xpath=f'{base_xpath}/{element.tag}',
                                      omitted_tags=element.tag in schema_dict['omitt_contained_tags'],
                                      logger=logger)

        if _OMIT_PLACEHOLDER in child_content:
            #We knoe that there is only one key here
            child_content = child_content.pop(_OMIT_PLACEHOLDER)

        tag_name = element.tag
        if omitted_tags:
            tag_name = _OMIT_PLACEHOLDER

        if element.tag in tag_info['several']\
           and _TEXT_PLACEHOLDER in child_content:
            #The text is stored under the name of the tag
            text_value = child_content.pop(_TEXT_PLACEHOLDER)
            content.setdefault(tag_name, []).append(text_value)
            child_tag_info = schema_dict['tag_info'].get(f'{base_xpath}/{element.tag}', EMPTY_TAG_INFO)
            for key, value in child_content.items():
                if key not in child_tag_info['optional_attribs']:
                    #All required attributes are stored as lists
                    if key in content and \
                       not isinstance(content[key], list):  #Key seems to be defined already
                        if logger is not None:
                            logger.error('%s cannot be extracted to the next level', key)
                        raise ValueError(f'{key} cannot be extracted to the next level')
                    content.setdefault(key, []).append(value)
                else:
                    #All optional attributes are stored as dicts pointing to the text
                    content.setdefault(key, {})[value] = text_value
        elif element.tag in tag_info['several']:
            content.setdefault(tag_name, []).append(child_content)
        elif _TEXT_PLACEHOLDER in child_content:
            content[tag_name] = child_content.pop(_TEXT_PLACEHOLDER)
        else:
            content[tag_name] = child_content

    return content
