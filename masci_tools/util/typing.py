"""
This module defines some aliases used in typing
"""
from __future__ import annotations

from typing import TypeVar, Any, IO, Union
import sys
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias
from lxml import etree
from pathlib import Path
import os

#Type for xml setters/getters for xpath objects that can be used in `eval_xpath`
from masci_tools.util.xml.xpathbuilder import XPathBuilder

XPathLike: TypeAlias = Union[str, bytes, etree.XPath, XPathBuilder]
"""
Type for xpath expressions
"""

TXPathLike = TypeVar('TXPathLike', bound=XPathLike)
"""
Type for xpath expressions
"""

FileLike: TypeAlias = Union[str, bytes, Path, os.PathLike, IO[Any]]
"""
Type used for functions accepting file-like objects, i.e. handles or file paths
"""

XMLFileLike: TypeAlias = Union[etree._ElementTree, etree._Element, FileLike]
"""
Type used for functions accepting xml-file-like objects, i.e. handles or file paths
or already parsed xml objects
"""

XMLLike: TypeAlias = Union[etree._Element, etree._ElementTree]
"""
Type used for functions accepting xml objects from lxml
"""
