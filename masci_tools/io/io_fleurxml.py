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
This module provides easy functions for loading a input/output xml file of
fleur and providing a parsed xml etree together with its corresponding schema dict
"""
from lxml import etree
import warnings


def load_inpxml(inpxmlfile):
    """
    Loads a inp.xml file for fleur together with its corresponding schema dictionary

    :param inpxmlfile: either path to the inp.xml file, opened file handle
                       or a xml etree to be parsed

    :returns: parsed xmltree of the inpxmlfile and the schema dictionary
              for the corresponding input version
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.io.parsers.fleur.fleur_schema import InputSchemaDict

    if isinstance(inpxmlfile, etree._ElementTree):
        xmltree = inpxmlfile
    else:
        parser = etree.XMLParser(attribute_defaults=True, encoding='utf-8')
        try:
            xmltree = etree.parse(inpxmlfile, parser)
        except etree.XMLSyntaxError as msg:
            raise ValueError(f'Failed to parse input file: {msg}') from msg

    version = eval_xpath(xmltree, '//@fleurInputVersion')
    version = str(version)
    if version is None:
        raise ValueError('Failed to extract inputVersion')

    schema_dict = InputSchemaDict.fromVersion(version)

    return xmltree, schema_dict


def load_outxml(outxmlfile):
    """
    Loads a out.xml file for fleur together with its corresponding schema dictionary

    :param outxmlfile: either path to the out.xml file, opened file handle
                       or a xml etree to be parsed

    :returns: parsed xmltree of the outxmlfile and the schema dictionary
              for the corresponding output version
    """
    from masci_tools.util.xml.common_functions import eval_xpath
    from masci_tools.io.parsers.fleur.fleur_schema import OutputSchemaDict

    outfile_broken = False

    if isinstance(outxmlfile, etree._ElementTree):
        xmltree = outxmlfile
    else:
        parser = etree.XMLParser(attribute_defaults=True, recover=False, encoding='utf-8')

        try:
            xmltree = etree.parse(outxmlfile, parser)
        except etree.XMLSyntaxError:
            outfile_broken = True
            warnings.warn('The out.xml file is broken I try to repair it.')

        if outfile_broken:
            # repair xmlfile and try to parse what is possible.
            parser = etree.XMLParser(attribute_defaults=True, recover=True, encoding='utf-8')
            try:
                xmltree = etree.parse(outxmlfile, parser)
            except etree.XMLSyntaxError as err:
                raise ValueError('Skipping the parsing of the xml file. Repairing was not possible.') from err

    out_version = eval_xpath(xmltree, '//@fleurOutputVersion')
    out_version = str(out_version)
    if out_version is None:
        raise ValueError('Failed to extract outputVersion')

    if out_version == '0.27':
        program_version = eval_xpath(xmltree, '//programVersion/@version')
        if program_version == 'fleur 32':
            #Max5 release (before bugfix)
            out_version = '0.33'
            inp_version = '0.33'
            warnings.warn("Ignoring '0.27' outputVersion for MaX5.0 release")
        elif program_version == 'fleur 31':
            #Max4 release
            out_version = '0.31'
            inp_version = '0.31'
            warnings.warn("Ignoring '0.27' outputVersion for MaX4.0 release")
        elif program_version == 'fleur 30':
            #Max3.1 release
            out_version = '0.30'
            inp_version = '0.30'
            warnings.warn("Ignoring '0.27' outputVersion for MaX3.1 release")
        elif program_version == 'fleur 27':
            #Max3.1 release
            out_version = '0.29'
            inp_version = '0.29'
            warnings.warn("Found version before MaX3.1 release falling back to file version '0.29'")
        else:
            raise ValueError(f"Unknown fleur version: File-version '{out_version}' Program-version '{program_version}'")
    else:
        inp_version = eval_xpath(xmltree, '//@fleurInputVersion')
        inp_version = str(inp_version)
        if inp_version is None:
            raise ValueError('Failed to extract inputVersion')

    schema_dict = OutputSchemaDict.fromVersion(out_version, inp_version=inp_version)

    return xmltree, schema_dict
