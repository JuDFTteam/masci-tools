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

class XML:
    
    def __init__(self, data):
        self.data = etree.tostring(data, encoding='unicode', pretty_print=True)
        
    def _repr_html_(self):
        return highlight(self.data, XmlLexer(), HtmlFormatter(noclasses=True))


html_formatter = get_ipython().display_formatter.formatters['text/html']
html_formatter.for_type(etree._Element, XML)
html_formatter.for_type(etree._ElementTree, XML)
```

```{code-cell} ipython3
:tags: [hide-output]

from masci_tools.io.fleur_xml import load_inpxml

xmltree, schema_dict = load_inpxml('files/inp.xml')
xmltree
```
