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

<!-- Increase dpi when calling plt.show -->
```{code-cell} ipython3
:tags: [remove-cell]
from masci_tools.vis.plot_methods import set_mpl_plot_defaults
set_mpl_plot_defaults(figure_kwargs={'dpi':450})
```

# Plotting Fleur DOS/bandstructures

```{eval-rst}
.. currentmodule:: masci_tools.io.parsers.hdf5
```

This section discusses how to obtain plots of data in the `banddos.hdf` for
density of states and bandstructure calculations.

In the following bandstructure and DOS plots are explained. Each section leads with the
names of the recipes from the {py:mod}`~masci_tools.io.parsers.hdf5.recipes` module that
can be used with the explained visualization function.

All Fleur specific plotting routines are found in {py:mod}`~masci_tools.vis.fleur` have
implementations for both the matplotlib and bokeh plotting libraries and can be customized
heavily. For an explanation on customizing plots refer to {ref}`plotting`.

```{contents}
```

## Reading `banddos.hdf` files

The process here is divided in two parts. First we extract and transform the data in a
way to make it easy to plot via the {py:class}`reader.HDF5Reader`. For a detailed
explanation of the capabilities of this tool refer to {ref}`hdf5-parser`.
Here we show the basic usage:

```{code-cell} ipython3
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands

with HDF5Reader('files/banddos_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

print(f"The following datasets were read: {list(data.keys())}")
print(f"The following attributes were read: {list(attributes.keys())}")
```
## Bandstructures

Compatible Recipes for the {py:class}`reader.HDF5Reader`:

- `FleurBands`: Default recipe reading in the kpoints, eignevalues and weights for atom and orbital contributions
- `FleurSimpleBands`: Reads in only the kpoints and eigenvalues and now weights
- `FleurOrbcompBands`: In addition to the eigenvalues the weights from an orbital decomposition calculation are read in
- `FleurjDOSBands`: In addition to the eigenvalues the weights from a jDOS calculation are read in
- `FleurMCDBands`: In addition to the eigenvalues the weights from a MCD calculation are read in
- {py:func}`recipes.get_fleur_bands_specific_weights()`: Function to generate a recipe for reading in the eigenvalues+a provided list of weights

```{eval-rst}
.. currentmodule:: masci_tools.vis.fleur
```

The bandstructure visualization {py:func}`plot_fleur_bands()` can be used to plot

1. Non-spinpolarized/spinpolarized bandstructures
2. Bandstructures with emphasized weights on all eigenvalues (Also non-spinpolarized and spinpolarized)

### Standard bandstructure

To plot a simple bandstructure without any weighting we just have to pass the data, that
the {py:class}`~masci_tools.io.parsers.hdf5.reader.HDF5Reader` provided to the
{py:func}`plot_fleur_bands()`.

The two examples below show the resulting plots for a non-psinpolarized system (bulk Si)
and a spin-polarized system (Fe fcc). For both systems the necessary code is exactly the
same and is shown above the plots. The shown plots are the ones for the matplotlib plotting
backend:

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Non spinpolarized bandstructure for a bulk Si structure

    name: fleur-bandplot-simple
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands
from masci_tools.vis.fleur import plot_fleur_bands

#Read in data
with HDF5Reader('files/banddos_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_bands(data,
                      attributes,
                      limits={'y': (-13, 5)},
                      markersize=10)
```

```{code-cell} ipython3
---
mystnb:
  remove_code_source: true
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Spinpolarized bandstructure for a bulk Fe fcc structure

    name: fleur-bandplot-simple-spinplot
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands
from masci_tools.vis.fleur import plot_fleur_bands

#Read in data
with HDF5Reader('files/banddos_spinpol_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_bands(data,
                      attributes,
                      limits={'y': (-9, 5)},
                      markersize=10)
```

### Bandstructure with weights

To plot a simple bandstructure with weighting we do the same procedure as above, but we
pass in the entry we want to use for weights. These correspond to the entries in the
`banddos.hdf` file (for example the weight for the s-orbital on the first atom type is
called `MT:1s`). The weights will be used to change the size and color (according to a colormap) to
indicate regions of high weight.

The two examples below show the resulting plots for a non-psinpolarized system (bulk Si)
weighted for the s-orbital on the first atom and a spin-polarized system (Fe fcc) with
weights for the d-orbital on the first atom type. For both systems the necessary code
is exactly the same and is shown above the plots. The shown plots are the ones for the
matplotlib plotting backend:

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Non spinpolarized bandstructure for a bulk Si structure.
      The s-like character inside the Muffin-tin sphere is highlighted

    name: fleur-bandplot-simple-weighted
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands
from masci_tools.vis.fleur import plot_fleur_bands

#Read in data
with HDF5Reader('files/banddos_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_bands(data,
                      attributes,
                      weight='MT:1s',
                      limits={'y': (-13,5)})
```

```{code-cell} ipython3
---
mystnb:
  remove_code_source: true
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Spinpolarized bandstructure for a bulk Fe fcc structure.
      The d-like character inside the Muffin-tin sphere is highlighted
    name: fleur-bandplot-simple-spinpol-weighted
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands
from masci_tools.vis.fleur import plot_fleur_bands

#Read in data
with HDF5Reader('files/banddos_spinpol_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_bands(data,
                      attributes,
                      weight='MT:1d',
                      limits={'y': (-9,4)})
```

### Plotting options for bandstructure plots

The {py:func}`plot_fleur_bands()` function has a couple of options to modify, what is being
displayed from the `banddos.hdf` file. Below we show a few examples of ways to use these
options, together with examples of resulting plots.

#### Plotting bandstructure without spinpolarization

Providing `spinpol=False` will display the bandstructure as non spinpolarized, even
if there are two spins in the data. Works for both non-weighted and weighted 
bandstructures.

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Non spinpolarized bandstructure for a bulk Fe fcc structure.
    name: fleur-bandplot-spinpol-false
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands
from masci_tools.vis.fleur import plot_fleur_bands

#Read in data
with HDF5Reader('files/banddos_spinpol_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_bands(data,
                      attributes,
                      limits={'y': (-9,4)},
                      markersize=10,
                      spinpol=False)
```

```{code-cell} ipython3
---
mystnb:
  remove_code_source: true
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Non spinpolarized bandstructure for a bulk Fe fcc structure.
      The d-like character inside the Muffin-tin sphere is highlighted
    name: fleur-bandplot-spinpol-weighted
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands
from masci_tools.vis.fleur import plot_fleur_bands

#Read in data
with HDF5Reader('files/banddos_spinpol_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_bands(data,
                      attributes,
                      limits={'y': (-9,4)},
                      weight='MT:1d',
                      spinpol=False)
```

#### Selecting a specific spin channel

Providing `only_spin='up'` or `'down'` will plot only the given spin channel

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Bandstructure for a bulk Fe fcc structure (only spin up).
    name: fleur-bandplot-only-spin-up
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands
from masci_tools.vis.fleur import plot_fleur_bands

#Read in data
with HDF5Reader('files/banddos_spinpol_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_bands(data,
                      attributes,
                      limits={'y': (-9,4)},
                      only_spin='up',
                      markersize=10,
                      color='darkblue')
```

```{code-cell} ipython3
---
mystnb:
  remove_code_source: true
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Bandstructure for a bulk Fe fcc structure (only spin down).
      The color is changed manually
    name: fleur-bandplot-only-spin-down
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurBands
from masci_tools.vis.fleur import plot_fleur_bands

#Read in data
with HDF5Reader('files/banddos_spinpol_bands.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurBands)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_bands(data,
                      attributes,
                      limits={'y': (-9,4)},
                      only_spin='down',
                      markersize=10,
                      color='darkred')
```

## Density of States

Compatible Recipes for the {py:class}`~masci_tools.io.parsers.hdf5.reader.HDF5Reader`:

- `FleurDOS`: Default recipe reading in the total, interstitial, vacuum, atom and l-channel resolved DOS
- `FleurORBCOMP`: Read in the DOS from an orbital decomposition calculation
- `FleurJDOS`: Read in the DOS from a jDOS calculation
- `FleurMCD`: Read in the DOS from a MCD calculation

The dos visualization {py:func}`plot_fleur_dos()` can be used to plot
non spinpolarized and spinpolarized DOS, with selection of which components to plot.

### Standard density of states plot

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Non spinpolarized DOS for a bulk Si structure

    name: fleur-dos-simple
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurDOS
from masci_tools.vis.fleur import plot_fleur_dos

#Read in data
with HDF5Reader('files/banddos_dos.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurDOS)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_dos(data,
                    attributes,
                    limits={'energy': (-13,5)})
```

```{code-cell} ipython3
---
mystnb:
  remove_code_source: true
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Spinpolarized DOS for a bulk Fe fcc structure

    name: fleur-dos-spinpol-simple
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurDOS
from masci_tools.vis.fleur import plot_fleur_dos

#Read in data
with HDF5Reader('files/banddos_spinpol_dos.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurDOS)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_dos(data,
                    attributes,
                    limits={'energy': (-9,4)})
```

### Plotting options for DOS plots

The {py:func}`plot_fleur_dos()` function has a couple of options to modify, what is being
displayed from the `banddos.hdf` file. Below we show a few examples of ways to use these
options, together with examples of resulting plots.

#### Selecting specific DOS components

The DOS is made up of a lot of contributions that can be displayed separately.

Here we list the options that are available and show example plots for only selecting
the atom projected compinents of the density of states

- `plot_keys`: Can be used to provide a explicit list of keys you want to display (Same format as in the `banddos.hdf`)
- `show_total`: Control, whether to show the total density of states (default `True`)
- `show_interstitial`: Control, whether to show the interstitial contribution of the density of states (default `True`)
- `show_atoms`: Control, which total atom projected DOS to show. Can be either the string
  `all` (All components are shown), the value `None` (no components are shown) or a list
  of the integer indices of the atom types that should be displayed (default `all`)
- `show_lresolved`: Control, on which atoms to show the orbital projected DOS. Can be
  either the string `all` (All components are shown), the value `None`
  (no components are shown) or a list of the integer indices of the atom types for
  which to display the orbital components (default `None`)

Below an example of only displaying the atom projected DOS together with their orbital contributions is shown.

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Non spinpolarized DOS for a bulk Si structure.
      Only the atom and l-channel projected DOS is shown

    name: fleur-dos-selection
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurDOS
from masci_tools.vis.fleur import plot_fleur_dos

#Read in data
with HDF5Reader('files/banddos_dos.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurDOS)

ax = plot_fleur_dos(data, attributes,
                    show_total=False,
                    show_interstitial=False,
                    show_lresolved='all',
                    limits={'energy': (-13,5)})
```

```{code-cell} ipython3
---
mystnb:
  remove_code_source: true
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Non spinpolarized DOS for a bulk Fe fcc structure.
      Only the atom and l-channel projected DOS is shown

    name: fleur-dos-spinpol-selection
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurDOS
from masci_tools.vis.fleur import plot_fleur_dos

#Read in data
with HDF5Reader('files/banddos_spinpol_dos.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurDOS)

ax = plot_fleur_dos(data, attributes,
                    show_total=False,
                    show_interstitial=False,
                    show_lresolved='all',
                    limits={'energy': (-13,5)})
```

#### Plotting DOS without spinpolarization

Providing `spinpol=False` will display the DOS as non spinpolarized, even
if there are two spins in the data.

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      Non spinpolarized DOS for a bulk Fe fcc structure.
    name: fleur-dos-spinpol-false
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurDOS
from masci_tools.vis.fleur import plot_fleur_dos

#Read in data
with HDF5Reader('files/banddos_spinpol_dos.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurDOS)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_dos(data,
                    attributes,
                    limits={'energy': (-9,4)},
                    spinpol=False)
```

#### Selecting a specific spin channel

Providing `only_spin='up'` or `'down'` will plot only the given spin channel

```{code-cell} ipython3
---
mystnb:
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      DOS for a bulk Fe fcc structure (only spin up).
    name: fleur-dos-only-spin-up
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurDOS
from masci_tools.vis.fleur import plot_fleur_dos

#Read in data
with HDF5Reader('files/banddos_spinpol_dos.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurDOS)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_dos(data,
                    attributes,
                    limits={'energy': (-9,4)},
                    only_spin='up')
```

```{code-cell} ipython3
---
mystnb:
  remove_code_source: true
  image:
    align: center
    width: 100%
    classes: shadow bg-primary
  figure:
    caption: |
      DOS for a bulk Fe fcc structure (only spin down).
    name: fleur-dos-only-spin-down
---
from masci_tools.io.parsers.hdf5 import HDF5Reader
from masci_tools.io.parsers.hdf5.recipes import FleurDOS
from masci_tools.vis.fleur import plot_fleur_dos

#Read in data
with HDF5Reader('files/banddos_spinpol_dos.hdf') as h5reader:
   data, attributes = h5reader.read(recipe=FleurDOS)

#Plot the data
#Notice that you get the axis object of this plot is returned
#if you want to make any special additions
ax = plot_fleur_dos(data,
                    attributes,
                    limits={'energy': (-9,4)},
                    only_spin='down')
```
