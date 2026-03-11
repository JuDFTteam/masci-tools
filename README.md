[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)
[![GitHub version](https://img.shields.io/github/v/tag/JuDFTTeam/masci-tools?include_prereleases&label=GitHub%20version&logo=GitHub)](https://github.com/JuDFTteam/masci-tools/releases)
[![PyPI version](https://img.shields.io/pypi/v/masci-tools)](https://pypi.org/project/masci-tools/)
[![PyPI pyversion](https://img.shields.io/pypi/pyversions/masci-tools)](https://pypi.org/project/masci-tools/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/masci-tools.svg)](https://anaconda.org/conda-forge/masci-tools)
[![Build status](https://github.com/JuDFTteam/masci-tools/workflows/masci-tools/badge.svg?branch=develop&event=push)](https://github.com/JuDFTteam/masci-tools/actions)
[![Coverage Status](https://codecov.io/gh/JuDFTteam/masci-tools/branch/develop/graph/badge.svg)](https://codecov.io/gh/JuDFTteam/masci-tools)
[![Documentation Status](https://readthedocs.org/projects/masci-tools/badge/?version=latest)](https://masci-tools.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5223353.svg)](https://doi.org/10.5281/zenodo.5223353)





# masci-tools

Masci-tools (short for "materials science tools") is a post-processing toolkit for electronic structure calculations. Its well-documented Python interface simplifies I/O parsing, visualization such as bandstructure and DOS plotting, and data analysis.

Feel free to contribute.

The code is hosted on GitHub at
<https://github.com/JuDFTteam/masci-tools>

The documentation is hosted on https://masci-tools.readthedocs.io.

Most functionality was developed for the use with the DFT codes developed at the Forschungszentrum Jülich (<http://judft.de>) and their AiiDA plugins for high-throughput calculations ([aiida-fleur](https://github.com/JuDFTteam/aiida-fleur), [aiida-kkr](https://github.com/JuDFTteam/aiida-kkr), [aiida-spirit](https://github.com/JuDFTteam/aiida-spirit)).

## Installation

```
pip install masci-tools
```

## Dependencies

These python packages are needed:
* `lxml`
* `h5py`
* `deepdiff`
* `humanfriendly`  
* `matplotlib`
* `seaborn`
* `ase`
* `pymatgen`
* `mendeleev`
* `click`
* `click-completion`
* `PyYAML`
* `tabulate`

It should not depend on `aiida-core`!

## Layout of `masci-tools`

* `io`
    * Contains methods to write certain files
    * `io.parsers`: Contains parsers of certain code output or input files
* `testing`
    * Contains utilities/fixtures for testing that can be useful outside the package
* `util`
    * Contains rather low-level utility
* `tools`
    * Contains rather high-level utility which is rather complete
* `vis`
    * Contains a collection of matplotlib/bokeh methods used for plotting common results from material science simulations, e.g. bandstructures, DOS, ... 
* `cmdline`
    * Contains a small click command line interface exposing some parts of the library

## License


*masci-tools* is distributed under the terms and conditions of the MIT license which is specified in the `LICENSE.txt` file.
