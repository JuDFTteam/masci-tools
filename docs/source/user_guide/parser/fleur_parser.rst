Using the Fleur input/output parsers
====================================

.. contents::

Parser for the Fleur inp.xml file
+++++++++++++++++++++++++++++++++

The fleur ```inp.xml``` contains all the information about the setup of a fleur calculation. To use this information in external scripts or aiida-fleur, the information needs to be parsed from the ```.xml``` format somehow.

For this purpose the :py:func:`~masci_tools.io.parsers.fleur.inpxml_parser()` is implemented. The usage is shown below. The input file is parsed recursively and all information is put into the dictionary.

.. code-block:: python

   from masci_tools.io.parsers.fleur import inpxml_parser

   input_dict = inpxml_parser('/path/to/random/inp.xml')

   #The call below will output warnings about failed conversions in the warnings dictionary
   warnings = {'parser_warnings': []}
   input_dict = inpxml_parser('/path/to/random/inp.xml', parser_info_out=warnings)

The conversion of each attribute or text is done according to the FleurInputSchema for the same version, which is stored in this repository for versions from ```0.27``` to ```0.33```


Parser for the Fleur out.xml file
+++++++++++++++++++++++++++++++++

For the ```out.xml``` file a similar parser is implemented. However, since the ouput file contains a lot more information, which is not always useful the :py:func:`~masci_tools.io.parsers.fleur.outxml_parser()` is defined a lot more selectively. But the usage is almost completely identical to the input file.

.. code-block:: python

   from masci_tools.io.parsers.fleur import outxml_parser

   #The default is that only the last stable iteration is parsed
   output_dict = inpxml_parser('/path/to/random/out.xml')

   #Here all iterations are parsed
   output_dict = inpxml_parser('/path/to/random/out.xml', iteration_to_parse='all')

   #Or the 5.
   output_dict = inpxml_parser('/path/to/random/out.xml', iteration_to_parse=5)

   #The call below will output warnings about failed conversions in the warnings dictionary
   warnings = {'parser_warnings': []}
   input_dict = inpxml_parser('/path/to/random/out.xml', parser_info_out=warnings)

For each iteration the parser decides based on the type of fleur calculation, what things should be parsed. For a more detailed explanation refer to the :doc:`../../devel_guide/index`.

