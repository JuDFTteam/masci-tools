(fleurxml-mod)=

# FleurXMLModifier

```{eval-rst}
.. currentmodule:: masci_tools.io.fleurxmlmodifier
```

## Description

The {py:class}`FleurXMLModifier` class can be used if you want to change anything in a
`inp.xml` file in an easy and robust way. It will validate all the changes you wish
to do and apply all these changes to a given `inp.xml` and produce a new XML tree.

## Usage

To modify an existing `inp.xml`, a {py:class}`FleurXMLModifier` instance has to be initialised.
After that, a user should register certain modifications which will be cached.
They will be applied on a given `inp.xml`. However, the provided `inp.xml` will not be
changed but only a modified XML tree is returned, which you can store in a new `.xml` file.

```python
from masci_tools.io.fleurxmlmodifier import  FleurXMLModifier

fm = FleurXMLModifier()                                      # Initialise FleurXMLModifier class
fm.set_inpchanges({'dos' : True, 'Kmax': 3.9 })              # Add changes
new_xmltree, _ = fm.modify_xmlfile('/path/to/original/inp.xml') #Apply 
```

## User Methods

### General methods

- {py:meth}`FleurXMLModifier.modify_xmlfile()`: Applies the registered changes to a
  given `inp.xml` (and optional `n_mmp_mat` file)
- {py:meth}`FleurXMLModifier.changes()`: Displays the current list of changes.
- {py:meth}`FleurXMLModifier.undo()`: Removes the
  last task or all tasks from the list of changes.

(modify-methods)=
### Modification methods

::::::{dropdown} Simple changes
:open:
:color: info
:animate: fade-in-slide-down

:::::{grid} 2

::::{grid-item-card} **set_inpchanges**
:text-align: center
Change the value of multiple text or attribute values at once.
+++
:::{button-ref} set_inpchanges
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **shift_value**
:text-align: center
Shift or multiply the value of multiple text or attribute values at once.
+++
:::{button-ref} shift_value
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::
:::::

::::::

::::::{dropdown} Modifying atom species
:open:
:color: info
:animate: fade-in-slide-down

:::::{grid} 2

::::{grid-item-card} **set_species**
:text-align: center
Change parameters or add new tags in atomic `species` elements.
For example changing the MT radius or adding DFT+U.
+++
:::{button-ref} set_species
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_species_label**
:text-align: center
Change parameters or add new tags in atomic `species` of a
specific atom. The atom is identified by it's label.
+++
:::{button-ref} set_species_label
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **clone_species**
:text-align: center
Duplicate a given species element with a different name.
+++
:::{button-ref} clone_species
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::
:::::
::::::

::::::{dropdown} Modifying atom groups
:open:
:color: info
:animate: fade-in-slide-down

:::::{grid} 2

::::{grid-item-card} **set_atomgroup**
:text-align: center
Change parameters or add new elements in `atomGroup` elements,
i.e. the elements containing the symmetry equivalent atoms.
+++
:::{button-ref} set_atomgroup
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_atomgroup_label**
:text-align: center
Change parameters or add new elements in `atomGroup` elements,
i.e. the elements containing the symmetry equivalent atoms.
The group to modify is identified by a given label of an atom.
+++
:::{button-ref} set_atomgroup_label
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **switch_species**
:text-align: center
Change the species of a given atom group.
+++
:::{button-ref} switch_species
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **switch_species_label**
:text-align: center
Change the species of a atom group containing a given atom.
+++
:::{button-ref} switch_species
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

:::::
::::::

::::::{dropdown} Modifying kpoint sets
:open:
:color: info
:animate: fade-in-slide-down

:::::{grid} 2

::::{grid-item-card} **switch_kpointset**
:text-align: center
Switch the used kpoint set {bdg-success-line}`MaX 5.0 or newer`
+++
:::{button-ref} switch_kpointset 
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_kpointlist**
:text-align: center
Create a k-point list from a list of coordinates and weights.
+++
:::{button-ref} set_kpointlist 
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_nkpts**
:text-align: center
Set the number of kpts (`kpointCount`) {bdg-danger-line}`MaX 4.0 or older`
+++
:::{button-ref} set_nkpts 
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_kpath**
:text-align: center
Set a explicit path for bandstructure {bdg-danger-line}`MaX 4.0 or older`
+++
:::{button-ref} set_kpath 
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

:::::
::::::

::::::{dropdown} Setting generic XML elements and attributes
:open:
:color: info
:animate: fade-in-slide-down

:::::{grid} 2

::::{grid-item-card} **set_attrib_value**
:text-align: center
Set abitrary XML attribute values
+++
:::{button-ref} set_attrib_value
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_first_attrib_value**
:text-align: center
Set abitrary XML attribute values for the
first occurrence of the given attribute in the XML tree
+++
:::{button-ref} set_first_attrib_value
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::


::::{grid-item-card} **set_text**
:text-align: center
Set the text of arbitrary XML elements
+++
:::{button-ref} set_text
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_first_text**
:text-align: center
Set the text of arbitrary XML elements for the first
occurrence of the given element in the XML tree
+++
:::{button-ref} set_first_text
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **add_number_to_attrib**
:text-align: center
Add to or multiply the values of arbitrary XML
attributes
+++
:::{button-ref} add_number_to_attrib
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **add_number_to_first_attrib**
:text-align: center
Add to or multiply the values of arbitrary XML
attributes for the first occurrence of the given attribute
in the XML tree
+++
:::{button-ref} add_number_to_first_attrib
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_simple_tag**
:text-align: center
Create or change arbitrary simple XML elements, i.e. elements
without child elements
+++
:::{button-ref} set_simple_tag
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **set_complex_tag**
:text-align: center
Create or change an arbitrary complex XML element, i.e. an element
with child elements.
+++
:::{button-ref} set_complex_tag
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

:::::
::::::

::::::{dropdown} Manipulating the DFT+U density matrix
:color: info
:animate: fade-in-slide-down

:::::{grid} 2

::::{grid-item-card} **set_nmmpmat**
:text-align: center
Initialize the `n_mmp_mat` file with a given density matrix
+++
:::{button-ref} set_nmmpmat
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **rotate_nmmpmat**
:text-align: center
Rotate one or multiple block(s) of the `n_mmp_mat` with euler angles
+++
:::{button-ref} rotate_nmmpmat
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **align_nmmpmat_to_sqa**
:text-align: center
Rotate one or multiple blocks of the `n_mmp_mat` with euler angles to align
with the spin-quantization axis specified.
+++
:::{button-ref} align_nmmpmat_to_sqa
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

:::::
::::::


::::::{dropdown} Using explicit XPath expressions for modifications
:color: warning
:icon: Alert
:animate: fade-in-slide-down

These routines should be used with a lot of care, since they have
much less checks than all other setting functions

:::::{grid} 2

::::{grid-item-card} **xml_create_tag**
:text-align: center
Create a XML element with the given name as a child of the
results of the XPath expression
+++
:::{button-ref} xml_create_tag
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **xml_delete_tag**
:text-align: center
Delete the results of the XPath expression.
+++
:::{button-ref} xml_delete_tag
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **xml_delete_att**
:text-align: center
Delete a give  XML attribute from the results of the XPath expression.
+++
:::{button-ref} xml_delete_att
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **xml_replace_tag**
:text-align: center
Replace the results of the XPath expression with a given XML element.
+++
:::{button-ref} xml_replace_tag
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **xml_set_attrib_value_no_create**
:text-align: center
Set XML attribute values on the results of the XPath expression.
+++
:::{button-ref} xml_set_attrib_value_no_create
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::

::::{grid-item-card} **xml_set_text_no_create**
:text-align: center
Set text on the results of the XPath expression.
+++
:::{button-ref} xml_set_text_no_create
:ref-type: ref
:click-parent:
:expand:
:color: primary
:outline:
Show Examples
:::
::::



:::::
::::::


% The figure below shows a comparison between the use of XML and shortcut methods.
%
% .. image:: images/registration_methods.png
%   :width: 100%
%   :align: center

## Modifying the density matrix for LDA+U calculations

The above mentioned {py:meth}`FleurXMLModifier.set_nmmpmat()`, {py:meth}`FleurXMLModifier.rotate_nmmpmat()` and
{py:meth}`FleurXMLModifier.align_nmmpmat_to_sqa()` take a special role in the modification registration methods,
as the modifications are not done on the `inp.xml` file but the density matrix file `n_mmp_mat` used by Fleur
for LDA+U calculations. The resulting new `n_mmp_mat` file is returned next to the new `inp.xml` by
the {py:meth}`FleurXMLModifier.modify_xmlfile()`.

The code example below shows how to use this method to add a LDA+U procedure to an atom species and provide
an initial guess for the density matrix.

```python
from masci_tools.io.fleurxmlmodifier import FleurXMLModifier

fm = FleurXMLModifier()
# Add LDA+U procedure
fm.set_species('Nd-1', {'ldaU':{'l': 3, 'U': 6.76, 'J': 0.76, 'l_amf': 'F'}})
# Initialize n_mmp_mat file with the states m = -3 to m = 0 occupied for spin up
# spin down is initialized with 0 by default, since no n_mmp_mat file is provided
fm.set_nmmpmat('Nd-1', orbital=3, spin=1, state_occupations=[1,1,1,1,0,0,0])
new_xmltree, add_files = fm.modify_xmlfile('/path/to/original/inp.xml')
print(add_files['n_mmp_mat'])
```

:::{note}
The `n_mmp_mat` file is a simple text file with no knowledge of which density matrix block corresponds to which
LDA+U procedure. They are read in the same order as they appear in the `inp.xml`. For this reason the `n_mmp_mat`
file can become invalid if one adds/removes a LDA+U procedure to the `inp.xml` after the `n_mmp_mat` file was
initialized. Therefore any modifications to the `n_mmp_mat` file should be done after adding/removing or modifying the LDA+U configuration.
:::
