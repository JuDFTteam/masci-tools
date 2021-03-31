.. _fleurxml_mod:

FleurXMLModifier
+++++++++++++++++

Description
-----------
The :py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier` class can be
used if you want to change anything in a `inp.xml` file in an easy and robust way.
It will validate all the changes you wish to do and apply all these changes to a given
`inp.xml` and produce a new xmltree.

Usage
------
To modify an existing `inp.xml`, a
:py:class:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier` instance
has to be initialised.
After that, a user should register
certain modifications which will be cached. They will be applied on
a given `inp.xml`. However, the provided `inp.xml` will not be changed but only
a modified xmltree is returned, which you can store in a new `.xml` file.

.. code-block:: python

  from masci_tools.io.fleurxmlmodifier import  FleurXMLModifier

  fm = FleurXMLModifier()                                      # Initialise FleurXMLModifier class
  fm.set_inpchanges({'dos' : True, 'Kmax': 3.9 })              # Add changes
  new_xmltree = fm.modify_xmlfile('/path/to/original/inp.xml') #Apply

User Methods
------------

General methods
_______________

    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.modify_xmlfile()`: Applies the registered changes to a given `inp.xml` (and optional `n_mmp_mat` file)
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.changes()`: Displays the
      current list of changes.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.undo()`: Removes the
      last task or all tasks from the list of changes.

.. _modify_methods:

Modification registration methods
_________________________________
The registration methods can be separated into two groups. First of all,
there are XML methods that require deeper knowledge about the structure of an ``inp.xml`` file.
All of them require an xpath input and start their method names start with `xml_`:

    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.xml_set_attrib_value_no_create()`: Set attributes on the result(s) of the given xpath
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.xml_set_text_no_create()`: Set text on the result(s) of the given xpath
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.xml_create_tag()`: Insert
      an xml element in the xml tree on the result(s) of the given xpath.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.xml_delete_tag()`: Delete
      an xml element in the xml tree on the result(s) of the given xpath.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.xml_delete_att()`: Delete
      an attribute in the xml tree on the result(s) of the given xpath.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.xml_replace_tag()`: Replace an xml element on the result(s) of the given xpath.

On the other hand, there are shortcut methods that already know some paths:

    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_species()`: Specific
      user-friendly method to change species parameters.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_atomgroup()`:  Specific
      method to change atom group parameters.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_species_label()`: Specific
      user-friendly method to change a species of an atom with a certain label.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_atomgroup_label()`:  Specific
      method to change atom group parameters of an atom with a certain label.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_inpchanges()`: Specific
      user-friendly method for easy changes of attribute key value type.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.shift_value()`: Specific
      user-friendly method to shift value of an attribute.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.shift_value_species_label()`: Specific
      user-friendly method to shift value of an attribute of an atom with a certain label.
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_attrib_value()`: user-friendly method for setting attributes in the xml file by specifying their name
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_first_attrib_value()`: user-friendly method for setting the first occurrence of an attribute in the xml file by specifying its name
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.add_number_to_attrib()`: user-friendly method for adding to or multiplying values of attributes in the xml file by specifying their name
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_first_attrib_value()`: user-friendly method for adding to or multiplying values of the first occurrence of an attribute in the xml file by specifying its name
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_text()`: user-friendly method for setting text on xml elements in the xml file by specifying their name
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_first_text()`: user-friendly method for setting the text on the first occurrence of an xml element in the xml file by specifying its name
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_simple_tag()`: user-friendly method for creating and setting attributes on simple xml elements (only attributes) in the xml file by specifying its name
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_complex_tag()`: user-friendly method for creating complex tags in the xml file by specifying its name
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_nmmpmat()`: Specific 
      method for initializing or modifying the density matrix file for a LDA+U calculation (details see below)
    * :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.rotate_nmmpmat()`: Specific 
      method for rotating a block of the density matrix file for a LDA+U calculation (details see below) in real space

.. The figure below shows a comparison between the use of XML and shortcut methods.

  .. image:: images/registration_methods.png
    :width: 100%
    :align: center

Modifying the density matrix for LDA+U calculations
---------------------------------------------------

The above mentioned :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.set_nmmpmat()` and :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.rotate_nmmpmat()` take a special
role in the modification registration methods, as the modifications are not done on the ``inp.xml`` file but the
density matrix file ``n_mmp_mat`` used by Fleur for LDA+U calculations. The resulting new `n_mmp_mat` file is returned next to the new `inp.xml` by
the :py:func:`~masci_tools.io.fleurxmlmodifier.FleurXMLModifier.modify_xmlfile()`.

The code example below shows how to use this method to add a LDA+U procedure to an atom species and provide
an initial guess for the density matrix.

.. code-block:: python

  from masci_tools.io.fleurxmlmodifier import FleurXMLModifier

  fm = FleurXMLModifier()                                              # Initialise FleurXMLModifier class
  fm.set_species('Nd-1', {'ldaU':                                      # Add LDA+U procedure
                         {'l': 3, 'U': 6.76, 'J': 0.76, 'l_amf': 'F'}}) 
  fm.set_nmmpmat('Nd-1', orbital=3, spin=1, occStates=[1,1,1,1,0,0,0]) # Initialize n_mmp_mat file with the states
                                                                       # m = -3 to m = 0 occupied for spin up
                                                                       # spin down is initialized with 0 by default
  new_xmltree, nmmp_content = fm.modify_xmlfile('/path/to/original/inp.xml')         # Apply

.. note::
    The ``n_mmp_mat`` file is a simple text file with no knowledge of which density matrix block corresponds to which
    LDA+U procedure. They are read in the same order as they appear in the ``inp.xml``. For this reason the ``n_mmp_mat``
    file can become invalid if one adds/removes a LDA+U procedure to the ``inp.xml`` after the ``n_mmp_mat`` file was 
    initialized. Therefore any modifications to the `n_mmp_mat` file should be done after adding/removing or modifying the LDA+U configuration.
    
