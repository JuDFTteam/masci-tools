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

# Plotting KKR DOS/bandstructures


This section discusses how the standard output files for density of states and bandstructure calculations of a KKR calculation can be visualized.

```{contents}
```

## Density of states

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      DOS of bulk fcc Cu.
    name: kkr-dos1
---
#Example: KKR DOS

from masci_tools.vis.kkr_plot_dos import dosplot

# the path can be a relative or absolute path to the directory
# where the dos.atom files reside (i.e. the dir where the DOS calculation ran)
dosplot('files/kkr_dos/', color='k', lw=4, marker='v', ls=':', ms=8)
```

Where the `color`, `lw`, etc inputs are optional settings which customize the plot:


We can also use this to show the l-decomposed DOS (red line are d-orbitals):

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      DOS of bulk fcc Cu, l-resolved.
    name: kkr-dos2
---
#Example: KKR DOS, l-resolved

dosplot('files/kkr_dos/', totonly=False)
```


## Bandstructure


```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Bandstructure of bulk fcc Cu.
    name: kkr-bs1
---
#Example: KKR bandstructure

from masci_tools.vis.kkr_plot_bandstruc_qdos import dispersionplot

# the path can be a relative or absolute path to the directory
# where the qdos files reside (i.e. the dir where the qdos calculation ran)
dispersionplot('files/kkr_bandstruc/', ptitle='bulk Cu')
```

Which can also be customized with keyword arguments to the `dispersionplot` function:


```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Bandstructure of bulk fcc Cu.
    name: kkr-bs2
---
#Example: KKR bandstructure with custom color map

dispersionplot('files/kkr_bandstruc/', ptitle='bulk Cu', cmap='binary', clims=[-2,2], clrbar=False)
```


### Fermi surface

Constant energy contours can be calculated by using a single energy point in a qdos calculation with a 2D k-point grid defined in the `qvec.dat` input file to KKRhost.
For example, this can then be used to visualize a cut through the Fermi surface of a material. 

```python
#Example: KKR bandstructure

from masci_tools.vis.kkr_plot_FS_qdos import FSqdos2D

# the path can be a relative or absolute path to the directory
# where the qdos files reside (i.e. the dir where the qdos calculation ran)
FSqdos2D('PATH/TO/OUTPUT-FILES/')
```
