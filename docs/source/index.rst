.. fleur_fleur documentation master file, created by
   sphinx-quickstart on Wed Aug 10 10:20:55 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the `Masci-tools`_'s documentation!
##############################################


.. _FLEUR: http://www.flapw.de
.. _AiiDA-FLEUR: https://github.com/JuDFTteam/aiida-fleur
.. _Masci-tools: https://github.com/JuDFTteam/masci-tools
.. _AiiDA_KKR: https://github.com/JuDFTteam/aiida-kkr
.. _AIIDA: https://aiida.net
.. _KKR: https://jukkr.fz-juelich.de
.. _juDFT: http://judft.de

This package was developed in the process of developing the `AiiDA-FLEUR`_ and `AiiDA_KKR`_ plugins to `AiiDA`_.
It contains helper functions that can help with common pre- and postprocessing steps of the `FLEUR`_ and `KKR`_ codes developed at the Forschungszentrum Jülich (see also the `juDFT`_ website for more information).

If you use this package please cite: ...


Requirements to use this code:
------------------------------

* lxml
* h5py
* ase
* pymatgen
* numpy
* scipy
* more_itertools

Installation Instructions:
--------------------------

Install from pypi the latest release::

    $ pip install masci-tools


or from the masci-tools source folder any branch::

    $ pip install .
    # or which is very useful to keep track of the changes (developers)
    $ pip install -e . 

Acknowledgments:
----------------

We acknowledge partial support from the EU Centre of Excellence “MaX – Materials Design at the Exascale” (http://www.max-centre.eu). (Horizon 2020 EINFRA-5, Grant No. 676598)
We thank the AiiDA team for their help and work. Also the vial exchange with developers of AiiDA packages for other codes was inspiring.

User's Guide
############

.. toctree::
   :maxdepth: 4
 
   user_guide/index

  
Developer's Guide
#################

.. toctree::
   :maxdepth: 4

   devel_guide/index

Module reference (API)
######################

.. toctree::
   :maxdepth: 4

   module_guide/mg_index
      


Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
