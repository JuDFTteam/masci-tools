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
from masci_tools.util.xml.xml_setters_xpaths import create_tag_xpath
from functools import partial

def create_tag(xmltree, schema_dict, tag_name, create=False, place_index=None, xpath=None, **kwargs):

   base_xpath = get_tag_xpath(schema_dict, tag_name, **kwargs)

   parent_xpath, tag_name = '/'.join(base_xpath.split('/')[:-1]), base_xpath.split('/')[-1]
   parent_tag_info = schema_dict['tag_info'][parent_xpath]

   tag_order = parent_tag_info['order']
   if len(tag_order) == 0 or place_index is not None:
      tag_order = None

   if xpath is None:
      xpath = parent_xpath

   xmltree = create_tag_xpath(xmltree, xpath, tag_name, tag_order=tag_order, create=create,
                              schema_dict_func=partial(create_tag, schema_dict=schema_dict))

   return xmltree

