# Using the Fleur input/output parsers

```{contents}
```

```{eval-rst}
.. currentmodule:: masci_tools.io.parsers.fleur
```

## Parser for the Fleur inp.xml file

The fleur `inp.xml` contains all the information about the setup of a fleur calculation.
To use this information in external scripts or aiida-fleur, the information needs to be
parsed from the `.xml` format somehow.

For this purpose the {py:func}`inpxml_parser()` is implemented. The usage is shown below.
The input file is parsed recursively and all information is put into the dictionary.

```python
from masci_tools.io.parsers.fleur import inpxml_parser

input_dict = inpxml_parser('/path/to/random/inp.xml')

#The call below will output warnings about failed conversions in the warnings dictionary
warnings = {'parser_warnings': []}
input_dict = inpxml_parser('/path/to/random/inp.xml', parser_info_out=warnings)
```

The conversion of each attribute or text is done according to the FleurInputSchema for the
same version, which is stored in this repository for versions from `0.27` to `0.35`.
The following table shows the version compatibility of the input parser.

|File Version|Compatible  |
|--|--|
| `0.27` - `0.36` |<span style="color:green;">Yes</span> |
| `0.37` |<span style="color:#ffb733;">Fallback to <cite>0.36</cite></span>  |


## Parser for the Fleur out.xml file

For the `out.xml` file a similar parser is implemented. However, since the output file
contains a lot more information, which is not always useful the {py:func}`outxml_parser()`
is defined a lot more selectively. But the usage is almost completely identical to the input file.

```python
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
```

For each iteration the parser decides based on the type of fleur calculation,
what things should be parsed. For a more detailed explanation refer to the
{ref}`devguidefleurxml`.

The following table shows the version compatibility of the output parser.
For versions before `0.34` the file version corresponds to the input version,
since the output version is `0.27` for all versions before this point.

|File Version|Compatible  |
|--|--|
| `0.27` - `0.29` |<span style="color:#ffb733;"><cite>0.29</cite> version is assumed  (no XML validation)</span> |
| `0.30` - `0.31` |<span style="color:#ffb733;">Yes (no XML validation)</span>  |
| `0.32` | <span style="color:red;">No (Does not exist for any release version of fleur)</span> |
| `0.33` |<span style="color:#ffb733;">Yes (no XML validation)</span> |
| `0.34` - `0.36` |<span style="color:green;">`Yes</span> |
| `0.37` -  |<span style="color:#ffb733;">Fallback to <cite>0.36</cite></span> |


````{admonition} Using File handles
Both the {py:func}`inpxml_parser()` and {py:func}`outxml_parser()`
can also be used with file handles like shown below.

```python
 from masci_tools.io.parsers.fleur import inpxml_parser

 with open('/path/to/random/inp.xml', 'rb') as file:
    input_dict = inpxml_parser(file)
```

Notice that the file has to be opened in binary mode.
````

## XML getter functions

There are a number of functions for extracting specific parts of the XML files
in the {py:mod}`~masci_tools.util.xml.xml_getters` module. The following are available:

```{eval-rst}
.. currentmodule:: masci_tools.util.xml.xml_getters
```

- {py:func}`get_fleur_modes()`: Get information about the mode of the fleur calculation
- {py:func}`get_nkpts()`: Get the (for older versions approximate if not `kPointList` is
  used) number of kpoints to be used in the calculation
- {py:func}`get_cell()`: Get the Bravais matrix of the system
- {py:func}`get_parameterdata()`: Get the information about the calculation parameters
  needed to reproduce a calculation starting from the inpgen
- {py:func}`get_structuredata()`: Get the structure from the xml file
  (atom positions + unit cell)
- {py:func}`get_kpointsdata()`: Get the defined kpoint sets (single/multiple)
  from the xml file (kpoints + weights + unit cell)
- {py:func}`get_relaxation_information()`: Get the relaxation history and current displacements
- {py:func}`get_symmetry_information()`: Get the symmetry operations used in the calculation

All of these are used in the same way

```python
from masci_tools.io.fleur_xml import load_inpxml
from masci_tools.util.xml.xml_getters import get_fleur_modes

xmltree, schema_dict = load_inpxml('/path/to/inp.xml')

fleur_modes = get_fleur_modes(xmltree, schema_dict)
print(fleur_modes)
```

## Using the {py:mod}`~masci_tools.util.schema_dict_util` functions

If only a small amount of information is required from the input or output files
of fleur the full parsers might be overkill. But there are a number of utility
functions allowing easy access to information from the `.xml` files without knowing
the exact XPath expressions for each version of the input/output. A code example extracting
information from a input file is given below.

```python
from masci_tools.io.fleur_xml import load_inpxml
from masci_tools.util.schema_dict_util import evaluate_attribute, eval_simple_xpath

#First we create a xml-tree from the input file and load the desired input schema dictionary
xmltree, schema_dict = load_inpxml('/path/to/inp.xml')
root = xmltree.getroot()

#Here an example of extracting some attributes. The interface to all functions in
#schema_dict_util is the same

#Number of spins
spins = evaluate_attribute(root, schema_dict, 'jspins')

#Planewave cutoff (notice the names are case-insensitive, 'KMAX' would work as well)
kmax = evaluate_attribute(root, schema_dict, 'kmax')

#Some attributes need to be specified further for a distinct path
#`radius` exists both for atom species and atom groups so we give a phrase to distinguish them
mt_radii = evaluate_attribute(root, schema_dict, 'radius', contains='species')

#But we can also make implicit constraints
# 1. Get some element in the xml tree, where the path is more specified. In the example lets
#    get the element containing all species
# 2. If we evaluate the `radius` attribute now on the species elements, we do not need
#    the contains parameter, since from the point of the species element there is only one possibility
#    for the `radius` attribute

species = eval_simple_xpath(root, schema_dict, 'atomSpecies')
mt_radii = evaluate_attribute(species, schema_dict, 'radius')
```

To manage the context of these functions the {py:func}`~masci_tools.io.fleur_xml.FleurXMLContext()`
is available to write the same code as above more concisely.

```python
from masci_tools.io.fleur_xml import load_inpxml, FleurXMLContext
xmltree, schema_dict = load_inpxml('/path/to/inp.xml')

with FleurXMLContext(xmltree, schema_dict) as root:
   spins = root.attribute('jspins')
   noco = root.attribute('l_noco', default=False)

   #Not nesting the context we need to specify which elements are meant
   mt_radii = root.attribute('radius', contains='species')

   #Nesting using find (the first element is return)
   with root.find('atomspecies') as all_species:
         mt_radii = all_species.attribute('radius')

   #Nesting using iter (each iteration returns a new context for the next element)
   mt_radii = []
   for species in root.iter('species'):
         mt_radii.append(species.attribute('radius'))
```
