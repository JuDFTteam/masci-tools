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

from lxml import etree
import warnings
import io
import os
from pathlib import Path
from functools import partial
from logging import Logger
from typing import Callable, Any
from masci_tools.io.parsers import fleur_schema
from masci_tools.util.typing import XMLFileLike


def load_inpxml(inpxmlfile: XMLFileLike,
                logger: Logger | None = None,
                base_url: str | None = None,
                **kwargs: Any) -> tuple[etree._ElementTree, fleur_schema.InputSchemaDict]:
    """
    Loads a inp.xml file for fleur together with its corresponding schema dictionary

    :param inpxmlfile: either path to the inp.xml file, opened file handle
                       or a xml etree to be parsed

    :returns: parsed xmltree of the inpxmlfile and the schema dictionary
              for the corresponding input version
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.io.parsers.fleur_schema import InputSchemaDict

    if isinstance(inpxmlfile, io.IOBase):
        xml_parse_func: Callable = etree.parse
    elif isinstance(inpxmlfile, (str, bytes, Path)):
        if os.path.isfile(inpxmlfile):
            xml_parse_func = etree.parse
        else:
            xml_parse_func = etree.fromstring
            if base_url is None:
                warnings.warn('You provided a string of content but no base_url argument.'
                              'Setting it to the current working directory.'
                              'If the tree contains xinclude tags these could fail')
                base_url = os.getcwd()
            elif isinstance(base_url, Path):
                base_url = os.fspath(base_url.resolve())
            xml_parse_func = partial(xml_parse_func, base_url=base_url)

    if isinstance(inpxmlfile, Path):
        inpxmlfile = os.fspath(inpxmlfile)

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
        xmltree = xmltree.getroottree()  #type:ignore

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
                base_url: str | None = None,
                **kwargs: Any) -> tuple[etree._ElementTree, fleur_schema.OutputSchemaDict]:
    """
    Loads a out.xml file for fleur together with its corresponding schema dictionary

    :param outxmlfile: either path to the out.xml file, opened file handle
                       or a xml etree to be parsed

    :returns: parsed xmltree of the outxmlfile and the schema dictionary
              for the corresponding output version
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.io.parsers.fleur_schema import OutputSchemaDict

    if isinstance(outxmlfile, io.IOBase):
        xml_parse_func: Callable = etree.parse
    elif isinstance(outxmlfile, (str, bytes, Path)):
        if os.path.isfile(outxmlfile):
            xml_parse_func = etree.parse
        else:
            xml_parse_func = etree.fromstring
            if base_url is None:
                warnings.warn('You provided a string of content but no base_url argument.'
                              'Setting it to the current working directory.'
                              'If the tree contains xinclude tags these could fail')
                base_url = os.getcwd()
            elif isinstance(base_url, Path):
                base_url = os.fspath(base_url.resolve())
            xml_parse_func = partial(xml_parse_func, base_url=base_url)

    if isinstance(outxmlfile, Path):
        outxmlfile = os.fspath(outxmlfile)

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
        xmltree = xmltree.getroottree()  #type:ignore

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
                'out.xml files before the MaX3.1 release are not explicitely supported.'
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
