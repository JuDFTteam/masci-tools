Using the Fleur input/output parsers
+++++++++++++++++++++++++++++++++++++

.. role:: raw-html(raw)
   :format: html

.. contents::

Parser for the Fleur inp.xml file
----------------------------------

The fleur ```inp.xml``` contains all the information about the setup of a fleur calculation. To use this information in external scripts or aiida-fleur, the information needs to be parsed from the ```.xml``` format somehow.

For this purpose the :py:func:`~masci_tools.io.parsers.fleur.inpxml_parser()` is implemented. The usage is shown below. The input file is parsed recursively and all information is put into the dictionary.

.. code-block:: python

   from masci_tools.io.parsers.fleur import inpxml_parser

   input_dict = inpxml_parser('/path/to/random/inp.xml')

   #The call below will output warnings about failed conversions in the warnings dictionary
   warnings = {'parser_warnings': []}
   input_dict = inpxml_parser('/path/to/random/inp.xml', parser_info_out=warnings)

The conversion of each attribute or text is done according to the FleurInputSchema for the same version, which is stored in this repository for versions from ```0.27``` to ```0.34```. The following table shows the version compatibility of the input parser.

+------------------+------------------------------------------------------------------------------+
| File version     | Compatible?                                                                  |
+------------------+------------------------------------------------------------------------------+
| `0.27` - `0.34`  | :raw-html:`<font color="green"> Yes </font>`                                 |
+------------------+------------------------------------------------------------------------------+
| `0.35` -         | :raw-html:`<font color="#ffb733"> Fallback to <cite>0.34</cite> </font>`     |
+------------------+------------------------------------------------------------------------------+


Parser for the Fleur out.xml file
----------------------------------

For the ```out.xml``` file a similar parser is implemented. However, since the output file contains a lot more information, which is not always useful the :py:func:`~masci_tools.io.parsers.fleur.outxml_parser()` is defined a lot more selectively. But the usage is almost completely identical to the input file.

.. code-block:: python

   from masci_tools.io.parsers.fleur import outxml_parser

   #The default is that only the last stable iteration is parsed
   output_dict = outxml_parser('/path/to/random/out.xml')

   #Here all iterations are parsed
   output_dict = outxml_parser('/path/to/random/out.xml', iteration_to_parse='all')

   #Or the 5.
   output_dict = outxml_parser('/path/to/random/out.xml', iteration_to_parse=5)

   #The call below will output warnings about failed conversions in the warnings dictionary
   warnings = {'parser_warnings': []}
   output_dict = outxml_parser('/path/to/random/out.xml', parser_info_out=warnings)

For each iteration the parser decides based on the type of fleur calculation, what things should be parsed. For a more detailed explanation refer to the :doc:`../../devel_guide/index`.

The following table shows the version compatibility of the output parser. For versions before `0.34` the file version corresponds to the input version, since the output version is `0.27` for all versions before this point.

+------------------+-----------------------------------------------------------------------------------------------------+
| File version     | Compatible?                                                                                         |
+------------------+-----------------------------------------------------------------------------------------------------+
| `0.27` - `0.29`  | :raw-html:`<font color="#ffb733"> <cite>0.29</cite> version is assumed (no XML validation) </font>` |
+------------------+-----------------------------------------------------------------------------------------------------+
| `0.30` - `0.31`  | :raw-html:`<font color="#ffb733"> Yes (no XML validation) </font>`                                  |
+------------------+-----------------------------------------------------------------------------------------------------+
| `0.32`           | :raw-html:`<font color="red"> No (Does not exist for any release version of fleur) </font>`         |
+------------------+-----------------------------------------------------------------------------------------------------+
| `0.33`           | :raw-html:`<font color="#ffb733"> Yes (no XML validation) </font>`                                  |
+------------------+-----------------------------------------------------------------------------------------------------+
| `0.34`           | :raw-html:`<font color="green"> Yes </font>`                                                        |
+------------------+-----------------------------------------------------------------------------------------------------+
| `0.35` -         | :raw-html:`<font color="#ffb733"> Fallback to <cite>0.34</cite> </font>`                            |
+------------------+-----------------------------------------------------------------------------------------------------+

Using the :py:mod:`~masci_tools.util.schema_dict_util` functions
-----------------------------------------------------------------

If only a small amount of information is required from the input or output files of fleur the full parsers might be overkill. But there are a number of utility functions allowing easy access to information from the ```.xml``` files without knowing the exact xpath expressions for each version of the input/output. A code example extracting information from a input file is given below.

.. code-block:: python

   from masci_tools.io.io_fleurxml import load_inpxml
   from masci_tools.util.schema_dict_util import read_constants #Read in predefined constants
   from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath

   #First we create a xml-tree from the input file and load the desired input schema dictionary
   xmltree, schema_dict = load_inpxml('/path/to/inp.xml')
   root = xmltree.getroot()

   #For the input file there can be predefined contants
   constants = read_constants(root, schema_dict)

   #Here an example of extracting some attributes. The interface to all functions in
   #schema_dict_util is the same

   #Number of spins
   spins = evaluate_attribute(root, schema_dict, 'jspins', constants)

   #Planewave cutoff (notice the names are case-insensitive, 'KMAX' would work as well)
   kmax = evaluate_attribute(root, schema_dict, 'kmax', constants)

   #Some attributes need to be specified further for a distinct path
   #`radius` exists both for atom species and atom groups so we give a phrase to distinguish them
   mt_radii = evaluate_attribute(root, schema_dict, 'radius', constants, contains='species')

   #But we can also make implicit constraints
   # 1. Get some element in the xml tree, where the path is more specified. In the example lets
   #    get the element containing all species
   # 2. If we evaluate the `radius` attribute now on the species elements, we do not need
   #    the contains parameter, since from the point of the species element there is only one possibility
   #    for the `radius` attribute

   species = eval_simple_xpath(root, schema_dict, 'atomSpecies')
   mt_radii = evaluate_attribute(species, schema_dict, 'radius', constants)
