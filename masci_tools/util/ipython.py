"""
Import this module to activate useful ipython extensions
"""
from __future__ import annotations

from lxml import etree
from pygments import highlight
from pygments.lexers import XmlLexer  #pylint: disable=no-name-in-module
from pygments.formatters import HtmlFormatter  #pylint: disable=no-name-in-module

from masci_tools.util.typing import XMLLike


def display_xml(data: XMLLike) -> str:
    """
    Display the given lxml XML tree as formatted HTML

    :param data: data to show

    :returns: HTML string for presentation in Jupyter notebooks
    """

    xmlstring = etree.tostring(data, encoding='unicode', pretty_print=True)
    return highlight(xmlstring, XmlLexer(), HtmlFormatter(noclasses=True))


def register_formatters(ipython):

    html_formatter = ipython.display_formatter.formatters['text/html']
    html_formatter.for_type(etree._Element, display_xml)
    html_formatter.for_type(etree._ElementTree, display_xml)
