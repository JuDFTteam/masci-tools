# Changelog

## latest
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.13.0...develop)

Nothing here yet

## v.0.13.0
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.12.0...v0.13.0)

### Improvements
- `set_kpointmesh` now also writes out the `nx/ny/nz` attributes fro the dimensions of the kpoint mesh
- `get_structure_data`, `get_parameter_data` and `get_kpoints_data` are renamed to `get_structuredata`, `get_parameterdata` and `get_kpointsdata` to match the names of the corresponding functions in aiida-fleur. Old names are available with deprecations [[#208]](https://github.com/JuDFTteam/masci-tools/pull/208)
- `FleurXMLModifier` now supports changes to input files with not yet available Fleur schemas, if the changes are compatible with the last available file schema [[#209]](https://github.com/JuDFTteam/masci-tools/pull/209)
### Bugfixes
- Bugfix in XML setters `set_inpchanges` and `set_attrib_value`, setting the `xcFunctional` key was previously not case-insensitive in constrast with all other keys
- Fixed crash in `get_parameter_data`. This function would previously crash if a kpoint mesh without `nx/ny/nz` attributes was used and the first point in the list was the gamma point

## v.0.12.0
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.11.3...v0.12.0)

### Added
- Added XPath evaluation functions with runtime tpye checking of the results of the expressions [[#181]](https://github.com/JuDFTteam/masci-tools/pull/181)
- Command `masci-tools fleur-schema pull <branch>` to update/add Fleur Schema files from the iffgit more easily [[#184]](https://github.com/JuDFTteam/masci-tools/pull/184)
- New XML setters [[#183]](https://github.com/JuDFTteam/masci-tools/pull/183):
  - Setting XC functional explicitly + LibXC support (`set_xcfunctional`),
  - Creating a kpoint path using `ase` (`set_kpointpath`)
  - Creating a kpoint mesh with symmetry reduction using `spglib`. Should be equivalent to the `gamma@grid=nx,ny,nz` kpoint generator in `inpgen` (`set_kpointmesh`)
- Added `FleurInputSchema.xsd` and `FleurOutputSchema.xsd` for the MaX6.1 release of fleur (file version `0.36`) [[#196]](https://github.com/JuDFTteam/masci-tools/pull/196)

### Bugfixes
- Add clearer error message if `None` is passed to the `convert_to_xml` functions. This would happen for example using the `set_inpchanges` function with `{'minDistance': None}` [[#182]](https://github.com/JuDFTteam/masci-tools/pull/182)
- Fixed `masci-tools fleur-schema add` with `--from-git` flag. Previously it would still check for the existence of the Schema file locally [[#184]](https://github.com/JuDFTteam/masci-tools/pull/184)
- `get_fleur_modes`: `gw` mode renamed to `spex` and now stores the actual integer value of the attribute [[#185]](https://github.com/JuDFTteam/masci-tools/pull/185)
- Bugfix in `clear_xml`, when multiple XML comments are present outside the root element [[#193]](https://github.com/JuDFTteam/masci-tools/pull/193)
- Bugfix in `reverse_xinclude`. This would previously break when reexcluding trees already containing a `relaxation` tag and would end up with two `xi:include` tags for the `relax.xml` [[#194]](https://github.com/JuDFTteam/masci-tools/pull/194)
- Bugfix for `FleurXMLModifier`. The `task_list` property would incorrectly enter a `kwargs` key if the modifying function in question has an explicit `**kwargs` argument
- Bugfix in matplotlib plots with placement of multiple colorbars (e.g. weighted spin-polarized bandstructure) [[#198]](https://github.com/JuDFTteam/masci-tools/pull/198)


## v.0.11.3
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.11.2...v0.11.3)

### Improvements
- Changes to KKR plotting routine `dispersionplot` for compatibility with AiiDA v2.0
- Connecting vectors for intersite `GreensFunction` are now saved in Angstroem. For better interoperability with ase, pymatgen, AiiDA

### For Developers
- Relaxed CI requirements for docs build. Nitpicky mode is no longer required to pass but is treated as a hint to look into the warnings

## v.0.11.2
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.11.1...v0.11.2)

### Improvements
- Several changes in KKR IO functions to make them compatible with `aiida-core>=2.0` [[#175]](https://github.com/JuDFTteam/masci-tools/pull/175)
- Add function to calculate fourier transform of e.g. `J_ij` constants calculated from Green's functions (`masci_tools.tools.greensf_calculations.heisenberg_reciprocal`)

### Bugfixes
- Fixed nondeterministic order in bokeh regression tests if multiple dictionaries with the same values but differing keys in the same list (e.g. Providing the same data for different columns)
- Fixed wrong names for columns entered in `decompose_jij_tensor`, i.e. `J_ji` -> `J_ij`

### Deprecations
- Deprecated the unused modules `util/kkr_rms_tracker.py` and `util/modify_potential.py`

## v.0.11.1

[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.11.0...v0.11.1)

### Bugfixes
- Bugfix in `reverse_xinclude`. Version `0.11.0` broke this function for versions, where the `relaxation` tag was not allowed.

## v.0.11.0
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.10.1...v0.11.0)

This release adds some improvements to the XML and HDF5 handling mainly for better AiiDA-Fleur
support. Also major updates to documentation configurations and Green's function calculations.

### Added
- Added `FleurElementMaker` class. This can be used to create XML elements compatible with a given version from scratch.
  Has case-insensitivity and converts values to strings for XML [[#159]](https://github.com/JuDFTteam/masci-tools/pull/159)
  Example
  ```python
   from masci_tools.util.xml.builder import FleurElementMaker
   E = FleurElementMaker.fromVersion('0.35')
   new_kpointset = E.kpointlist(
       *(
           E.kpoint(kpoint, weight=weight, label=special_labels[indx]) if indx in special_labels else
           E.kpoint(kpoint, weight=weight) for indx, (kpoint, weight) in enumerate(zip(kpoints, weights))
       ),
       name=name,
       count=nkpts,
       type=kpoint_type)
  ```
- Function `serialize_xml_arguments` to `masci_tools.util.xml.common_functions` to remove XML elements/trees from positional/keyword arguments and replace them with string representations of the XML. Can be used in AiiDA-Fleur
- Module `masci_tools.util.ipython` and ipython extension (`%load_ext masci_tools`). Adds syntax highlighted XML tree output and creating HTML syntax highlighted diffs of XML trees [[#158]](https://github.com/JuDFTteam/masci-tools/pull/158)
- Added calculation of Jij Tensor from intersite Green's functions [[#170]](https://github.com/JuDFTteam/masci-tools/pull/170)

### Improvements
- Added `name` entry to `SchemaDict.tag_info` which contains the tag name in the original case [[#159]](https://github.com/JuDFTteam/masci-tools/pull/159)
- `convert_to_xml` is made more strict. Conversion `int` to `str` uses the `{:d}` format specifier and string conversion is no longer always attempted [[#159]](https://github.com/JuDFTteam/masci-tools/pull/159)
- Improvements to Colorbar creation in matplotlib plotting methods. Limits are now set consistently with `limits={'color': (low, high)}` in the plot and colorbar. Spinpolarized bandplots now show two colorbars for the two colormaps if requested
- `get_parameter_data` now also extracts the `gamma` switch for kpoint generation for more consistent roundtrips. This is only set if the first kpoint in the mesh is the gamma point and there are multiple
- `load_inpxml` and `load_outxml` now consistently accept the XML file given as a
string of the content. The content no longer has to be manually encoded as bytes
- The method `FleurXMLModifier.modify_xmlfile` now always returns two things. The modified XML tree and a dictionary with all additional file contents, e.g. `n_mmp_mat`.
- Support for aligning spin/real-space frames of Green's functions. Several further imporvements/bugfixes for Green's function modules [[#170]](https://github.com/JuDFTteam/masci-tools/pull/170)

### Bugfixes
- Bugfix for `outxml_parser` returning a nested list for Hubbard 1 distances, where a flat list was expected. Removed `force_list` argument from the parsing task definition
- Fixes in `plot_fleur_bands`, when providing custom weights without spin suffixes, i.e. `_up`/`_down`
- Fix in `HDF5Reader`. IO like objects without an attached filename would lead to an  early error. This is the case for example for some readers in the file repository implementation used in AiiDA v2.0
- Fix in `HDF5Reader`. The file handles for compressed files in the AiiDA v2 repository have to be copied into a temporary file first before they can be used

### For Developers
- Docs: Updated `sphinx` and `sphinx-autodoc-typehints` versions and build docs on python 3.10 [[#156]](https://github.com/JuDFTteam/masci-tools/pull/156)
- Docs: Converted to `MyST` markdown and where appropriate introduced `myst-nb` for executing code cells in the documentation, e.g. generate plotting examples [[#157]](https://github.com/JuDFTteam/masci-tools/pull/157)
- Bokeh regression tests now strip out the bokeh version from the test files
- Added pre-commit hook, which generates the docstrings for the `FleurXMLModifier` registration methods from their XML setter function counterparts [[#166]](https://github.com/JuDFTteam/masci-tools/pull/166)

## v0.10.1
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.10.0...v0.10.1)

### Bugfixes
- Remove accidentally left in debug print in `outxml_parser`

## v.0.10.0
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.9.1...v0.10.0)

This release provides several new features in the XML modification/evaluation for Fleur XML files and bugfixes. Multiple problems when
working with DFT+U density matrix files are also fixed.
### Added
- New XML setter `align_nmmpmat_to_sqa` to rotate the density matrix file according to SQAs specified either for noco or second variation SOC [[#140]](https://github.com/JuDFTteam/masci-tools/pull/140)
- Added `task_list` property to `FleurXMLModifier` to construct a list which can be used to replicate the same `FleurXMLModifier` with the `fromList()` classmethod [[#149]](https://github.com/JuDFTteam/masci-tools/pull/149)
- Added `FleurXMLContext`, which acts as a holder of th XML elements,  schema dictionary, constants and logger to reduce the amount of information/clutter in functions evaluating things from the XML file [[#152]](https://github.com/JuDFTteam/masci-tools/pull/152)

  Note: The class `ParseTasks` used in the `outxml_parser` was simplified and placed into the `outxml_parser` module and the decorator `register_parsing_function` was removed. This was done without deprecation since they were exclusively used in the `outxml_parser` and were the main cause of cyclic import problems previously
- Added several predefined conversions to/from input version `0.35` to `inpxml_converter` [[#153]](https://github.com/JuDFTteam/masci-tools/pull/153)

### Improvements
- Added `inverse` argument to nmmpmat XML setters. These will correctly produce the inverse rotation operation for the given angles. Also allow setting `orbital='all'` in `rotate_nmmpmat` to rotate all blocks by the given angles [[#140]](https://github.com/JuDFTteam/masci-tools/pull/140)
- The XML setters `create_tag`, `replace_tag` and their low-level equivalents now also accept XML strings, i.e. `<example attribute="1"/>`, as arguments for the elements to create/replace [[#145]](https://github.com/JuDFTteam/masci-tools/pull/145)
### Bugfixes
- Fix for XML setters operating on the DFT+U density matrix file. Previously these functions would not map the density matrix blocks correctly if multiple atomgroups shared the same species containing `ldaU` tags [[#140]](https://github.com/JuDFTteam/masci-tools/pull/140)
- Added missing prefactor `(-1)^(m-mp)` to `get_wigner_matrix()`
- Added basic tests of `masci_tools.tools.greensfunction` module and fixed several bugs found due to this [[#150]](https://github.com/JuDFTteam/masci-tools/pull/150)
- Fixed bug in XML setters operating on the DFT+U density matrix file not correctly extracting the number of spin blocks when only setting `l_mperp`
- Fixed bug, when using the `FleurXMLModifier` directly (not in `aiida-fleur`), included XML files were not handled
- Fixed bug in `outxml_parser`, when the XML file had to be repaired and more than one iteration was present the wrong iteration was chosen as the last stable iteration [[#152]](https://github.com/JuDFTteam/masci-tools/pull/152)

### Deprecated
- The module `masci_tools.io.io_fleurxml` is renamed to `masci_tools.io.fleur_xml` [[#152]](https://github.com/JuDFTteam/masci-tools/pull/152)
- The module `masci_tools.util.parse_task_decorator` is removed. All decorators are now availaibe under `masci_tools.io.parsers.fleur` [[#152]](https://github.com/JuDFTteam/masci-tools/pull/152)

### For Developers
- Added `py.typed` marker to masci-tools, since a large part of the outside facing code (especially the XML APIs are typed). With this marker other packages can use the typehints in this package

## v.0.9.1
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.9.0...v0.9.1)

### Added
- Standalone function `masci_tools.tools.fleur_inpxml_converter.convert_inpxml` to allow conversions of `inp.xml` files within a python runtime without needing to go via the commandline

### Bugfixes
- Fixed bug in bokeh testing fixtures using the wrong folder for fallback versions
- Fixed bug not correctly converting complex numbers from the Fleur xml files if they have whitespace at beginning/end

## v.0.9.0
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.8.0...v0.9.0)

### Added
- New `bokeh` plot routine for matrix plot of rectangle patches with added texts [[#124]](https://github.com/JuDFTteam/masci-tools/pull/124)
- Added TS contribution to free energy to output of `outxml_parser`

### Improvements
- Several arguments in XML setter functions were renamed for more consistent signatures.
  The main changes are 
   - `attributedict`/`change_dict` -> `changes`
   - `attributename`/`attribv` -> `name`/`value`
   - `add_number` -> `number_to_add`
  
  The old signatures are still supported with deprecations if called via the `FleurXMLModifier` [[#118]](https://github.com/JuDFTteam/masci-tools/pull/118)
- Remove constraint on `bokeh` version (previously `<=1.4.0`) [[#122]](https://github.com/JuDFTteam/masci-tools/pull/122)
- Add `only_spin` option and calculate complete non-spinpolarized DOS for `spinpol=False` in `plot_fleur_dos` [[#125]](https://github.com/JuDFTteam/masci-tools/pull/125)
- Refactored `CFCalculation`, i.e. naming of attributes handling of cutoffs. Added classmethod to construct instance directly from numpy arrays [[#127]](https://github.com/JuDFTteam/masci-tools/pull/127)
- Refactored plotting methods for `CFCalculation` to allow the same parameter freedom as for the other matplolib routines [[#127]](https://github.com/JuDFTteam/masci-tools/pull/127)
- Improvement to labels and legends in DOS/bandstructure plots. Matplotlib plots now put the legend centered below the plot and added latex labels to axis and ticks in bokeh (version `2.4.0` needed) [[#133]](https://github.com/JuDFTteam/masci-tools/pull/133)
- `io_nmmpmat`: Allow negative indices in `read_nmmpmat_block` and raise error for invalid index
### Bugfixes
- Fix for signatures of `set_text`/`set_first_text`. These contained names of attribute setting functions [[#118]](https://github.com/JuDFTteam/masci-tools/pull/118)
- Fix for validating arguments in `FleurXMLModifier` not accepting an argument named `name` when passed by keyword. [[#118]](https://github.com/JuDFTteam/masci-tools/pull/118)
- Fixed problems in `masci_tools.testing.bokeh` when adding files for new bokeh versions [[#122]](https://github.com/JuDFTteam/masci-tools/pull/122)
- Several fixes for `plot_fleur_dos`. Using the `area_plot` or specifying `color` explicitly could mess up the color order [[#132]](https://github.com/JuDFTteam/masci-tools/pull/132)
- Fixed bug in `validate_nmmpmat` and consequently `FleurXMLModifier` not correctly validating denisty matrix files with certain off-diagonal elements being negative [[#135]](https://github.com/JuDFTteam/masci-tools/pull/135)
- Fix for `HDF5Reader` for compatibility for file handles in `aiida-core` 2.0. The file handles coming from the file repository have no directly attached extension so the check if the file is a hdf file cannot be performed

### For developers
- Fixed upload of pytest-mpl results artifacts to include the whole directory with images and not just the HTML file [[#117]](https://github.com/JuDFTteam/masci-tools/pull/117)
- Updated typing to newer version of `lxml-stubs` (`0.4.0`) [[#123]](https://github.com/JuDFTteam/masci-tools/pull/123)

## v.0.8.0
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
- Adjusted `get_cell` to understand the `bravaisMatrixFilm` input introduced with the MaX6 release of fleur [[#110]](https://github.com/JuDFTteam/masci-tools/pull/110)
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

## v.0.7.2
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.7.1...v0.7.2)

### Bugfixes
- Fixed regression in ``set_atomgroup_label`` and ``set_species_label``. These functions could be used in previous versions with atom labels, that do not exist. This is not possible in ``v.0.7.1``. Since some parts of the ``aiida-fleur`` plugin relied on this the behaviour has to be kept.

## v.0.7.1
[full changelog](https://github.com/JuDFTteam/masci-tools/compare/v0.7.0...v0.7.1)

### Added
- ``XPathBuilder`` class for specifying complex conditions on xpaths with a dictionary. Added ``filters`` argument to ``schema_dict_util`` and ``xml_setters`` functions for this dictionary [[#96]](https://github.com/JuDFTteam/masci-tools/pull/96)
### Bugfixes
- Fixed issue with ``MANIFEST.in``, where non-python files from the ``tools`` subpackage were not included in the built packages
- Fixed bug not correctly processing the plot limits in ``plot_fleur_bands`` in excluding points outside the plot area for better performance
- Fix for HDF5 transformation ``add_partial_sums`` if not all formatted patterns are present in the dataset, e.g. if a bandstructure/DOS is calculated for only selected atoms
### For developers
- More strict ``mypy`` configuration and moved a lot of the annotations to modern syntax with ``from __future__ import annotations``
- Added ``pyupgrade`` hook to automatically do some easy refactoring, i.e. removing compatibility workarounds move to modern syntax. Set to apply changes compatible with ``3.7`` and later

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
- Added ``mypy`` pre-commit hook. Checked files are specified explicitly [[#86]](https://github.com/JuDFTteam/masci-tools/pull/86).
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
- Exceptions occurring in `transforms` for `HDF5Reader` are now bundled into `HDF5TransformationError` to allow easier error handling
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
- Introduced patching functions for the schema dictionaries to manually correct ambiguities [[#48]](https://github.com/JuDFTteam/masci-tools/pull/48)
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
- Re-add `fleur_modes` to output_dict
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
