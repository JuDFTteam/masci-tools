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

### Modification registration methods

The registration methods can be separated into two groups. First of all,
there are XML methods that require deeper knowledge about the structure of an `inp.xml` file.
All of them require an xpath input and start their method names start with `xml_`:

- {py:meth}`FleurXMLModifier.xml_set_attrib_value_no_create()`: Set attributes on the result(s) of the given xpath
- {py:meth}`FleurXMLModifier.xml_set_text_no_create()`: Set text on the result(s) of the given xpath
- {py:meth}`FleurXMLModifier.xml_create_tag()`: Insert
  an xml element in the xml tree on the result(s) of the given xpath.
- {py:meth}`FleurXMLModifier.xml_delete_tag()`: Delete
  an xml element in the xml tree on the result(s) of the given xpath.
- {py:meth}`FleurXMLModifier.xml_delete_att()`: Delete
  an attribute in the xml tree on the result(s) of the given xpath.
- {py:meth}`FleurXMLModifier.xml_replace_tag()`: Replace an xml element on the result(s) of the given xpath.

On the other hand, there are shortcut methods that already know some paths:

- {py:meth}`FleurXMLModifier.set_species()`: Specific
  user-friendly method to change species parameters.
- {py:meth}`FleurXMLModifier.clone_species()`: Method to
  create a clone of a given species with optional modifications
- {py:meth}`FleurXMLModifier.set_atomgroup()`:  Specific
  method to change atom group parameters.
- {py:meth}`FleurXMLModifier.set_species_label()`: Specific
  user-friendly method to change a species of an atom with a certain label.
- {py:meth}`FleurXMLModifier.set_atomgroup_label()`:  Specific
  method to change atom group parameters of an atom with a certain label.
- {py:meth}`FleurXMLModifier.switch_species()`: user-friendly method for switching the atom species of a atom group
- {py:meth}`FleurXMLModifier.switch_species_label()`: user-friendly method for switching the atom species of a atom group with an atom with a certain label.
- {py:meth}`FleurXMLModifier.set_nkpts()`: user-friendly method for setting the `kPointCount` (**Only for MaX4 and older**)
- {py:meth}`FleurXMLModifier.set_kpath()`: user-friendly method for setting the path for a bandstructure calculations (**Only for MaX4 and older**)
- {py:meth}`FleurXMLModifier.set_kpointlist()`: user-friendly method for setting/creating a `kPointlist` from lists
- {py:meth}`FleurXMLModifier.switch_kpointset()`: user-friendly method for switching the used kpoint set in a calculation (**Only for MaX5 and newer**)
- {py:meth}`FleurXMLModifier.set_inpchanges()`: Specific
  user-friendly method for easy changes of attribute key value type.
- {py:meth}`FleurXMLModifier.shift_value()`: Specific
  user-friendly method to shift value of an attribute.
- {py:meth}`FleurXMLModifier.shift_value_species_label()`: Specific
  user-friendly method to shift value of an attribute of an atom with a certain label.
- {py:meth}`FleurXMLModifier.set_attrib_value()`: user-friendly method for setting attributes in the xml file by specifying their name
- {py:meth}`FleurXMLModifier.set_first_attrib_value()`: user-friendly method for setting the first occurrence of an attribute in the xml file by specifying its name
- {py:meth}`FleurXMLModifier.add_number_to_attrib()`: user-friendly method for adding to or multiplying values of attributes in the xml file by specifying their name
- {py:meth}`FleurXMLModifier.add_number_to_first_attrib()`: user-friendly method for adding to or multiplying values of the first occurrence of the attribute in the xml file by specifying their name
- {py:meth}`FleurXMLModifier.set_text()`: user-friendly method for setting text on xml elements in the xml file by specifying their name
- {py:meth}`FleurXMLModifier.set_first_text()`: user-friendly method for setting the text on the first occurrence of an xml element in the xml file by specifying its name
- {py:meth}`FleurXMLModifier.set_simple_tag()`: user-friendly method for creating and setting attributes on simple xml elements (only attributes) in the xml file by specifying its name
- {py:meth}`FleurXMLModifier.set_complex_tag()`: user-friendly method for creating complex tags in the xml file by specifying its name
- {py:meth}`FleurXMLModifier.create_tag()`: User-friendly method for inserting a tag in the right place by specifying it's name
- {py:meth}`FleurXMLModifier.delete_tag()`: User-friendly method for delete a tag by specifying it's name
- {py:meth}`FleurXMLModifier.delete_att()`: User-friendly method for deleting an attribute from a tag by specifying it's name
- {py:meth}`FleurXMLModifier.replace_tag()`: User-friendly method for replacing a tag by another by specifying its name
- {py:meth}`FleurXMLModifier.set_nmmpmat()`: Specific
  method for initializing or modifying the density matrix file for a LDA+U calculation (details see below)
- {py:meth}`FleurXMLModifier.rotate_nmmpmat()`: Specific
  method for rotating a block/blocks of the density matrix file for a LDA+U calculation (details see below) in real space
- {py:meth}`FleurXMLModifier.align_nmmpmat_to_sqa()`: Specific
  method for aligning a block/blocks of the density matrix file for a LDA+U calculation (details see below) in real space with the SQA already specified in the `inp.xml`

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
