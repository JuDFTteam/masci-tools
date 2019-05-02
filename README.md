[![Build Status](https://travis-ci.com/JuDFTteam/masci-tools.svg?branch=master)](https://travis-ci.com/JuDFTteam/masci-tools)
[![Coverage Status](https://codecov.io/gh/JuDFTteam/masci-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/JuDFTteam/masci-tools)
[![Documentation Status](https://readthedocs.org/projects/masci-tools/badge/?version=latest)](https://masci-tools.readthedocs.io/en/latest/?badge=latest)
[![GitHub version](https://badge.fury.io/gh/JuDFTteam%2Fmasci-tools.svg)](https://badge.fury.io/gh/JuDFTteam%2Fmasci-tools)
[![PyPI version](https://badge.fury.io/py/masci-tools.svg)](https://badge.fury.io/py/masci-tools)


# masci-tools

**This is a collection of tools, common things used by packages of material science.**

Feel free to contribute.

The code is hosted on GitHub at
<https://github.com/JuDFTteam/masci-tools>

The documentation is hosted on https://masci-tools.readthedocs.io.

## Installation

```
pip install masci-tools
```

## Dependencies

These python packages are needed:
* `pymatgen`
* `ase`
* `lxml`
* `matplotlib`
* `h5py`

It should not depend on `aiida_core`!

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
