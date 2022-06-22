# Welcome to the [Masci-tools]'s documentation!

This package was developed in the process of developing the [AiiDA-FLEUR] and [AiiDA_KKR] plugins to [AiiDA].
It contains helper functions that can help with common pre- and postprocessing steps of the [FLEUR] and [KKR] codes
developed at the Forschungszentrum Jülich (see also the [juDFT] website for more information).

If you use this package please cite: ...

## Requirements to use this code:

- `lxml`
- `h5py`
- `numpy`
- `matplotlib`
- `bokeh` (optional)
- `seaborn`
- `ase`
- `mendeleev`
- `click`
- `click-completion`
- `PyYAML`
- `tabulate`
- `deepdiff`
- `humanfriendly`
- `more_itertools`

## Installation Instructions:

Install from pypi the latest release

```bash
pip install masci-tools
```

or from the masci-tools source folder any branch

```bash
pip install .
# or which is very useful to keep track of the changes (developers)
pip install -e .
```

## Acknowledgments:

We acknowledge partial support from the EU Centre of Excellence “MaX – Materials Design at the Exascale” (<http://www.max-centre.eu>). (Horizon 2020 EINFRA-5, Grant No. 676598)
We thank the AiiDA team for their help and work. Also the vial exchange with developers of AiiDA packages for other codes was inspiring.

# User's Guide

```{toctree}
:maxdepth: 4

user_guide/index
```

# Developer's Guide

```{toctree}
:maxdepth: 4

devel_guide/index
```

# Reference

```{toctree}
:maxdepth: 2

reference/index
```

# Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`

[aiida]: https://aiida.net
[aiida-fleur]: https://github.com/JuDFTteam/aiida-fleur
[aiida_kkr]: https://github.com/JuDFTteam/aiida-kkr
[fleur]: http://www.flapw.de
[judft]: http://judft.de
[kkr]: https://jukkr.fz-juelich.de
[masci-tools]: https://github.com/JuDFTteam/masci-tools
