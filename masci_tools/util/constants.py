# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
#                                                                             #
###############################################################################
"""
Here we collect physical constants which are used throughout the code
that way we ensure consistency

.. literalinclude:: ../../../masci_tools/util/constants.py
   :language: python
   :lines: 23-
   :linenos:

"""
import numpy as np

#Predefined constants in the Fleur Code (These are accepted in the inp.xml)
FLEUR_DEFINED_CONSTANTS = {
    'Pi': np.pi,
    'Deg': 2 * np.pi / 360.0,
    'Ang': 1.8897261247728981,
    'nm': 18.897261247728981,
    'pm': 0.018897261247728981,
    'Bohr': 1.0
}

# NIST https://physics.nist.gov/cgi-bin/cuu/Value?hrev
HTR_TO_EV = 27.211386245988  #(53)
BOHR_A = 0.5291772108
#Scipy bohr 5.29177210903e-11 m
#Scipy htr 27.211386245988 eV
# NIST BOHR 0.529177210903 #(80)
#https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0

#Fleur
#htr_eV   = 27.21138602
#bohr=0.5291772108
#bohrtocm=0.529177e-8
#pymatgen uses scipy.constants
#ase: Bohr 0.5291772105638411
#Hartree 27.211386024367243
#Rydberg 13.605693012183622
#1/Bohr
#1.8897261258369282
#aiida-core units:
#bohr_to_ang = 0.52917720859
