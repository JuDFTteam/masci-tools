Developers Guide
================

This is the developers guide for masci-tools

.. contents::

Updating or adapting the Fleur Parsers
++++++++++++++++++++++++++++++++++++++++++++++++

Each input and output file for Fleur has a correspong XML-Schema, where the structure
of these files are defined.

To be able to parse such files efficiently and without hardcoding their structure we
extract all necessary infomration about the schemas in :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.inpschema_todict()`:
and :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.outschema_todict()`:. The resulting python dictionaries are stored
in ```.py``` files next to the schema and can be loaded via :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.load_inpschema()`:
or :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.load_outschema()`: by providing the version string.

To make maintenance of the plugin and the schemas easier, a couple of small utility functions are provided.
All functions below can either be called in python or on the commandline

.. topic:: Adding/modifying a new Fleur Schema:
  
  The :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.add_fleur_schema()`: can be used if a new ```FleurInputSchema.xsd```
  and ```FleurOutputSchema.xsd``` ar e to be added and parsed into their corresponding dictionaries. A usage example is provided
  below:
  
  .. code-block:: python

    from masci_tools.io.parsers.fleur.fleur_schema import add_fleur_schema

    #This function adds the Schemas to the folder with the corresponding version
    #and creates the parsed dicitionaries
    add_fleur_schema('/path/to/folder/with/schema/')

    #If the schema with the found version is found the above call will raise an exception
    #use overwrite=True to replace the schemas
    add_fleur_schema('/path/to/folder/with/schema/', overwrite=True)


   
.. topic:: Modifying the parsed Fleur Schema:

.. topic:: Adapting the outxml_parser:

