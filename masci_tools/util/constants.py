# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the Masci-tools package.                               #
# (Material science tools)                                                    #
#                                                                             #
# The code is hosted on GitHub at https://github.com/judftteam/masci-tools.   #
# For further information on the license, see the LICENSE.txt file.           #
# For further information please visit http://judft.de/.                      #
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
RY_TO_EV = 13.605693122994  #(26)
BOHR_A = 0.5291772108
HTR_TO_KELVIN = 315_775.02480407
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

PERIODIC_TABLE_ELEMENTS = {
    0: {  # This is for empty spheres etc.
        'mass': 1.00000,
        'name': 'Unknown',
        'symbol': 'X'
    },
    1: {
        'mass': 1.00794,
        'name': 'Hydrogen',
        'symbol': 'H',
        'econfig': '1s1',
        'fleur_default_econfig': '| 1s1',
        'lo': '',
        'rmt': 0.65,
        'lmax': '',
        'jri': 981,
        'soc': False,
        'mag': False
    },
    2: {
        'mass': 4.002602,
        'name': 'Helium',
        'symbol': 'He',
        'econfig': '1s2',
        'fleur_default_econfig': '| 1s2',
        'lo': '',
        'rmt': 1.2,
        'lmax': '',
        'jri': 981
    },
    3: {
        'mass': 6.941,
        'name': 'Lithium',
        'symbol': 'Li',
        'econfig': '1s2 | 2s1',
        'fleur_default_econfig': '1s2 | 2s1',
        'lo': '',
        'rmt': 2.13,
        'lmax': '',
        'jri': 981
    },
    4: {
        'mass': 9.012182,
        'name': 'Beryllium',
        'symbol': 'Be',
        'econfig': '1s2 | 2s2',
        'fleur_default_econfig': '1s2 | 2s2',
        'lo': '',
        'rmt': 1.87,
        'lmax': '',
        'jri': 981
    },
    5: {
        'mass': 10.811,
        'name': 'Boron',
        'symbol': 'B',
        'econfig': '1s2 | 2s2 2p1',
        'fleur_default_econfig': '1s2 | 2s2 2p1',
        'lo': '',
        'rmt': 1.4,
        'lmax': '',
        'jri': 981
    },
    6: {
        'mass': 12.0107,
        'name': 'Carbon',
        'symbol': 'C',
        'econfig': '[He] 2s2 | 2p2',
        'fleur_default_econfig': '[He] 2s2 | 2p2',
        'lo': '',
        'rmt': 1.2,
        'lmax': '',
        'jri': 981
    },
    7: {
        'mass': 14.0067,
        'name': 'Nitrogen',
        'symbol': 'N',
        'econfig': '[He] 2s2 | 2p3',
        'fleur_default_econfig': '[He] 2s2 | 2p3',
        'lo': '',
        'rmt': 1.0,
        'lmax': '',
        'jri': 981
    },
    8: {
        'mass': 15.9994,
        'name': 'Oxygen',
        'symbol': 'O',
        'econfig': '[He] 2s2 | 2p4',
        'fleur_default_econfig': '[He] 2s2 | 2p4',
        'lo': '',
        'rmt': 1.1,
        'lmax': '',
        'jri': 981
    },
    9: {
        'mass': 18.9984032,
        'name': 'Fluorine',
        'symbol': 'F',
        'econfig': '[He] 2s2 | 2p5',
        'fleur_default_econfig': '[He] 2s2 | 2p5',
        'lo': '',
        'rmt': 1.2,
        'lmax': '',
        'jri': 981
    },
    10: {
        'mass': 20.1797,
        'name': 'Neon',
        'symbol': 'Ne',
        'econfig': '[He] 2s2 | 2p6',
        'fleur_default_econfig': '[He] 2s2 | 2p6',
        'lo': '',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    11: {
        'mass': 22.98977,
        'name': 'Sodium',
        'symbol': 'Na',
        'econfig': '[He] 2s2 | 2p6 3s1',
        'fleur_default_econfig': '[He] | 2s2 2p6 3s1',
        'lo': '2s 2p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    12: {
        'mass': 24.305,
        'name': 'Magnesium',
        'symbol': 'Mg',
        'econfig': '[He] 2s2 | 2p6 3s2',
        'fleur_default_econfig': '[He] 2s2 | 2p6 3s2',
        'lo': '2p',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    13: {
        'mass': 26.981538,
        'name': 'Aluminium',
        'symbol': 'Al',
        'econfig': '[He] 2s2 2p6 | 3s2 3p1',
        'fleur_default_econfig': '[He] 2s2 2p6 | 3s2 3p1',
        'lo': '',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    14: {
        'mass': 28.0855,
        'name': 'Silicon',
        'symbol': 'Si',
        'econfig': '[He] 2s2 2p6 | 3s2 3p2',
        'fleur_default_econfig': '[He] 2s2 2p6 | 3s2 3p2',
        'lo': '',
        'rmt': 2.0,
        'lmax': '',
        'jri': 981
    },
    15: {
        'mass': 30.973761,
        'name': 'Phosphorus',
        'symbol': 'P',
        'econfig': '[He] 2s2 2p6 | 3s2 3p3',
        'fleur_default_econfig': '[He] 2s2 2p6 | 3s2 3p3',
        'lo': '',
        'rmt': 1.9,
        'lmax': '',
        'jri': 981
    },
    16: {
        'mass': 32.065,
        'name': 'Sulfur',
        'symbol': 'S',
        'econfig': '[He] 2s2 2p6 | 3s2 3p4',
        'fleur_default_econfig': '[He] 2s2 2p6 | 3s2 3p4',
        'lo': '',
        'rmt': 1.7,
        'lmax': '',
        'jri': 981
    },
    17: {
        'mass': 35.453,
        'name': 'Chlorine',
        'symbol': 'Cl',
        'econfig': '[He] 2s2 2p6 | 3s2 3p5',
        'fleur_default_econfig': '[He] 2s2 2p6 | 3s2 3p5',
        'lo': '',
        'rmt': 1.7,
        'lmax': '',
        'jri': 981
    },
    18: {
        'mass': 39.948,
        'name': 'Argon',
        'symbol': 'Ar',
        'econfig': '[He] 2s2 2p6 | 3s2 3p6',
        'fleur_default_econfig': '[He] 2s2 2p6 | 3s2 3p6',
        'lo': '',
        'rmt': 1.8,
        'lmax': '',
        'jri': 981
    },
    19: {
        'mass': 39.0983,
        'name': 'Potassium',
        'symbol': 'K',
        'econfig': '[Ne] 3s2 | 3p6 4s1',
        'fleur_default_econfig': '[Ne] | 3s2 3p6 4s1',
        'lo': '3s 3p',
        'rmt': 2.0,
        'lmax': '',
        'jri': 981
    },
    20: {
        'mass': 40.078,
        'name': 'Calcium',
        'symbol': 'Ca',
        'econfig': '[Ne] 3s2 | 3p6 4s2',
        'fleur_default_econfig': '[Ne] | 3s2 3p6 4s2',
        'lo': '3s 3p',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    21: {
        'mass': 44.955912,
        'name': 'Scandium',
        'symbol': 'Sc',
        'econfig': '[Ne] 3s2 3p6 | 4s2 3d1',
        'fleur_default_econfig': '[Ne] | 3s2 3p6 4s2 3d1',
        'lo': '3s 3p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    22: {
        'mass': 47.867,
        'name': 'Titanium',
        'symbol': 'Ti',
        'econfig': '[Ne] | 3s2 3p6 4s2 3d2',
        'fleur_default_econfig': '[Ne] | 3s2 3p6 4s2 3d2',
        'lo': '3s 3p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    23: {
        'mass': 50.9415,
        'name': 'Vanadium',
        'symbol': 'V',
        'econfig': '[Ne] 3s2 3p6 | 4s2 3d3',
        'fleur_default_econfig': '[Ne] | 3s2 3p6 4s2 3d3',
        'lo': '3s 3p',
        'rmt': 1.9,
        'lmax': '',
        'jri': 981
    },
    24: {
        'mass': 51.9961,
        'name': 'Chromium',
        'symbol': 'Cr',
        'econfig': '[Ne] 3s2 3p6 | 4s1 3d5',
        'fleur_default_econfig': '[Ne] | 3s2 3p6 4s1 3d5',
        'lo': '3s 3p',
        'rmt': 1.8,
        'lmax': '',
        'jri': 981
    },
    25: {
        'mass': 54.938045,
        'name': 'Manganese',
        'symbol': 'Mn',
        'econfig': '[Ne] 3s2 3p6 | 4s2 3d5',
        'fleur_default_econfig': '[Ne] | 3s2 3p6 4s2 3d5',
        'lo': '3s 3p',
        'rmt': 2.0,
        'lmax': '',
        'jri': 981
    },
    26: {
        'mass': 55.845,
        'name': 'Iron',
        'symbol': 'Fe',
        'econfig': '[Ne] 3s2 3p6 | 4s2 3d6',
        'fleur_default_econfig': '[Ne] | 3s2 3p6 4s2 3d6',
        'lo': '3s 3p',
        'rmt': 2.00,
        'lmax': '',
        'jri': 981
    },
    27: {
        'mass': 58.933195,
        'name': 'Cobalt',
        'symbol': 'Co',
        'econfig': '[Ne] 3s2 3p6 | 4s2 3d7',
        'fleur_default_econfig': '[Ne] 3s2 | 3p6 4s2 3d7',
        'lo': '3p',
        'rmt': 1.9,
        'lmax': '',
        'jri': 981
    },
    28: {
        'mass': 58.6934,
        'name': 'Nickel',
        'symbol': 'Ni',
        'econfig': '[Ne] 3s2 3p6 | 4s2 3d8',
        'fleur_default_econfig': '[Ne] 3s2 | 3p6 4s2 3d8',
        'lo': '3p',
        'rmt': 1.9,
        'lmax': '',
        'jri': 981
    },
    29: {
        'mass': 63.546,
        'name': 'Copper',
        'symbol': 'Cu',
        'econfig': '[Ne] 3s2 3p6 |4s1 3d10',
        'fleur_default_econfig': '[Ne] 3s2 | 3p6 4s1 3d10',
        'lo': '3p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    30: {
        'mass': 65.38,
        'name': 'Zinc',
        'symbol': 'Zn',
        'econfig': '[Ne] 3s2 3p6 | 3d10 4s2',
        'fleur_default_econfig': '[Ne] 3s2 3p6 | 3d10 4s2',
        'lo': '3d',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    31: {
        'mass': 69.723,
        'name': 'Gallium',
        'symbol': 'Ga',
        'econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p1',
        'fleur_default_econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p1',
        'lo': '3d',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    32: {
        'mass': 72.64,
        'name': 'Germanium',
        'symbol': 'Ge',
        'econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p2',
        'fleur_default_econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p2',
        'lo': '3d',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    33: {
        'mass': 74.9216,
        'name': 'Arsenic',
        'symbol': 'As',
        'econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p3',
        'fleur_default_econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p3',
        'lo': '3d',
        'rmt': 2.0,
        'lmax': '',
        'jri': 981
    },
    34: {
        'mass': 78.96,
        'name': 'Selenium',
        'symbol': 'Se',
        'econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p4',
        'fleur_default_econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p4',
        'lo': '3d',
        'rmt': 2.0,
        'lmax': '',
        'jri': 981
    },
    35: {
        'mass': 79.904,
        'name': 'Bromine',
        'symbol': 'Br',
        'econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p5',
        'fleur_default_econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p5',
        'lo': '3d',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    36: {
        'mass': 83.798,
        'name': 'Krypton',
        'symbol': 'Kr',
        'econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p6',
        'fleur_default_econfig': '[Ne] 3s2 3p6 | 3d10 4s2 4p6',
        'lo': '3d',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    37: {
        'mass': 85.4678,
        'name': 'Rubidium',
        'symbol': 'Rb',
        'econfig': '[Ar] 3d10 4s2 | 4p6 5s1',
        'fleur_default_econfig': '[Ar] 3d10 | 4s2 4p6 5s1',
        'lo': '4s 4p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    38: {
        'mass': 87.62,
        'name': 'Strontium',
        'symbol': 'Sr',
        'econfig': '[Ar] 3d10 4s2 | 4p6 5s2',
        'fleur_default_econfig': '[Ar] 3d10 | 4s2 4p6 5s2',
        'lo': '4s 4p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    39: {
        'mass': 88.90585,
        'name': 'Yttrium',
        'symbol': 'Y',
        'econfig': '[Ar] 4s2 3d10 4p6 | 5s2 4d1',
        'fleur_default_econfig': '[Ar] 3d10 | 4s2 4p6 5s2 4d1',
        'lo': '4s 4p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    40: {
        'mass': 91.224,
        'name': 'Zirconium',
        'symbol': 'Zr',
        'econfig': '[Ar] 4s2 3d10 4p6 | 5s2 4d2',
        'fleur_default_econfig': '[Ar] 3d10 | 4s2 4p6 5s2 4d2',
        'lo': '4s 4p',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    41: {
        'mass': 92.90638,
        'name': 'Niobium',
        'symbol': 'Nb',
        'econfig': '[Ar] 4s2 3d10 4p6 | 5s1 4d4',
        'fleur_default_econfig': '[Ar] 3d10 | 4s2 4p6 5s1 4d4',
        'lo': '4s 4p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    42: {
        'mass': 95.96,
        'name': 'Molybdenum',
        'symbol': 'Mo',
        'econfig': '[Ar] 4s2 3d10 4p6 | 5s1 4d5',
        'fleur_default_econfig': '[Ar] 3d10 | 4s2 4p6 5s1 4d5',
        'lo': '4s 4p',
        'rmt': 2.0,
        'lmax': '',
        'jri': 981
    },
    43: {
        'mass': 98.0,
        'name': 'Technetium',
        'symbol': 'Tc',
        'econfig': '[Ar] 4s2 3d10 4p6 | 5s2 4d5',
        'fleur_default_econfig': '[Ar] 3d10 | 4s2 4p6 5s2 4d5',
        'lo': '4s 4p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    44: {
        'mass': 101.07,
        'name': 'Ruthenium',
        'symbol': 'Ru',
        'econfig': '[Ar] 4s2 3d10 4p6 | 5s1 4d7',
        'fleur_default_econfig': '[Ar] 4s2 3d10 | 4p6 5s1 4d7',
        'lo': '4p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    45: {
        'mass': 102.9055,
        'name': 'Rhodium',
        'symbol': 'Rh',
        'econfig': '[Ar] 4s2 3d10 4p6 | 5s1 4d8',
        'fleur_default_econfig': '[Ar] 4s2 3d10 | 4p6 5s1 4d8',
        'lo': '4p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    46: {
        'mass': 106.42,
        'name': 'Palladium',
        'symbol': 'Pd',
        'econfig': '[Ar] 4s2 3d10 4p6 | 4d10',
        'fleur_default_econfig': '[Ar] 4s2 3d10 | 4p6 4d10',
        'lo': '4p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    47: {
        'mass': 107.8682,
        'name': 'Silver',
        'symbol': 'Ag',
        'econfig': '[Ar] 4s2 3d10 4p6 | 5s1 4d10',
        'fleur_default_econfig': '[Ar] 3d10 | 4s2 4p6 5s1 4d10',
        'lo': '4s 4p',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    48: {
        'mass': 112.411,
        'name': 'Cadmium',
        'symbol': 'Cd',
        'econfig': '[Ar] 4s2 3d10 4p6 | 4d10 5s2',
        'fleur_default_econfig': '[Ar] 4s2 3d10 4p6 | 4d10 5s2',
        'lo': '4d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    49: {
        'mass': 114.818,
        'name': 'Indium',
        'symbol': 'In',
        'econfig': '[Ar] 4s2 3d10 4p6 | 4d10 5s2 5p1',
        'fleur_default_econfig': '[Ar] 4s2 3d10 4p6 | 4d10 5s2 5p1',
        'lo': '4d',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    50: {
        'mass': 118.71,
        'name': 'Tin',
        'symbol': 'Sn',
        'econfig': '[Kr] 4d10 | 5s2 5p2',
        'fleur_default_econfig': '[Kr] | 4d10 5s2 5p2',
        'lo': '4d',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    51: {
        'mass': 121.76,
        'name': 'Antimony',
        'symbol': 'Sb',
        'econfig': '[Kr] 4d10 | 5s2 5p3',
        'fleur_default_econfig': '[Kr] | 4d10 5s2 5p3',
        'lo': '4d',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    52: {
        'mass': 127.6,
        'name': 'Tellurium',
        'symbol': 'Te',
        'econfig': '[Kr] 4d10 | 5s2 5p4',
        'fleur_default_econfig': '[Kr] | 4d10 5s2 5p4',
        'lo': '4d',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    53: {
        'mass': 126.90447,
        'name': 'Iodine',
        'symbol': 'I',
        'econfig': '[Kr] 4d10 | 5s2 5p5',
        'fleur_default_econfig': '[Kr] | 4d10 5s2 5p5',
        'lo': '4d',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    54: {
        'mass': 131.293,
        'name': 'Xenon',
        'symbol': 'Xe',
        'econfig': '[Kr] 4d10 | 5s2 5p6',
        'fleur_default_econfig': '[Kr] | 4d10 5s2 5p6',
        'lo': '4d',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    55: {
        'mass': 132.9054519,
        'name': 'Caesium',
        'symbol': 'Cs',
        'econfig': '[Kr] 4d10 5s2 | 5p6 6s1',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s1',
        'lo': '5s 5p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    56: {
        'mass': 137.327,
        'name': 'Barium',
        'symbol': 'Ba',
        'econfig': '[Kr] 4d10 5s2 | 5p6 6s2',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2',
        'lo': '5s 5p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    57: {
        'mass': 138.90547,
        'name': 'Lanthanum',
        'symbol': 'La',
        'econfig': '[Kr] 4d10 5s2 | 5p6 6s2 5d1',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 5d1',
        'lo': '5s 5p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    58: {
        'mass': 140.116,
        'name': 'Cerium',
        'symbol': 'Ce',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f1 5d1',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f1 5d1',
        'lo': '5s 5p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    59: {
        'mass': 140.90765,
        'name': 'Praseodymium',
        'symbol': 'Pr',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f3',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6  6s2 4f3',
        'lo': '5s 5p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    60: {
        'mass': 144.242,
        'name': 'Neodymium',
        'symbol': 'Nd',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f4',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f4',
        'lo': '5s 5p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    61: {
        'mass': 145.0,
        'name': 'Promethium',
        'symbol': 'Pm',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f5',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f5',
        'lo': '5s 5p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    62: {
        'mass': 150.36,
        'name': 'Samarium',
        'symbol': 'Sm',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f6',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f6',
        'lo': '5s 5p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    63: {
        'mass': 151.964,
        'name': 'Europium',
        'symbol': 'Eu',
        'econfig': '[Kr] 4d10 | 4f7 5s2 5p6 6s2',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 4f7 6s2',
        'lo': '5s 5p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    64: {
        'mass': 157.25,
        'name': 'Gadolinium',
        'symbol': 'Gd',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f7 5d1',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f7 5d1',
        'lo': '5s 5p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    65: {
        'mass': 158.92535,
        'name': 'Terbium',
        'symbol': 'Tb',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f9',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f8 5d1',
        'lo': '5s 5p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    66: {
        'mass': 162.5,
        'name': 'Dysprosium',
        'symbol': 'Dy',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f10',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f9 5d1',
        'lo': '5s 5p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    67: {
        'mass': 164.93032,
        'name': 'Holmium',
        'symbol': 'Ho',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f11',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f10 5d1',
        'lo': '5s 5p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    68: {
        'mass': 167.259,
        'name': 'Erbium',
        'symbol': 'Er',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f12',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f11 5d1',
        'lo': '5s 5p',
        'rmt': 2.5,
        'lmax': '',
        'jri': 981
    },
    69: {
        'mass': 168.93421,
        'name': 'Thulium',
        'symbol': 'Tm',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f13',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f12 5d1',
        'lo': '5s 5p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    70: {
        'mass': 173.054,
        'name': 'Ytterbium',
        'symbol': 'Yb',
        'econfig': '[Kr] 4d10 5s2 5p6 | 6s2 4f14',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 6s2 4f13 5d1',
        'lo': '5s 5p',
        'rmt': 2.6,
        'lmax': '',
        'jri': 981
    },
    71: {
        'mass': 174.9668,
        'name': 'Lutetium',
        'symbol': 'Lu',
        'econfig': '[Kr] 4d10 | 4f14 5s2 5p6 5d1 6s2',
        'fleur_default_econfig': '[Kr] 4d10 | 5s2 5p6 4f14 6s2 5d1',
        'lo': '5s 5p',
        'rmt': 2.5,
        'lmax': '',
        'jri': 981
    },
    72: {
        'mass': 178.49,
        'name': 'Hafnium',
        'symbol': 'Hf',
        'econfig': '[Kr] 4d10 | 4f14 5s2 5p6 5d2 6s2',
        'fleur_default_econfig': '[Kr] 4d10 4f14 | 5s2 5p6 6s2 5d2',
        'lo': '5s 5p',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    73: {
        'mass': 180.94788,
        'name': 'Tantalum',
        'symbol': 'Ta',
        'econfig': '[Kr] 4d10 4f14 | 5s2 5p6 5d3 6s2',
        'fleur_default_econfig': '[Kr] 4d10 4f14 | 5s2 5p6 6s2 5d3',
        'lo': '5s 5p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    74: {
        'mass': 183.84,
        'name': 'Tungsten',
        'symbol': 'W',
        'econfig': '[Kr] 5s2 4d10 4f14 | 5p6 6s2 5d4',
        'fleur_default_econfig': '[Kr] 4d10 4f14 | 5s2 5p6 6s2 5d4',
        'lo': '5s 5p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    75: {
        'mass': 186.207,
        'name': 'Rhenium',
        'symbol': 'Re',
        'econfig': '[Kr] 4d10 4f14 5p6 | 5s2 6s2 5d5',
        'fleur_default_econfig': '[Kr] 4d10 4f14 | 5s2 5p6 6s2 5d5',
        'lo': '5s 5p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    76: {
        'mass': 190.23,
        'name': 'Osmium',
        'symbol': 'Os',
        'econfig': '[Kr] 4d10 4f14 5p6 | 5s2 6s2 5d6',
        'fleur_default_econfig': '[Kr] 5s2 4d10 4f14 | 5p6 6s2 5d6',
        'lo': '5p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    77: {
        'mass': 192.217,
        'name': 'Iridium',
        'symbol': 'Ir',
        'econfig': '[Kr] 4d10 4f14 5p6 | 5s2 6s2 5d7',
        'fleur_default_econfig': '[Kr] 5s2 4d10 4f14 | 5p6 6s2 5d7',
        'lo': '5p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    78: {
        'mass': 195.084,
        'name': 'Platinum',
        'symbol': 'Pt',
        'econfig': '[Kr] 4d10 4f14 5p6 | 5s2 6s2 5d8',
        'fleur_default_econfig': '[Kr] 5s2 4d10 4f14 | 5p6 6s2 5d8',
        'lo': '5p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    79: {
        'mass': 196.966569,
        'name': 'Gold',
        'symbol': 'Au',
        'econfig': '[Kr] 4d10 4f14 5p6 | 5s2 6s2 5d9',
        'fleur_default_econfig': '[Kr] 4d10 4f14 | 5s2 5p6 6s2 5d9',
        'lo': '5s 5p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    80: {
        'mass': 200.59,
        'name': 'Mercury',
        'symbol': 'Hg',
        'econfig': '[Kr] 5s2 4d10 4f14 | 5p6 5d10 6s2',
        'fleur_default_econfig': '[Kr] 5s2 4d10 4f14 5p6 | 5d10 6s2',
        'lo': '5d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    81: {
        'mass': 204.3833,
        'name': 'Thallium',
        'symbol': 'Tl',
        'econfig': '[Xe] 4f14 | 5d10 6s2 6p1',
        'fleur_default_econfig': '[Xe] 4f14 | 5d10 6s2 6p1',
        'lo': '5d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    82: {
        'mass': 207.2,
        'name': 'Lead',
        'symbol': 'Pb',
        'econfig': '[Xe] 4f14 | 5d10 6s2 6p2',
        'fleur_default_econfig': '[Xe] 4f14 | 5d10 6s2 6p2',
        'lo': '5d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    83: {
        'mass': 208.9804,
        'name': 'Bismuth',
        'symbol': 'Bi',
        'econfig': '[Xe] 4f14 | 5d10 6s2 6p3',
        'fleur_default_econfig': '[Xe] 4f14 | 5d10 6s2 6p3',
        'lo': '5d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    84: {
        'mass': 209.0,
        'name': 'Polonium',
        'symbol': 'Po',
        'econfig': '[Xe] 4f14 | 5d10 6s2 6p4',
        'fleur_default_econfig': '[Xe] 4f14 | 5d10 6s2 6p4',
        'lo': '5d',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    85: {
        'mass': 210.0,
        'name': 'Astatine',
        'symbol': 'At',
        'econfig': '[Xe] 4f14 | 5d10 6s2 6p5',
        'fleur_default_econfig': '[Xe] 4f14 | 5d10 6s2 6p5',
        'lo': '5d',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    86: {
        'mass': 222.0,
        'name': 'Radon',
        'symbol': 'Rn',
        'econfig': '[Xe] 4f14 | 5d10 6s2 6p6',
        'fleur_default_econfig': '[Xe] 4f14 | 5d10 6s2 6p6',
        'lo': '5d',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },  # TODO: after wards not rigth
    87: {
        'mass': 223.0,
        'name': 'Francium',
        'symbol': 'Fr',
        'econfig': '[Xe] 4f14 5d10 6s2 | 6p6 7s1',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s1',
        'lo': '6s 6p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    88: {
        'mass': 226.0,
        'name': 'Radium',
        'symbol': 'Ra',
        'econfig': '[Xe] 4f14 5d10 6s2 | 6p6 7s2',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2',
        'lo': '6s 6p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    89: {
        'mass': 227.0,
        'name': 'Actinium',
        'symbol': 'Ac',
        'econfig': '[Xe] 4f14 5d10 6s2 | 6p6 7s2 6d1',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 6d1',
        'lo': '6s 6p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    90: {
        'mass': 232.03806,
        'name': 'Thorium',
        'symbol': 'Th',
        'econfig': '[Xe] 4f14 5d10 6s2 | 6p6 7s2 6d1 5f1',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 6d1 5f1',
        'lo': '6s 6p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    91: {
        'mass': 231.03588,
        'name': 'Protactinium',
        'symbol': 'Pa',
        'econfig': '[Xe] 4f14  5d10 6s2 | 6p6 7s2 6d1 5f2',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 6d1 5f2',
        'lo': '6s 6p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    92: {
        'mass': 238.02891,
        'name': 'Uranium',
        'symbol': 'U',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6| 7s2 5f4',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f4',
        'lo': '6s 6p',
        'rmt': 2.3,
        'lmax': '',
        'jri': 981
    },
    93: {
        'mass': 237.0,
        'name': 'Neptunium',
        'symbol': 'Np',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f5',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f5',
        'lo': '6s 6p',
        'rmt': 2.1,
        'lmax': '',
        'jri': 981
    },
    94: {
        'mass': 244.0,
        'name': 'Plutonium',
        'symbol': 'Pu',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f6',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f6',
        'lo': '6s 6p',
        'rmt': 2.2,
        'lmax': '',
        'jri': 981
    },
    95: {
        'mass': 243.0,
        'name': 'Americium',
        'symbol': 'Am',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f7',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f7',
        'lo': '6s 6p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    96: {
        'mass': 247.0,
        'name': 'Curium',
        'symbol': 'Cm',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f8',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f8',
        'lo': '6s 6p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    97: {
        'mass': 247.0,
        'name': 'Berkelium',
        'symbol': 'Bk',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f9',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f9',
        'lo': '6s 6p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    98: {
        'mass': 251.0,
        'name': 'Californium',
        'symbol': 'Cf',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f10',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f10',
        'lo': '6s 6p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    99: {
        'mass': 252.0,
        'name': 'Einsteinium',
        'symbol': 'Es',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f11',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f11',
        'lo': '6s 6p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    100: {
        'mass': 257.0,
        'name': 'Fermium',
        'symbol': 'Fm',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f12',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f12',
        'lo': '6s 6p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    101: {
        'mass': 258.0,
        'name': 'Mendelevium',
        'symbol': 'Md',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f13',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f13',
        'lo': '6s 6p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    102: {
        'mass': 259.0,
        'name': 'Nobelium',
        'symbol': 'No',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f14',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f14',
        'lo': '6s 6p',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    103: {
        'mass': 262.0,
        'name': 'Lawrencium',
        'symbol': 'Lr',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f14 6d1',
        'fleur_default_econfig': '[Xe] 4f14 5d10 | 6s2 6p6 7s2 5f14 6d1',
        'lo': '6s 6p 5f',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    104: {
        'mass': 267.0,
        'name': 'Rutherfordium',
        'symbol': 'Rf',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f14 6d2',
        'fleur_default_econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f14 6d2',
        'lo': '6p 5f',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    105: {
        'mass': 268.0,
        'name': 'Dubnium',
        'symbol': 'Db',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f14 6d3',
        'fleur_default_econfig': '[Xe] 4f14 5d10 6s2 | 6p6 7s2 5f14 6d3',
        'lo': '6p 5f',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    106: {
        'mass': 271.0,
        'name': 'Seaborgium',
        'symbol': 'Sg',
        'econfig': '[Xe] 4f14 5d10 6s2 6p6 | 7s2 5f14 6d4',
        'fleur_default_econfig': '[Xe] 4f14 5d10 6s2 | 6p6 7s2 5f14 6d4',
        'lo': '6p 5f',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    107: {
        'mass': 272.0,
        'name': 'Bohrium',
        'symbol': 'Bh',
        'econfig': '[Rn] 7s2 5f14 | 6d5',
        'fleur_default_econfig': '[Xe] 4f14 5d10 6s2 6p6 5f14 | 7s2 6d5',
        'lo': '',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    108: {
        'mass': 270.0,
        'name': 'Hassium',
        'symbol': 'Hs',
        'econfig': '[Rn] 7s2 5f14 | 6d6',
        'fleur_default_econfig': '[Rn] 5f14 | 7s2 6d6',
        'lo': '',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    109: {
        'mass': 276.0,
        'name': 'Meitnerium',
        'symbol': 'Mt',
        'econfig': '[Rn] 7s2 5f14 | 6d7',
        'fleur_default_econfig': '[Rn] 5f14 | 7s2 6d7',
        'lo': '',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    110: {
        'mass': 281.0,
        'name': 'Darmstadtium',
        'symbol': 'Ds',
        'econfig': '[Rn] 7s2 5f14 | 6d8',
        'fleur_default_econfig': '[Rn] 5f14 | 7s2 6d8',
        'lo': '',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    111: {
        'mass': 280.0,
        'name': 'Roentgenium',
        'symbol': 'Rg',
        'econfig': '[Rn] 7s2 5f14 | 6d9',
        'fleur_default_econfig': '[Rn] 5f14 | 7s2 6d9',
        'lo': '',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    112: {
        'mass': 285.0,
        'name': 'Copernicium',
        'symbol': 'Cn',
        'econfig': '[Rn] 7s2 5f14 | 6d10',
        'fleur_default_econfig': '[Rn] 5f14 | 7s2 6d10',
        'lo': '6d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    113: {
        'mass': 285.0,
        'name': 'Nihomium',
        'symbol': 'Nh',
        'econfig': '[Rn] 7s2 5f14 | 6d10 7p1',
        'fleur_default_econfig': '[Rn] 7s2 5f14 | 6d10 7p1',
        'lo': '6d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    114: {
        'mass': 289.0,
        'name': 'Flerovium',
        'symbol': 'Fl',
        'econfig': '[Rn] 7s2 5f14 | 6d10 7p2',
        'fleur_default_econfig': '[Rn] 7s2 5f14 | 6d10 7p2',
        'lo': '6d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    115: {
        'mass': 0.0,
        'name': 'Mascovium',
        'symbol': 'Mc',
        'econfig': '[Rn] 7s2 5f14 | 6d10 7p3',
        'fleur_default_econfig': '[Rn] 7s2 5f14 | 6d10 7p3',
        'lo': '6d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    116: {
        'mass': 293.0,
        'name': 'Livermorium',
        'symbol': 'Lv',
        'econfig': '[Rn] 7s2 5f14 | 6d10 7p4',
        'fleur_default_econfig': '[Rn] 7s2 5f14 | 6d10 7p4',
        'lo': '6d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    117: {
        'mass': 0.0,
        'name': 'Tennessine',
        'symbol': 'Ts',
        'econfig': '[Rn] 7s2 5f14 | 6d10 7p5',
        'fleur_default_econfig': '[Rn] 7s2 5f14 | 6d10 7p5',
        'lo': '6d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    },
    118: {
        'mass': 0.0,
        'name': 'Oganesson',
        'symbol': 'Og',
        'econfig': '[Rn] 7s2 5f14 | 6d10 7p6',
        'fleur_default_econfig': '[Rn] 7s2 5f14 | 6d10 7p6',
        'lo': '6d',
        'rmt': 2.4,
        'lmax': '',
        'jri': 981
    }
}
