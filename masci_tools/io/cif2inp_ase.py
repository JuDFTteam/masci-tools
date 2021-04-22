#!/usr/bin/env python3
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
Independent utility script to convert cif file formats to input for the inpgen code
Usage: `python cif2inp_ase.py <filename.cif>`
"""

import sys
import ase.io
import numpy as np

cifFilename = sys.argv[1]
structure = ase.io.read(cifFilename)

structureFormula = structure.get_chemical_formula()
inpFilename = 'inp_' + structureFormula

Binv = np.linalg.inv(structure.cell)
frac_coordinates = structure.arrays['positions'].dot(Binv)

with open(inpFilename, 'w+') as f:
    natoms = len(structure.arrays['numbers'])
    f.write(structureFormula + '\r\n')
    f.write('&input film=F /\r\n')
    for i in range(3):
        f.write(' '.join(map('{:.12f}'.format, structure.cell[i])) + '\r\n')
    f.write('1.8897    !lattice const scaled as(1.0*bohr)\r\n1.0000 1.0000 1.0000    !scaling\r\n\r\n')
    f.write(str(natoms) + '\r\n')
    for i in range(natoms):
        f.write(
            str(structure.arrays['numbers'][i]) + ' ' + ' '.join(map('{:.12f}'.format, frac_coordinates[i])) + '\r\n')
    f.write('\r\n')
