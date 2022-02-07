# Changelog

# v.0.8.0
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.7.2...v0.8.0)

### Added
- Added `FleurInputSchema.xsd` and `FleurOutputSchema.xsd` for the MaX6 release of fleur (file version `0.35`) [[#112]](https://github.com/JuDFTteam/masci-tools/pull/112)
- New XML getter function: `get_special_kpoints` extracts the labelled kpoints from a kpoint list (for now only implemented for Max5 or later)
- Added extraction of Hubbard 1 input and distances in the `outxml_parser` for fleur (distances only available starting from version `0.35`) [[#108]](https://github.com/JuDFTteam/masci-tools/pull/108)
- Added extraction of global vector of magnetic moments in non-collinear calculations in `outxml_parser` under the key `magnetic_vec_moments` starting from version `0.35`

### Improvements
- Fleur schema parsing functions now recognize a new alias from the fleur schemas `FortranComplex` which is a number of the form `(float,float)`. Converters for complex values are added. (Note: Complex numbers should not yet be used in the `outxml_parser`, since AiiDA (<2.0) does not support complex numbers yet) [[#106]](https://github.com/JuDFTteam/masci-tools/pull/106)
- Added `IncompatibleSchemaVersions` error when a combination of output and input version for `OutputSchemaDict` is given, for which it is known that no XML schema can be compiled
- `xml_getters` functions can now be used in the task definitions of the `outxml_parser` to keep information consistent. This example definition will insert the structure data, i.e. a tuple of atoms, bravais matrix and periodic boundary conditions into the output dictionary. `{'parse_type':'xmlGetter', 'name': 'get_structure_data'}` [[#107]](https://github.com/JuDFTteam/masci-tools/pull/107)
- The `_conversions` key in the `outxml_parser` now accepts namedtuples `Conversion` to enable passing additional arguments to these functions. [[#109]](https://github.com/JuDFTteam/masci-tools/pull/109)
- Adjusted `get_cell` to understand the `bravaisMatrixFilm` inut introduced with the MaX6 release of fleur [[#110]](https://github.com/JuDFTteam/masci-tools/pull/110)
- Improved detection, whether a given xpath contains a tag including stripping predicates. Added function `contains_tag` in `masci_tools.util.xml.common_functions` [[#113]](https://github.com/JuDFTteam/masci-tools/pull/113)
- Refactored bokeh plot routine `periodic_table_plot` to make use of the plot parameters utilities [[#114]](https://github.com/JuDFTteam/masci-tools/pull/114)
- `get_parameter_data` now extracts LOs with higher energy derivatives or `HELO` type, as they are supported by the newest versions of the inpgen. The old behaviour of dropping all non `SCLO` and `eDeriv="0"` LOs is available via the option `allow_special_los=False`
### Bugfixes
- Fix in ``load_inpxml`` and ``load_outxml`` (this also effects the ``inpxml/outxml_parser``). Previously file handle like objects not directly subclassing ``io.IOBase`` would lead to an exception
- Added patch for `OutputSchemaDict` objects with `FleurOutputSchema.xsd` files before version `0.35`. The attribute `qPoints` in the DMI output was actually called `qpoints` in these schemas, making it impossible to retrieve this attribute
- Fixed behaviour of relative XPath methods of `SchemaDict` which did not correctly handle root tags, whose names are contained in other tag names, for example `bravaisMatrix` and `bravaisMatrixFilm` from the new file version `0.35`

### Deprecated
- Passing strings in the `_conversions` key in task definitions for the `outxml_parser`. Use `masci_tools.util.parse_utils.Conversion` instead. [[#109]](https://github.com/JuDFTteam/masci-tools/pull/109)
### For developers
- Reorganized visualization tests, making the regeneration of baseline images with `pytest-mpl` easier [[#101]](https://github.com/JuDFTteam/masci-tools/pull/101)
- Switched build system from `setuptools` to `flit`, since this way all the configuration can be specified in the `pyproject.toml` and a lot of duplication of information is avoided (e.g. version numbers) [[#102]](https://github.com/JuDFTteam/masci-tools/pull/102)

# v.0.7.2
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.7.1...v0.7.2)

### Bugfixes
- Fixed regression in ``set_atomgroup_label`` and ``set_species_label``. These functions could be used in previous versions with atom labels, that do not exist. This is not possible in ``v.0.7.1``. Since some parts of the ``aiida-fleur`` plugin relied on this the behaviour has to be kept.

# v.0.7.1
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.7.0...v0.7.1)

### Added
- ``XPathBuilder`` class for specifying complex conditions on xpaths with a dictionary. Added ``filters`` argument to ``schema_dict_util`` and ``xml_setters`` functions for this dictionary [[#96]](https://github.com/JuDFTteam/masci-tools/pull/96)
### Bugfixes
- Fixed issue with ``MANIFEST.in``, where non-python files from the ``tools`` subpackage were not included in the built packages
- Fixed bug not correctly processing the plot limits in ``plot_fleur_bands`` in excluding points outside the plot area for better performance
- Fix for HDF5 transformation ``add_partial_sums`` if not all formatted patterns are present in the dataset, e.g. if a bandstructure/DOS is calculated for only selected atoms
### For developers
- More strict ``mypy`` configuration and moved a lot of the annotations to modern syntax with ``from __future__ import annotations``
- Added ``pyupgrade`` hook to automatically do some easy refactoring, i.e. removing compatibility workarounds move ot modern syntax. Set to apply changes compatible with ``3.7`` and later

## v.0.7.0
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.6.2...v0.7.0)

Commandline interface, refactoring of SchemaDict/XML functions and major improvements for package configuration/tooling for developers. Added support for python ``3.10``. Dropped testing for python ``3.6``.
### Added
- Added click command line interface (available as ``masci-tools``). Can add Fleur XML Schema files with validation (Also directly pulled from the Fleur git), use the XML parsing functions and interface to the fleur visualization routines [[#49]](https://github.com/JuDFTteam/masci-tools/pull/49)
- Added ``Tabulator`` for use of creating ``pandas.Dataframes`` from attributes of python objects. Used in ``aiida-jutools`` to tabulate attributes of aiida nodes
- Added ``optional_tasks`` argument to ``outxml_parser``. Adds tasks marked with ``'_optional': True`` to the performed tasks [[#81]](https://github.com/JuDFTteam/masci-tools/pull/81)
- Added visualization routine for spectral functions (colormesh plot with path though Brillouin zone)
- Added tool for converting ``inp.xml`` files between different file versions (Available through the click CLI ``masci-tools inpxml``) [[#88]](https://github.com/JuDFTteam/masci-tools/pull/88)
- Added three new XML setters: ``clone_species`` (Create and modify a species starting from an existing one), ``switch_species``/``switch_species_label`` for switching the species attribute of atom groups with additional checks
- ``outxml_parser``: Total Energy is now taken from the output ``freeEnergy`` in the ``out.xml``
### Improvements
- Refactored SchemaDict code. Moved routines ``get_tag_xpath`` and similar to methods on the SchemaDict. If the path cannot be determined custom exceptions ``NoPathFound`` and ``NoUniquePathFound`` are now raised [[#84]](https://github.com/JuDFTteam/masci-tools/pull/84)
- Added utility to ``OutputSchemaDict`` to create absolute paths into ``iteration`` elements in ``out.xml``. Added support for this option in ``schema_dict_util`` functions with ``iteration_path=True``
- All basic XML modification functions now accept either a ``ElementTree`` or ``Element``. and warn they find no nodes to operate on
- Improved capabilities of green's function tool, can now be used with radially resolved/k-resolved Green's functions
- Improved performance of Fleur XML Schema parsing by switching from the ``xpath`` method on the ``ElementTree`` to constructing a ``XPathEvaluator`` object [[#89]](https://github.com/JuDFTteam/masci-tools/pull/89)
- All ``xml_getters`` functions can now also be used with ``out.xml`` files
- ``set_atomgroup``/``set_atomgroup_label`` now use ``switch_species`` if the species attribute is changed
- ``set_atomgroup`` now supports the ``all-<search string>`` syntax for species argument, equivalent to ``set_species``
- Improved behaviour of spin-polarized DOS plots for duplicating all plot parameters for spin-down components (previously only color was repeated)
### Bugfixes
- Fixed several issues in version handling of Schema dictionaries. It is now possible to add a new schema and have it work (with warnings) without needing to change any code (``masci-tools fleur-schema add <path/to/schema>``)
- Bugfix in ``evaluate_tag`` not handling the combination of options ``subtags=True`` and ``text=True`` correctly. Previously some results were overwritten.
- Fixed accidental change in ``write_inpgen_file`` in comparison to old ``aiida-fleur`` implementation. Now the species name is always appended to the position in the inpgen file if it is not equal to the atom symbol
- Fixed behaviour of ``get_parameter_data`` for inputs with local orbitals with higher energy derivatives. These cannot be created by the inpgen and so are dropped
- Fixes in ``xml_setters`` to allow consistent creation of multiple tags for setting text or attributes
### Deprecated
- The ``fleur_schema`` subpackage was moved from ``masci_tools.io.parsers.fleur`` to ``masci_tools.io.parsers`` to avoid circular import issues [[#87]](https://github.com/JuDFTteam/masci-tools/pull/87)
### Removed
- ``get_structure_data`` now returns ``AtomSiteProperties`` for the atom information by default. The default value of ``site_namedtuple`` is now ``True``
### For developers
- Moved configuration of ``yapf``, ``pylint`` and ``pytest`` into ``pyproject.toml``
- Made test suite executable from the root-folder (Some file paths were not transferrable when changing the execution directory)
- Added ``test_file`` fixture, which constructs the absolute filepath to files in the ``tests/files`` folder to reduce the difficulty of moving test files around and reorganizing the pytest suite
- Updated pylint (``2.11``), pytest (``6.0``) in ``setup.py``
- Added ``mypy`` pre-commit hook. Checked files are specified explicitely [[#86]](https://github.com/JuDFTteam/masci-tools/pull/86).
- Added typing to majority of XML functions (with stubs package ``lxml-stubs``) and large parts of the ``io`` and ``util`` subpackages
- Dropped testing for python ``3.6`` in CI

## v.0.6.2
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.6.1...v0.6.2)

Small bugfixes and refactoring for plotting routines
### Added
- Common plot routines for equation of states `eos_plot` and plotting scf convergence `convergence_plot`
- Replaced old convergence plot routines with single routines for bokeh/matplotlib named `plot_convergence`
### Improvements
- Moved eos and convergence plots to use `PlotData` class
- Fixed some edge cases of bokeh testing fixtures. Previously some plots would crash the code for normalizing the json
### Bugfixes
- Fixed bugs in convergence routines for using them in aiida-fleur

## v.0.6.1
Release fixing a small issue with publishing version `0.6.0` to zenodo
## v.0.6.0

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.5.0...v0.6.0)

This release contains major improvements to plotting methods and new tools. Also the fleur parsing functions were improved

### Added
- `PlotData` class for handling data passed to plotting methods very flexibly [[#54]](https://github.com/JuDFTteam/masci-tools/pull/54) (For more information see the relevant [users guide](https://masci-tools.readthedocs.io/en/latest/user_guide/plotting.html#providing-data) or [developers guide](https://masci-tools.readthedocs.io/en/latest/devel_guide/plot_data.html) sections in the documentation)
- `masci_tools.vis.common` module for plotting methods with common interfaces for bokeh/matplotlib [[#71]](https://github.com/JuDFTteam/masci-tools/pull/71)
- `get_parameter_data` also extracts kpt mesh specifications for the input generator
- Exposed and improved bokeh testing fixtures in `masci_tools.testing.bokeh` for use in higher level packages
- `greensf_calculations` module in `tools` with sample functions for calculating properties with green's functions from fleur
- Added two options `line_plot` and `separate_bands` to bandstructure plots. While `line_plot` is obvious (no weighted bandstructures possible), `separate_bands` allows to set parameters for single selected bands. These options can also be combined

### Improvements
- Added option `only_used` to `get_kpoints_data` to get only the `kPointList` referenced in the `kPointListSelection` tag
- Made `constants` argument to `schema_dict_util` functions completely optional. Will raise an exception if a undefined constant is encountered
- Bandstructure plots now exclude points outside the plotting area to speed up these plots significantly for systems with a large number of bands
- Refactored attribute/text type definitions in `SchemaDict` objects. Now unified under one structure. Both attributes and texts can now be recognized to contain multiple values [[#64]](https://github.com/JuDFTteam/masci-tools/pull/64)
- Added `spin_arrows` option to toggle spin arrows in `plot_spinpol_dos` for matplotlib. Previously this was only possible for bokeh
- Added options to create different types of bar plots to `barchart`: Available are `'stacked'` (default), `'grouped'`, `'independent'` (positions can be defined for each data set)
- Exceptions occuring in `transforms` for `HDF5Reader` are now bundled into `HDF5TransformationError` to allow easier error handling
- Added MT keys to `kkrparams`

### Bugfixes
- Fix for `write_inpgen_file`, which was incorrectly inserting the `'X'` (empty sphere) element into inpgen files
- Fix for `read_inpgen_file`, which could not handle inpgen files with comments on certain lines in the inpgen file
- Several fixes for `plot_fleur_dos` not using the standard DOS calculation but orbital decompositions and so on
- Adjusted default `dpi` for matplotlib to `100` to avoid problems with size when using `plt.show()` instead of saving

## v.0.5.0

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.10...v0.5.0)

This release contains fleur inpgen IO capabilities and many major improvements

### Added
- IO routines for reading/writing inpgen input files
- `get_structure_data` now returns the relaxed structure if a `relaxation` section is present
- `get_parameter_data` can read in the electron configuration if requested
- `get_symmetry_information` xml getter to get all defined symmetry operations
- `get_structure_data` and `get_parameter_data` now norm the species names to get consistent ids for usage in the inpgen files [[#70]](https://github.com/JuDFTteam/masci-tools/pull/70)
### Improvements
- Added another possible value to environment variable `MASCI_TOOLS_USE_OLD_CONSTANTS` to get the values of constants in between commits c171563 and 66953f8 [[#66]](https://github.com/JuDFTteam/masci-tools/pull/66)
- `spex` attribute is now used in addition to old `gw` attribute to determine whether a fleur input file is from a SPEX calculation
- `evaluate_tag` can now also get the text and recursively parse all subtags
- Changed default of `multiply_by_eqiv_atoms` in `plot_fleur_dos` to `True`
- `barchart` can now make horizontal bar charts
- `get_cell` now also takes the `scale` attribute into account
- Made conversion to angstroem optional (done by default) in the xml getters. Can be turned off with the options `convert_to/from_angstroem`
- Deprecated: Old atom position output in `get_structure_data`. Use option `site_namedtuple=True` to get new output (includes species information)
### Bugfixes
- Fixes to make `plot_convex_hull_2d` work
- Fix in `evaluate_text` make `constants` argument optional
- Fix for `get_structure_data`; Added missing unit conversion for z-coordinate of film positions

## v.0.4.10

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.9...v0.4.10)

This release contains bugifxes for the visualization routines 

### Bugfixes
- Fixed issue for histogram plot, which prevented usage for e.g. stacked histograms with multiple datasets
- Fixed usage of dictionary arguments in plot_fleur_dos, that should not be used to specify parameters for multiple datasets (e.g. limits, lines)
- Updated documentation table of plot parameters to put all dictionaries into literal blocks. Otherwise single quotes appear differently on read the docs

## v.0.4.9

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.8...v0.4.9)

### Improvements
- Added saving/loading of plot defaults in json files to Plotter class (No exposed functions yet in plot_methods or bokeh_plots)
- DOS plot parameters in plot_fleur_dos can now be specifified by label, e.g. color={'Total_up': 'blue'}
### Bugfixes
- Various Bugfixes and improvements to ChemicalElements class, greensfunction tools and plotting methods
- Fixed wrong atom label generation in DOS plots (#55)

## v.0.4.8

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.7...v0.4.8)

### Added
- Tool to analyze/work with greensfunctions calculated by Fleur `masci_tools.tools.greensfunction`
### Improvements
- Several improvements of KKR parsers/parameters [[#13]](https://github.com/JuDFTteam/masci-tools/pull/13)
- Introduced patching functions for the schema dictionaries to manually correct ambiguities (#48)
- Improvements of the `HDF5Reader` and  recipes for Fleur DOS/bandstructure calculation
- For devs:
   - pylint warnings are no longer fatal for the CI jobs
   - tests folder moved outside package directory
### Bugfixes
- Bugfixes and improvements in the plotting functions for DOS/bandstructures
- Bugfixes in `xml_setters` and `fleurxmlmodifier` modules

## v.0.4.7

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.6...v0.4.7)

### Added
- Introduced higher level XML modification functions for `xml_delete_tag`, `xml_delete_att`, `xml_replace_tag`
### Improvements
- moving conversion factors for energy and bohr to angstroem conversion to NIST values in KKR parts of the code. This can also be disabled for backwards compatibility by setting the environment flag `MASCI_TOOLS_USE_OLD_CONSTANTS`
- Added missing energy unit alias for  Fleur input files
- `xml_delete_tag`, `xml_delete_att`, `xml_replace_tag` now also support the `occurrences` argument
- FleurXMLModifier improvements. Modification registration methods will now test the given arguments against the modifying functions immediately to fail early for errors. `fromList` classmethod allows the instantiation with a known list of tasks to perform. These are passed through the same procedure as the normal registration of changes

## v.0.4.6

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.5...v0.4.6)

### Bugfixes
- Fix for the `clear_xml` function, where comments could end up in the set of included tags. This lead to failures in aiida-fleur

## v.0.4.5

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.4...v0.4.5)

### Added
- Introduced function to split a xmltree back up into the included subtrees and the main tree with `xi:include` tags
- clear_xml now returns a set of the tags, that were included
### Bugfixes
- various bugfixes for xml modifying functions
- A special case for `theta`, `phi` and `ef_shift` attributes of forceTheorem tags, since they are not correctly typed in the Inputschema

## v.0.4.4

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.3...v0.4.4)

### Added
- XML getter methods for number of kpoints and relaxation information
- XML setter methods for manipulating kpoints
### Improvements
- top level `create_tag` now also accepts a etree.Element
- XML getters now also accept etree.Element
- Added `etree.indent` calls to keep modified `inp.xml` clean (raises lxml dependency constraint to 4.5)
- `io_fleurxml` functions now pass keyword arguments to XMLParser
- Readd `fleur_modes` to output_dict
### Bugfixes
- Bugfix for relative xpaths

## v.0.4.3

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.2...v0.4.3)

### Added
- Added utility for creating schema dictionary version specific functions
- Added XML getter functions adapted from aiida-fleur fleurinpdata methods [[#40]](https://github.com/JuDFTteam/masci-tools/pull/40)
### Improvements
- Improved logging and failure handling of XML parser functions [[#39]](https://github.com/JuDFTteam/masci-tools/pull/39)
- Improved handling of `schema_dict_util` functions with nodes away from the XML root of the file [[#41]](https://github.com/JuDFTteam/masci-tools/pull/41)

## v.0.4.2

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.1...v0.4.2)

### Added
- Added key descriptions to Plotter objects and ``get_mpl_help`` and ``get_bokeh_help`` functions in plotting modules for getting descriptions of parameters
- Two new recipes for ``HDF5Reader`` for bandstructures (for reading in no or specific weights besides eigenvalues)
### Improvements
- MatplotlibPlotter and BokehPlotter now have a autogenerated table of descriptions and default values in the docstring (not as nicely formatted) and in the sphinx build (really nicely formatted)
- ``save_format`` in matplotlib plots can now be a list of formats
- Various visual improvements to band/DOS plots:
   - Bandstructure size scaling adjusted to not produce massive bands
   - Bandstrcuture spin up components are now potted on top by default
   - size/color scaling now done with respect to the maximum in the plotting region
   - DOS added spin arrows in spin-polarized case
   - DOS inverted x-axis in vertical plot (spin down now on the right side)
   - DOS added symmetric limits in DOS direction for spin-polarized plots
   - DOS default figsize flipped for vertical plots

## v.0.4.1

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.4.0...v0.4.1)

### Bugfixes
- Fix for `plot_lattice_constant` to make it work in aiida-fleur

## v.0.4.0

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.3.12...v0.4.0)

### Added
- Parsers for Fleur `inp.xml`/`out.xml` files. These are robust with respect to changing file versions [[#3]](https://github.com/JuDFTteam/masci-tools/pull/3)
- General parser for `.hdf` files [[#30]](https://github.com/JuDFTteam/masci-tools/pull/30)
- Functionality for modifying `inp.xml` files [[#23]](https://github.com/JuDFTteam/masci-tools/pull/23)
- Fleur visualization routines `plot_fleur_dos` and `plot_fleur_bands`
- IO Module for creating/reading and manipulating `n_mmp_mat` files for LDA+U calculations in fleur [[#31]](https://github.com/JuDFTteam/masci-tools/pull/31)
- Tool for calculating crystal field coefficients [[#22]](https://github.com/JuDFTteam/masci-tools/pull/22)
### Improvements
- Refactored parameter handling in plotting methods. Introduced
`Plotter` class for consistent behaviour and easy extendability of plotting capabilities [[#6]](https://github.com/JuDFTteam/masci-tools/pull/6)
