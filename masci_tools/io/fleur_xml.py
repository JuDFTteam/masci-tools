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
This module provides easy functions for loading a input/output xml file of
fleur and providing a parsed xml etree together with its corresponding schema dict
"""
from __future__ import annotations
import logging

from lxml import etree
import warnings
import os
from pathlib import Path
from functools import partial
from logging import Logger
from typing import Callable, Any, Generator
from masci_tools.io.parsers import fleur_schema
from masci_tools.util.typing import XMLFileLike, XMLLike

__all__ = ('load_inpxml', 'load_outxml', 'FleurXMLContext', 'get_constants')


def load_inpxml(inpxmlfile: XMLFileLike,
                logger: Logger | None = None,
                base_url: str | Path | None = None,
                **kwargs: Any) -> tuple[etree._ElementTree, fleur_schema.InputSchemaDict]:
    """
    Loads a inp.xml file for fleur together with its corresponding schema dictionary

    :param inpxmlfile: either path to the inp.xml file, opened file handle (in bytes modes i.e. rb)
                       or a xml etree to be parsed

    :returns: parsed xmltree of the inpxmlfile and the schema dictionary
              for the corresponding input version
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.io.parsers.fleur_schema import InputSchemaDict

    xml_parse_func: Callable = etree.parse
    if isinstance(inpxmlfile, (str, bytes, Path)) and not os.path.isfile(inpxmlfile):
        xml_parse_func = etree.fromstring
        if base_url is None:
            warnings.warn('You provided a string of content but no base_url argument.'
                          'Setting it to the current working directory.'
                          'If the tree contains xinclude tags these could fail')
            base_url = os.getcwd()
        elif isinstance(base_url, Path):
            base_url = os.fspath(base_url)
        xml_parse_func = partial(xml_parse_func, base_url=base_url)

    if isinstance(inpxmlfile, etree._ElementTree):
        xmltree = inpxmlfile
    else:
        parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8', **kwargs)

        try:
            xmltree = xml_parse_func(inpxmlfile, parser)
        except etree.XMLSyntaxError as msg:
            if logger is not None:
                logger.exception('Failed to parse input file')
            raise ValueError(f'Failed to parse input file: {msg}') from msg

    if etree.iselement(xmltree):
        xmltree = xmltree.getroottree()

    if xmltree is None:
        if logger is not None:
            logger.error('No XML tree generated. Check that the given file exists')
        raise ValueError('No XML tree generated. Check that the given file exists')

    version = eval_xpath(xmltree, '//@fleurInputVersion')
    if not version:
        if logger is not None:
            logger.error('Failed to extract inputVersion')
        raise ValueError('Failed to extract inputVersion')
    version = str(version)

    if logger is not None:
        logger.info('Got Fleur input file with file version %s', version)

    schema_dict = InputSchemaDict.fromVersion(version, logger=logger)

    return xmltree, schema_dict


def load_outxml(outxmlfile: XMLFileLike,
                logger: Logger | None = None,
                base_url: str | Path | None = None,
                **kwargs: Any) -> tuple[etree._ElementTree, fleur_schema.OutputSchemaDict]:
    """
    Loads a out.xml file for fleur together with its corresponding schema dictionary

    :param outxmlfile: either path to the out.xml file, opened file handle (in bytes modes i.e. rb)
                       or a xml etree to be parsed

    :returns: parsed xmltree of the outxmlfile and the schema dictionary
              for the corresponding output version
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.io.parsers.fleur_schema import OutputSchemaDict

    xml_parse_func: Callable = etree.parse
    if isinstance(outxmlfile, (str, bytes, Path)) and not os.path.isfile(outxmlfile):
        xml_parse_func = etree.fromstring
        if base_url is None:
            warnings.warn('You provided a string of content but no base_url argument.'
                          'Setting it to the current working directory.'
                          'If the tree contains xinclude tags these could fail')
            base_url = os.getcwd()
        elif isinstance(base_url, Path):
            base_url = os.fspath(base_url)
        xml_parse_func = partial(xml_parse_func, base_url=base_url)

    outfile_broken = False

    if isinstance(outxmlfile, etree._ElementTree):
        xmltree = outxmlfile
    elif 'recover' in kwargs:
        parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8', **kwargs)

        try:
            xmltree = xml_parse_func(outxmlfile, parser)
        except etree.XMLSyntaxError as msg:
            if logger is not None:
                logger.error(f"Failed to parse output file with recover={kwargs['recover']}")
            raise ValueError(f"Failed to parse output file with recover={kwargs['recover']}: {msg}") from msg
    else:
        parser = etree.XMLParser(attribute_defaults=True, recover=False, encoding='utf-8', **kwargs)

        try:
            xmltree = xml_parse_func(outxmlfile, parser)
        except etree.XMLSyntaxError:
            outfile_broken = True
            if logger is None:
                warnings.warn('The out.xml file is broken I try to repair it.')
            else:
                logger.warning('The out.xml file is broken I try to repair it.')

        if outfile_broken:
            # repair xmlfile and try to parse what is possible.
            parser = etree.XMLParser(attribute_defaults=True, recover=True, encoding='utf-8', **kwargs)

            try:
                xmltree = xml_parse_func(outxmlfile, parser)
            except etree.XMLSyntaxError as err:
                raise ValueError('Skipping the parsing of the xml file. Repairing was not possible.') from err

    if etree.iselement(xmltree):
        xmltree = xmltree.getroottree()

    if xmltree is None:
        if logger is not None:
            logger.error('No XML tree generated. Check that the given file exists')
        raise ValueError('No XML tree generated. Check that the given file exists')

    out_version = eval_xpath(xmltree, '//@fleurOutputVersion')
    if not out_version:
        if logger is not None:
            logger.error('Failed to extract outputVersion')
        raise ValueError('Failed to extract outputVersion')
    out_version = str(out_version)

    if out_version == '0.27':
        program_version = str(eval_xpath(xmltree, '//programVersion/@version'))
        if program_version == 'fleur 32':
            #Max5 release (before bugfix)
            out_version = '0.33'
            inp_version = '0.33'
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX5.0 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX5.0 release")
        elif program_version == 'fleur 31':
            #Max4 release
            out_version = '0.31'
            inp_version = '0.31'
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX4.0 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX4.0 release")
        elif program_version == 'fleur 30':
            #Max3.1 release
            out_version = '0.30'
            inp_version = '0.30'
            if logger is not None:
                logger.warning("Ignoring '0.27' outputVersion for MaX3.1 release")
            else:
                warnings.warn("Ignoring '0.27' outputVersion for MaX3.1 release")
        elif program_version == 'fleur 27':
            #Max3.1 release
            out_version = '0.29'
            inp_version = '0.29'
            if logger is not None:
                logger.warning("Found version before MaX3.1 release falling back to file version '0.29'")
            warnings.warn(
                'out.xml files before the MaX3.1 release are not explicitly supported.'
                ' No guarantee is given that the parser will work without error', UserWarning)
        else:
            if logger is not None:
                logger.error("Unknown fleur version: File-version '%s' Program-version '%s'", out_version,
                             program_version)
            raise ValueError(f"Unknown fleur version: File-version '{out_version}' Program-version '{program_version}'")
    else:
        inp_version: str = eval_xpath(xmltree, '//@fleurInputVersion')  #type:ignore
        if not inp_version:
            raise ValueError('Failed to extract inputVersion')
        inp_version = str(inp_version)

    schema_dict = OutputSchemaDict.fromVersion(out_version, inp_version=inp_version, logger=logger)

    return xmltree, schema_dict


from contextlib import contextmanager
from masci_tools.util.xml.common_functions import normalize_xmllike


class _EvalContext:

    def __init__(self,
                 etree_or_element: XMLLike,
                 schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                 constants: dict[str, float] | None = None,
                 logger: logging.Logger | None = None) -> None:
        self.node = normalize_xmllike(etree_or_element)
        self.schema_dict = schema_dict
        self.logger = logger
        self.constants = constants or get_constants(self.node, self.schema_dict, self.logger)

    def attribute(self, name, default=None, **kwargs):
        from masci_tools.util.schema_dict_util import evaluate_attribute
        if default is not None:
            kwargs['optional'] = True
        res = evaluate_attribute(self.node,
                                 self.schema_dict,
                                 name,
                                 logger=self.logger,
                                 constants=self.constants,
                                 **kwargs)
        if res is None and default is not None:
            return default
        return res

    def text(self, name, **kwargs):
        from masci_tools.util.schema_dict_util import evaluate_text
        return evaluate_text(self.node, self.schema_dict, name, logger=self.logger, constants=self.constants, **kwargs)

    def all_attributes(self, name, **kwargs):
        from masci_tools.util.schema_dict_util import evaluate_tag
        return evaluate_tag(self.node, self.schema_dict, name, logger=self.logger, constants=self.constants, **kwargs)

    def parent_attributes(self, name, **kwargs):
        from masci_tools.util.schema_dict_util import evaluate_parent_tag
        return evaluate_parent_tag(self.node,
                                   self.schema_dict,
                                   name,
                                   logger=self.logger,
                                   constants=self.constants,
                                   **kwargs)

    def single_value(self, name, **kwargs):
        from masci_tools.util.schema_dict_util import evaluate_single_value_tag
        return evaluate_single_value_tag(self.node,
                                         self.schema_dict,
                                         name,
                                         logger=self.logger,
                                         constants=self.constants,
                                         **kwargs)

    def tag_exists(self, name, **kwargs):
        from masci_tools.util.schema_dict_util import tag_exists
        return tag_exists(self.node, self.schema_dict, name, logger=self.logger, **kwargs)

    def number_nodes(self, name, **kwargs):
        from masci_tools.util.schema_dict_util import get_number_of_nodes
        return get_number_of_nodes(self.node, self.schema_dict, name, logger=self.logger, **kwargs)

    def attribute_exists(self, name, **kwargs):
        from masci_tools.util.schema_dict_util import attrib_exists
        return attrib_exists(self.node, self.schema_dict, name, logger=self.logger, **kwargs)

    def simple_xpath(self, name, **kwargs):
        from masci_tools.util.schema_dict_util import eval_simple_xpath
        return eval_simple_xpath(self.node, self.schema_dict, name, logger=self.logger, **kwargs)

    def child(self, name, **kwargs):

        if 'list_return' in kwargs:
            raise ValueError('The argument list_return is not allowed in child()')

        nodes = self.simple_xpath(name, **kwargs, list_return=True)
        if len(nodes) != 1:
            raise ValueError(f'Expected one node for {name}. Got {len(nodes)}')
        return self.nested(nodes[0])

    @contextmanager
    def nested(self, etree_or_element):
        yield _EvalContext(etree_or_element, self.schema_dict, self.constants, logger=self.logger)

    def optional_child(self, name, **kwargs):

        if 'list_return' in kwargs:
            raise ValueError('The argument list_return is not allowed in child()')

        nodes = self.simple_xpath(name, **kwargs, list_return=True)
        if len(nodes) == 0:
            return False

        if len(nodes) != 1:
            raise ValueError(f'Expected one node for {name}. Got {len(nodes)}')
        return _EvalContext(nodes[0], self.schema_dict, self.constants)

    def children(self, name, **kwargs):
        nodes = self.simple_xpath(name, **kwargs, list_return=True)
        for node in nodes:
            yield _EvalContext(node, self.schema_dict, self.constants)


@contextmanager
def FleurXMLContext(etree_or_element: XMLLike,
                    schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                    constants: dict[str, float] | None = None,
                    logger: logging.Logger | None = None) -> Generator[_EvalContext, None, None]:

    yield _EvalContext(etree_or_element, schema_dict, constants=constants, logger=logger)

def get_constants(xmltree: XMLLike | etree.XPathElementEvaluator,
                  schema_dict: fleur_schema.InputSchemaDict | fleur_schema.OutputSchemaDict,
                  logger: Logger | None = None) -> dict[str, float]:
    """
    Reads in the constants defined in the inp.xml
    and returns them combined with the predefined constants from
    fleur as a dictionary

    :param root: root of the etree of the inp.xml file
    :param schema_dict: schema_dictionary of the version of the file to read (inp.xml or out.xml)
    :param logger: logger object for logging warnings, errors

    :return: a python dictionary with all defined constants
    """
    from masci_tools.util.constants import FLEUR_DEFINED_CONSTANTS
    from masci_tools.io.parsers.fleur_schema import NoPathFound
    import copy

    defined_constants = copy.deepcopy(FLEUR_DEFINED_CONSTANTS)
    with FleurXMLContext(xmltree, schema_dict, logger=logger, constants=defined_constants) as root:

        try:
            root.tag_exists('constant')
        except NoPathFound:
            warnings.warn('Cannot extract custom constants for the given root. Assuming defaults')
            return defined_constants

        if not root.tag_exists('constant'):  #Avoid warnings for empty constants
            return defined_constants

        constants = root.all_attributes('constant')
        if constants['name'] is not None:
            if not isinstance(constants['name'], list):
                constants = {key: [val] for key, val in constants.items()}
            for name, value in zip(constants['name'], constants['value']):
                if name not in defined_constants:
                    defined_constants[name] = value
                else:
                    if logger is not None:
                        logger.error('Ambiguous definition of constant %s', name)
                    raise KeyError(f'Ambiguous definition of constant {name}')

    return defined_constants