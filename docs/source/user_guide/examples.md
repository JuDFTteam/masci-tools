---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.4
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

<!-- Set up pretty XML representations -->
```{code-cell} ipython3
:tags: [remove-cell]

from lxml import etree
from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter

def display_xml(data):

    xmlstring = etree.tostring(data, encoding='unicode', pretty_print=True)
    return highlight(xmlstring, XmlLexer(), HtmlFormatter(noclasses=True))

html_formatter = get_ipython().display_formatter.formatters['text/html']
html_formatter.for_type(etree._Element, display_xml)
html_formatter.for_type(etree._ElementTree, display_xml)
```

# Examples
```{code-cell} ipython3
:tags: [hide-output]

from masci_tools.io.fleur_xml import load_inpxml

xmltree, schema_dict = load_inpxml('files/inp.xml')
xmltree
```
