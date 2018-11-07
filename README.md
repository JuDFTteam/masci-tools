# masci-tools [![Build Status](https://travis-ci.com/JuDFTteam/masci-tools.svg?branch=master)](https://travis-ci.com/JuDFTteam/masci-tools) 

This is a collection of tools, common things used by packages of material science.

Feel free to contribute.

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
