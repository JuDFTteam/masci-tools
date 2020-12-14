Developers Guide
================

This is the developers guide for masci-tools

.. contents::

Updating or adapting the Fleur Parsers
++++++++++++++++++++++++++++++++++++++++++++++++

Each input and output file for Fleur has a correspong XML-Schema, where the structure
of these files are defined.

To be able to parse such files efficiently and without hardcoding their structure we extract all necessary information about the schemas in :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.create_inpschema_dict()` and :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.create_outschema_dict()`. The resulting python dictionaries are stored in ```inpschema_dict.py``` or ```outschema_dict.py``` files next to the schema and can be loaded via the functions :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.load_inpschema()`
or :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.load_outschema()` by providing the desired version string.

To make maintenance of the plugin and the schemas easier, a couple of small utility functions are provided.
All functions below can either be called in python scripts or from the commandline

.. topic:: Adding/modifying a Fleur Schema:
  
  The :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.add_fleur_schema()` function can be used if a new ```FleurInputSchema.xsd``` or ```FleurOutputSchema.xsd``` are to be added and parsed into their corresponding dictionaries. A usage example is provided below:
  
  .. code-block:: python

    from masci_tools.io.parsers.fleur.fleur_schema import add_fleur_schema

    #This function adds the Schemas to the folder with the corresponding version
    #and creates the parsed dicitionaries
    add_fleur_schema('/path/to/folder/with/schema/')

    #If the schema with the found version is found the above call will raise an exception
    #use overwrite=True to replace the schemas
    add_fleur_schema('/path/to/folder/with/schema/', overwrite=True)
   
.. topic:: Modifying the parsed Fleur Schema:

  The :py:func:`~masci_tools.io.parsers.fleur.fleur_schema.update_schema_dicts()` function can be used if all available schemas should be be reparsed and all dictionaries updated, if the parsing functions are updated or a new key is added for example. This is really straightforward to use:
  
  .. code-block:: python

    from masci_tools.io.parsers.fleur.fleur_schema import update_schema_dicts

    #This function goes through all .xsd files in the version subfolder of masci_tools/io/parsers/fleur/fleur_schema
    #And creates a new dict and restores them
    update_schema_dicts()

.. topic:: Adapting the outxml_parser:

  In contrast to the input file parser :py:func:`~masci_tools.io.parsers.fleur.inpxml_parser()`, which parses all information available,
  the :py:func:`~masci_tools.io.parsers.fleur.outxml_parser()` has to be more flexible. The out file has much more information which might
  not be always useful for users. Therefore the selection of what is parsed has to be much more specific.
  
  This selection is expressed in the context of tasks. In general this corresponds to things like:
    - Total energy
    - Charge density distances
    - Magnetic moments
    - and so on ...

  These are expressed in a definition in form of a dictionary. Below a simple example (Total energy) is shown, which parses the ```value``` and ```units``` attribute of the ```totalEnergy``` tag. The hardcoded known parsing tasks can be found in :py:mod:`~masci_tools.io.parsers.fleur.default_parse_tasks`

  .. code-block:: python

    total_energy_definition = {
        'energy_hartree': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'totalEnergy'
            }
        },
    }

  The definition of a task can consist of multiple keys (in this case only ```energy_hartree```), which by default correspond to the keys in the resulting output dictionary. Each key has to contain the ```parse_type``` and ```path_spec``` key. The ```parse_type``` defines the method used to extract the information.

  The following are possible:
    :attrib: Will parse the value of the given attribute
    :text: Will parse the text of the given tag
    :numberNodes: Will return the number of nodes for the given tag
    :exists: Will return, whether the given tag exists
    :allAttribs: Will parse all known attributes at the given tag
                 into a dictionary
    :parentAttribs: Will parse all known attributes at the given tag
                    into a dictionary, but for the parent of the tag
    :singleValue: Special case of allAttribs to parse value and units
                  attribute for the given tag

  The ```path_spec``` key specifies how the key can be uniquely identified.

  It can contain the following specifications:
    :name: Name of the wanted tag/attribute (CASE SENSITIVE!!)
    :contains: A phrase, which has to occur in the path
    :no_contains: A phrase, which has to not occur in the path
    :exclude: list of str. Only valid for attributes (these are sorted into different categories
              ```unique```, ```unique_path``` and ```other```). This attribute can exclude one or more
              of these categories

  All except the ```name``` key are optional and should be constructed so that there is only one
  possible choice. Otherwise an exception is raised. There are other keywords, which can be entered
  here. These control how the parsed data is entered into the output dictionary. For a definition of these keywords, please refer to :py:mod:`~masci_tools.io.parsers.fleur.default_parse_tasks`.
