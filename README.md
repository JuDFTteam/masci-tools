[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)
[![GitHub version](https://img.shields.io/github/v/tag/JuDFTTeam/masci-tools?include_prereleases&label=GitHub%20version&logo=GitHub)](https://github.com/JuDFTteam/masci-tools/releases)
[![PyPI version](https://img.shields.io/pypi/v/masci-tools)](https://pypi.org/project/masci-tools/)
[![PyPI pyversion](https://img.shields.io/pypi/pyversions/masci-tools)](https://pypi.org/project/masci-tools/)
[![Build status](https://github.com/JuDFTteam/masci-tools/workflows/masci-tools/badge.svg?branch=develop&event=push)](https://github.com/JuDFTteam/masci-tools/actions)
[![Coverage Status](https://codecov.io/gh/JuDFTteam/masci-tools/branch/develop/graph/badge.svg)](https://codecov.io/gh/JuDFTteam/masci-tools)
[![Documentation Status](https://readthedocs.org/projects/masci-tools/badge/?version=latest)](https://masci-tools.readthedocs.io/en/latest/?badge=latest)




# masci-tools

**This is a collection of tools, common things used by packages of material science.**

Feel free to contribute.

The code is hosted on GitHub at
<https://github.com/JuDFTteam/masci-tools>

The documentation is hosted on https://masci-tools.readthedocs.io.

Most functionality was developed for the use with the DFT codes developed at the Forschungszentrum Jülich (see <http://judft.de>, <https://flapw.de> and <https://jukkr.fz-juelich.de> for further information on the codes) and in the context of the AiiDA plugins for the [Fleur code](https://github.com/JuDFTteam/aiida-fleur) and the [KKR code](https://github.com/JuDFTteam/aiida-kkr).

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

It should not depend on `aiida-core`!

## Layout of`masci-tools`

* `io`
    * Contains methods to write certain files
    * `io.parsers`: Contains parsers of certain code output or input files
* `tests`
    * auto tests of `masci-tools` functions
* `util`
    * Contains rather low level utility
* `tools`
    * Contains rather highlevel utility which is rather complete
* `vis`
    * Contain a collection of matplotlib, pyplot, gnuplot methods used for ploting common results from material science simulations, e.g. bandsstructures, DOS, ... 

## License


*masci-tools* is distributed under the terms and conditions of the MIT license which is specified in the `LICENSE.txt` file.
