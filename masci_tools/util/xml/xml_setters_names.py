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
Functions for modifying the xml input file of Fleur utilizing the schema dict
"""
from masci_tools.util.schema_dict_util import get_tag_xpath


def create_tag(xmltree, schema_dict, tag_name, complex_xpath=None, create_parents=False, **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import create_tag_schema_dict

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    parent_xpath, tag_name = '/'.join(base_xpath.split('/')[:-1]), base_xpath.split('/')[-1]

    if complex_xpath is None:
        complex_xpath = parent_xpath

    xmltree = create_tag_schema_dict(xmltree,
                                     schema_dict,
                                     complex_xpath,
                                     tag_name,
                                     parent_xpath,
                                     create_parents=create_parents)

    return xmltree


def get_tag_or_create(xmltree, schema_dict, tag_name, create_parents=False, complex_xpath=None, **kwargs):

    from masci_tools.util.xml.xml_setters_xpaths import eval_xpath_create

    base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

    parent_xpath, tag_name = '/'.join(base_xpath.split('/')[:-1]), base_xpath.split('/')[-1]
    if complex_xpath is None:
        complex_xpath = parent_xpath

    xmltree = eval_xpath_create(xmltree, schema_dict, complex_xpath, base_xpath, create_parents=create_parents)

    return xmltree
