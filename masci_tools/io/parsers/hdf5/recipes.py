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
This module defines commonly used recipes for the :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader`

Available are:
    - Recipe for bandstructure calculations with Fleur
    - Recipes for almost all DOS calculation modes of Fleur

A Recipe is a python dictionary in a specific format.

A Template Example:

.. code-block:: python

    from masci_tools.io.parser.hdf5.readers import Transformation, AttribTransformation

    RecipeExample = {
        'datasets': {
            'example_dataset': {
                'h5path': '/path/in/hdf/file',
                'transforms': [Transformation(name='get_first_element')]
            },
            'example_attrib_transform': {
                'h5path': '/other/path/in/hdf/file',
                'transforms': [AttribTransformation(name='multiply_by_attribute', attrib_name='example_attribute')]
            }
        },
        'attributes': {
            'example_attribute': {
                'h5path':
                '/path/in/hdf/file',
                'transforms':
                [Transformation(name='get_attribute', args=('attribName',)),
                 Transformation(name='get_first_element')]
            }
        }
    }

The Recipe consists of two sections 'datasets' and 'attributes'. All data from these two sections will be returned
in separate python dictionaries by the :py:class:`~masci_tools.io.parsers.hdf5.reader.HDF5Reader` class

Each entry in those sections has to have a `h5path` entry, which will specify the dataset to initially
read from the hdf file. Then each entry can define a entry `transforms` with a list of the namedtuples
imported at the top of the code example. These corresponds to function calls to functions in
:py:mod:`~masci_tools.io.parsers.hdf5.transforms` to transform the read in data

Entries in the `attributes` section are read and transformed first and can subsequently be used in transformations
for the `datasets`. These correpsond to the transforms created with the :py:class:`~masci_tools.io.parsers.hdf5.reader.AttribTransformation`
namedtuple instead of :py:class:`~masci_tools.io.parsers.hdf5.reader.Transformation`.
"""
from __future__ import annotations

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  #type:ignore
from masci_tools.util.constants import HTR_TO_EV, BOHR_A
from .reader import HDF5Recipe, Transformation, AttribTransformation


def dos_recipe_format(group: Literal['Local', 'jDOS', 'Orbcomp', 'MCD']) -> HDF5Recipe:
    """
    Format for denisty of states calculations retrieving the DOS from the given group

    :param group: str of the group the DOS should be taken from

    :returns: dict of the recipe to retrieve a DOS calculation
    """

    if group == 'Local':
        atom_prefix = 'MT:'
    elif group == 'jDOS':
        atom_prefix = 'jDOS:'
    elif group == 'Orbcomp':
        atom_prefix = 'ORB:'
    elif group == 'MCD':
        atom_prefix = 'At'
    else:
        raise ValueError(f'Unknown group: {group}')

    return HDF5Recipe({
        'datasets': {
            'dos': {
                'h5path':
                f'/{group}/DOS',
                'transforms': [
                    Transformation(name='get_all_child_datasets', kwargs={'ignore': 'energyGrid'}),
                    AttribTransformation(name='add_partial_sums',
                                         attrib_name='atoms_groups',
                                         args=(f'{atom_prefix}{{}}'.format,),
                                         kwargs={'make_set': True}),
                    Transformation(name='multiply_scalar', args=(1.0 / HTR_TO_EV,)),
                    Transformation(
                        name='split_array',
                        kwargs={'suffixes': ['up', 'down']},
                    )
                ],
                'unpack_dict':
                True,
            },
            'energy_grid': {
                'h5path': f'/{group}/DOS/energyGrid',
                'transforms': [Transformation(name='multiply_scalar', args=(HTR_TO_EV,))]
            }
        },
        'attributes': {
            'group_name': {
                'h5path': f'/{group}',
                'transforms': [
                    Transformation(name='get_name'),
                ],
            },
            'n_types': {
                'h5path':
                '/atoms',
                'description':
                'Number of atom types',
                'transforms':
                [Transformation(name='get_attribute', args=('nTypes',)),
                 Transformation(name='get_first_element')]
            },
            'atoms_elements': {
                'h5path': '/atoms/atomicNumbers',
                'description': 'Atomic numbers',
                'transforms': [Transformation(name='periodic_elements')]
            },
            'atoms_groups': {
                'h5path': '/atoms/equivAtomsGroup'
            },
            'fermi_energy': {
                'h5path':
                '/general',
                'description':
                'fermi_energy of the system',
                'transforms': [
                    Transformation(name='get_attribute', args=('lastFermiEnergy',)),
                    Transformation(name='get_first_element')
                ]
            },
            'spins': {
                'h5path':
                '/general',
                'description':
                'number of distinct spin directions in the system',
                'transforms':
                [Transformation(name='get_attribute', args=('spins',)),
                 Transformation(name='get_first_element')]
            }
        }
    })


#DOS Recipes
FleurDOS = dos_recipe_format('Local')
FleurJDOS = dos_recipe_format('jDOS')
FleurORBCOMP = dos_recipe_format('Orbcomp')
FleurMCD = dos_recipe_format('MCD')


def bands_recipe_format(group: Literal['Local', 'jDOS', 'Orbcomp', 'MCD'], simple: bool = False) -> HDF5Recipe:
    """
    Format for bandstructure calculations retrieving weights from the given group

    :param group: str of the group the weights should be taken from
    :param simple: bool, if True no additional weights are retrieved with the produced recipe

    :returns: dict of the recipe to retrieve a bandstructure calculation
    """

    if group == 'Local':
        atom_prefix = 'MT:'
    elif group == 'jDOS':
        atom_prefix = 'jDOS:'
    elif group == 'Orbcomp':
        atom_prefix = 'ORB:'
    elif group == 'MCD':
        atom_prefix = 'At'
    else:
        raise ValueError(f'Unknown group: {group}')

    recipe = HDF5Recipe({
        'datasets': {
            'eigenvalues': {
                'h5path':
                f'/{group}/BS/eigenvalues',
                'transforms': [
                    AttribTransformation(name='shift_by_attribute',
                                         attrib_name='fermi_energy',
                                         kwargs={
                                             'negative': True,
                                         }),
                    Transformation(name='multiply_scalar', args=(HTR_TO_EV,)),
                    Transformation(name='split_array', kwargs={
                        'suffixes': ['up', 'down'],
                        'name': 'eigenvalues'
                    }),
                    Transformation(name='flatten_array')
                ],
                'unpack_dict':
                True
            },
            'kpath': {
                'h5path':
                '/kpts/coordinates',
                'transforms': [
                    AttribTransformation(name='multiply_by_attribute',
                                         attrib_name='reciprocal_cell',
                                         kwargs={'transpose': True}),
                    Transformation(name='calculate_norm', kwargs={'between_neighbours': True}),
                    Transformation(name='cumulative_sum'),
                    AttribTransformation(name='repeat_array_by_attribute', attrib_name='nbands'),
                ]
            },
        },
        'attributes': {
            'group_name': {
                'h5path': f'/{group}',
                'transforms': [
                    Transformation(name='get_name'),
                ],
            },
            'kpoints': {
                'h5path': '/kpts/coordinates',
            },
            'nkpts': {
                'h5path': '/Local/BS/eigenvalues',
                'transforms': [Transformation(name='get_shape'),
                               Transformation(name='index_dataset', args=(1,))]
            },
            'nbands': {
                'h5path': '/Local/BS/eigenvalues',
                'transforms': [Transformation(name='get_shape'),
                               Transformation(name='index_dataset', args=(2,))]
            },
            'atoms_elements': {
                'h5path': '/atoms/atomicNumbers',
                'description': 'Atomic numbers',
                'transforms': [Transformation(name='periodic_elements')]
            },
            'n_types': {
                'h5path':
                '/atoms',
                'description':
                'Number of atom types',
                'transforms':
                [Transformation(name='get_attribute', args=('nTypes',)),
                 Transformation(name='get_first_element')]
            },
            'atoms_position': {
                'h5path': '/atoms/positions',
                'description': 'Atom coordinates per atom',
            },
            'atoms_groups': {
                'h5path': '/atoms/equivAtomsGroup'
            },
            'reciprocal_cell': {
                'h5path': '/cell/reciprocalCell'
            },
            'bravais_matrix': {
                'h5path': '/cell/bravaisMatrix',
                'description': 'Coordinate transformation internal to physical for atoms',
                'transforms': [Transformation(name='multiply_scalar', args=(BOHR_A,))]
            },
            'special_kpoint_indices': {
                'h5path': '/kpts/specialPointIndices',
                'transforms': [Transformation(name='shift_dataset', args=(-1,))]
            },
            'special_kpoint_labels': {
                'h5path': '/kpts/specialPointLabels',
                'transforms': [Transformation(name='convert_to_str')]
            },
            'fermi_energy': {
                'h5path':
                '/general',
                'description':
                'fermi_energy of the system',
                'transforms': [
                    Transformation(name='get_attribute', args=('lastFermiEnergy',)),
                    Transformation(name='get_first_element')
                ]
            },
            'spins': {
                'h5path':
                '/general',
                'description':
                'number of distinct spin directions in the system',
                'transforms':
                [Transformation(name='get_attribute', args=('spins',)),
                 Transformation(name='get_first_element')]
            }
        }
    })

    if simple:
        return recipe

    recipe['datasets']['weights'] = {
        'h5path':
        f'/{group}/BS',
        'transforms': [
            Transformation(name='get_all_child_datasets', kwargs={'ignore': ['eigenvalues', 'kpts']}),
            AttribTransformation(name='add_partial_sums',
                                 attrib_name='atoms_groups',
                                 args=(f'{atom_prefix}{{}}'.format,),
                                 kwargs={'make_set': True}),
            Transformation(name='split_array', kwargs={'suffixes': ['up', 'down']}),
            Transformation(name='flatten_array')
        ],
        'unpack_dict':
        True
    }

    return recipe


def get_fleur_bands_specific_weights(weight_name: str | list[str],
                                     group: Literal['Local', 'jDOS', 'Orbcomp', 'MCD'] = 'Local') -> HDF5Recipe:
    """
    Recipe for bandstructure calculations only retrieving one
    additional weight besides the eigenvalues and kpath

    :param weight_name: key or list of keys of the weight(s) to retrieve
    :param group: optional str (default Local) name of the group from where to take the weights

    :returns: dict of the recipe to retrieve a simple bandstructure
              plus the one specified weight
    """
    recipe = bands_recipe_format(group, simple=True)

    if isinstance(weight_name, str):
        weight_name = [weight_name]

    for name in weight_name:
        if 'MT:' in name and not any(c in name for c in ('s', 'p', 'd', 'f')):
            #We need to get all orbitals and calculate the atom sum
            recipe['datasets'][name] = {
                'h5path':
                f'/{group}/BS',
                'transforms': [
                    Transformation(name='get_all_child_datasets', kwargs={'contains': name}),
                    Transformation(name='sum_over_dict_entries', kwargs={'overwrite_dict': True}),
                    Transformation(name='split_array', kwargs={
                        'suffixes': ['up', 'down'],
                        'name': name
                    }),
                    Transformation(name='flatten_array')
                ],
                'unpack_dict':
                True
            }
        else:
            recipe['datasets'][name] = {
                'h5path':
                f'/{group}/BS/{name}',
                'transforms': [
                    Transformation(name='split_array', kwargs={
                        'suffixes': ['up', 'down'],
                        'name': name
                    }),
                    Transformation(name='flatten_array')
                ],
                'unpack_dict':
                True
            }

    return recipe


#Recipe for bandstructures
FleurBands = bands_recipe_format('Local')
FleurOrbcompBands = bands_recipe_format('Orbcomp')
FleurjDOSBands = bands_recipe_format('jDOS')
FleurMCDBands = bands_recipe_format('MCD')
#Recipe for bandstructures without reading in weights
FleurSimpleBands = bands_recipe_format('Local', simple=True)
