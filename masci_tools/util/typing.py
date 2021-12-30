# -*- coding: utf-8 -*-
"""
This module defines some aliases used in typing
"""
from typing import TypeVar, Union
try:
    from typing import TypeAlias #type: ignore[attr-defined]
except ImportError:
    from typing_extensions import TypeAlias
from lxml import etree

#Type for xml setters/getters for xpath objects that can be used in `eval_xpath`
from masci_tools.util.xml.xpathbuilder import XPathBuilder

XPathLike: TypeAlias = Union[str, bytes, etree.XPath, XPathBuilder]
TXPathLike = TypeVar('TXPathLike', str, etree.XPath, XPathBuilder)
"""
Type for xpath expressions
"""
