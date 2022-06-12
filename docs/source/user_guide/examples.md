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

%load_ext masci_tools
```

# Examples
```{code-cell} ipython3
:tags: [hide-output]

from masci_tools.io.fleur_xml import load_inpxml

xmltree, schema_dict = load_inpxml('files/inp.xml')
xmltree
```

```{code-cell} ipython3
from masci_tools.io.fleurxmlmodifier import FleurXMLModifier

fm = FleurXMLModifier()
fm.set_inpchanges({
    'itmax': 50,
    'band': True
})
new_xmltree = fm.modify_xmlfile(xmltree)
```

```{code-cell} ipython3
:tags: [remove-cell]
from masci_tools.util.ipython import xml_diff
xml_diff(xmltree, new_xmltree)
```

```{code-cell} ipython3
:tags: [hide-output]
from masci_tools.util.ipython import xml_diff
xml_diff(xmltree, new_xmltree)
```

