(devguidefleurxml)=

# Updating or adapting the Fleur Parsers

```{eval-rst}
.. currentmodule:: masci_tools.io.parsers.fleur_schema
```

:::{note}
A more detailed walkthrough of the important design decisions concerning the implementation
Fleur XML parsers and IO capabilities can be found in this
[document](https://python-fleur-xml-design.readthedocs.io/en/latest/)
:::

Each input and output file for Fleur has a correspong XML-Schema, where the structure
of these files are defined.

To be able to parse such files efficiently and without hardcoding their structure
we extract all necessary information about the schemas in the modules under
{py:mod}`~masci_tools.io.parsers.fleur_schema`. The resulting python dictionaries
can be accessed via the classes {py:class}`InputSchemaDict` and {py:class}`OutputSchemaDict`.
The easiest way to instantiate one of these objects is to use the
{py:meth}`InputSchemaDict.fromVersion()` or {py:meth}`OutputSchemaDict.fromVersion()` methods
by providing the desired version string.

## Adding/modifying a Fleur Schema:

The command `masci-tools fleur-schema add <path-to-schema-file>` can be used to add
the schema to the repository. If the schema for the specified version already exists
an error is raised. To ignore this error the option `--overwrite` can be used.

## Adapting the outxml_parser:

```{eval-rst}
.. currentmodule:: masci_tools.io.parsers.fleur
```

In contrast to the input file parser {py:func}`inpxml_parser()`, which parses all information available,
the {py:func}`outxml_parser()` has to be more flexible. The out file has much more information which might
not be always useful for users. Therefore the selection of what is parsed has to be much more specific.

This selection is expressed in the context of tasks. In general this corresponds to things like:
\- Total energy
\- Charge density distances
\- Magnetic moments
\- and so on ...

These are expressed in a definition in form of a dictionary. Below a simple example
(Total energy) is shown, which parses the `value` and `units` attribute of the
`totalEnergy` tag. The hardcoded known parsing tasks can be found in
{py:mod}`~masci_tools.io.parsers.fleur.default_parse_tasks`.

```python
total_energy_definition = {
    'energy_hartree': {
        'parse_type': 'singleValue',
        'path_spec': {
            'name': 'totalEnergy'
        }
    },
}
```

The definition of a task can consist of multiple keys (in this case only `energy_hartree`),
which by default correspond to the keys in the resulting output dictionary. Each key has
to contain the `parse_type` and `path_spec` key. The `parse_type` defines the
method used to extract the information.

The following are possible:

:attrib: Will parse the value of the given attribute
:text: Will parse the text of the given tag
:numberNodes: Will return the number of nodes for the given tag
:exists: Will return, whether the given tag exists
:attrib_exists: Will return, whether the given attribute exists
:allAttribs: Will parse all known attributes at the given tag
              into a dictionary
:parentAttribs: Will parse all known attributes at the given tag
                into a dictionary, but for the parent of the tag
:singleValue: Special case of allAttribs to parse value and units
              attribute for the given tag
:xmlGetter: Will execute a function in the module {py:mod}`~masci_tools.util.xml.xml_getters` given in the `name` entry

The `path_spec` key specifies how the key can be uniquely identified.
It can contain the following specifications:

:name: Name of the wanted tag/attribute
:contains: A phrase, which has to occur in the path
:not_contains: A phrase, which has to not occur in the path
:exclude: list of str. Only valid for attributes (these are sorted into different
          categories `unique`, `unique_path` and `other`). This attribute can
          exclude one or more of these categories

All except the `name` key are optional and should be constructed so that there is only one
possible choice. Otherwise an exception is raised. There are other keywords, which can be entered
here. These control how the parsed data is entered into the output dictionary.
For a definition of these keywords, please refer to
{py:mod}`~masci_tools.io.parsers.fleur.default_parse_tasks`.

Each task can also contain a number of control keys, determining when to perform the tasks.
Each of these keys begins with an underscore. All of these are optional.
The following are valid:

:_general: bool, if True (default False) the task is not performed for
           each iteration but once on the root of the file
:_minimal: bool, if True the task is performed even when `minimal_mode = True`
           is given
:_modes: list of tuples specifying requirements on the `fleur_modes` for the task.
         For example `[('jspins', 2), ('soc', True)]` will only perform the task for a
         magnetic SOC calculation
:_conversions: list of str, giving the names of functions to call after this task.
               Functions given here have to be decorated with the 
               {py:func}`conversion_function()` decorator
:_special: bool, if True (default False) this task is *NEVER* added automatically
           and has to be added by hand

## Migrating the parsing tasks

These task definitions might have to be adapted for new fleur versions. Some changes
might be possible to make in {py:mod}`~masci_tools.io.parsers.fleur.default_parse_tasks`
directly without breaking backwards compatibility. If this is not possible there is
a decorator {py:func}`register_migration()` to define a function that is recognized
by the {py:func}`outxml_parser()` to convert between versions. A usage example is shown below.

```python
from masci_tools.io.parsers.fleur import register_migration
import copy

@register_migration(base_version='0.33', target_version='0.34')
def migrate_033_to034(definition_dict):
  """
  Fictitious migration from 0.33 to 0.34
  Moves the `number_of_atom_types` attribute from reading a simple
  attribute to counting the number of atomGroups in the input section
  And removes orbital_magnetic_moments task
  """

  #IMPORTANT: First copy the original dict
  new_dict = copy.deepcopy(definition_dict)

  #If a task is incompatible remove it from the defintion_dict
  new_dict.pop('orbital_magnetic_moments')

  new_dict['general_out_info'].pop('number_of_atom_types')
  new_dict['general_inp_info']['number_of_atom_types'] = {
      'parse_type': 'numberNodes',
      'path_spec': {
          'name': 'atomGroup'
      }
  }

  return new_dict
```
