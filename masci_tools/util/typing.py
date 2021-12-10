# -*- coding: utf-8 -*-
"""
This module defines some aliases used in typing
"""
from typing import Union
from lxml import etree

#Type for xml setters/getters for xpath objects that can be used in `eval_xpath`
from masci_tools.util.xml.xpathbuilder import XPathBuilder

XPathLike = Union['etree._xpath', XPathBuilder]
