"""
This module defines some aliases used in typing
"""
from __future__ import annotations

from typing import TypeVar, Any, IO
try:
    from typing import TypeAlias  #type: ignore[attr-defined]
except ImportError:
    from typing_extensions import TypeAlias
from lxml import etree
from pathlib import Path
import os

#Type for xml setters/getters for xpath objects that can be used in `eval_xpath`
from masci_tools.util.xml.xpathbuilder import XPathBuilder

XPathLike: TypeAlias = 'str | bytes | etree.XPath | XPathBuilder'
"""
Type for xpath expressions
"""

TXPathLike = TypeVar('TXPathLike', str, etree.XPath, XPathBuilder)
"""
Type for xpath expressions
"""

FileLike: TypeAlias = 'str | bytes | Path | os.PathLike[Any] | IO'
"""
Type used for functions accepting file-like objects, i.e. handles or file paths
"""

XMLFileLike: TypeAlias = 'etree._ElementTree | etree._Element | FileLike'
"""
Type used for functions accepting xml-file-like objects, i.e. handles or file paths
or already parsed xml objects
"""

XMLLike: TypeAlias = 'etree._Element | etree._ElementTree'
"""
Type used for functions accepting xml objects from lxml
"""
