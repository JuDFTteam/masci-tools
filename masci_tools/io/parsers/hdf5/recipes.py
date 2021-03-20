# -*- coding: utf-8 -*-
"""
This module defines commonly used recipes for the HDF5Reader
"""

from masci_tools.util.constants import HTR_TO_EV, BOHR_A
from masci_tools.io.parsers.hdf5.reader import Transformation, AttribTransformation


def dos_recipe_format(group):

    if group == 'Local':
        atom_prefix = 'MT'
    elif group == 'jDOS':
        atom_prefix = 'jDOS'
    elif group == 'Orbcomp':
        atom_prefix = 'ORBCOMP'
    elif group == 'mcd':
        atom_prefix = 'MCD'
    else:
        raise ValueError(f'Unknown group: {group}')

    return {
        'datasets': {
            'dos': {
                'h5path':
                f'/{group}/DOS',
                'transforms': [
                    Transformation(name='get_all_child_datasets', kwargs={'ignore': 'energyGrid'}),
                    AttribTransformation(name='add_partial_sums',
                                         attrib_name='atom_groups',
                                         args=('{atom_prefix}:{{}}'.format(atom_prefix=atom_prefix).format,)),
                    Transformation(name='scale_with_constant', args=(1.0 / HTR_TO_EV,))
                ],
                'unpack_dict':
                True,
            },
            'energy_grid': {
                'h5path': f'/{group}/DOS/energyGrid',
                'transforms': [Transformation(name='scale_with_constant', args=(HTR_TO_EV,))]
            }
        },
        'attributes': {
            'atom_groups': {
                'h5path': '/atoms/equivAtomsGroup',
                'transforms': [Transformation(name='move_to_memory')]
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
    }


#DOS Recipes
FleurDOS = dos_recipe_format('Local')
FleurJDOS = dos_recipe_format('jDOS')
FleurORBCOMP = dos_recipe_format('Orbcomp')
FleurMCD = dos_recipe_format('mcd')

FleurBands = {
    'datasets': {
        'weights': {
            'h5path':
            '/Local/BS',
            'transforms': [
                Transformation(name='get_all_child_datasets', kwargs={'ignore': ['eigenvalues', 'kpts']}),
                AttribTransformation(name='add_partial_sums', attrib_name='atom_groups', args=('MT:{}'.format,))
            ],
            'unpack_dict':
            True
        },
        'eigenvalues': {
            'h5path': '/Local/BS/eigenvalues',
            'transforms': [Transformation(name='scale_with_constant', args=(HTR_TO_EV,))]
        },
        'kpath': {
            'h5path':
            '/Local/BS/kpts',
            'transforms': [
                AttribTransformation(name='multiply_by_attribute',
                                     attrib_name='reciprocal_cell',
                                     kwargs={
                                         'reverse_order': True,
                                         'by_element': True
                                     }),
                Transformation(name='calculate_norm', kwargs={'between_neighbours': True}),
                Transformation(name='cumulative_sum')
            ]
        },
        'kpoints': {
            'h5path':
            'Local/BS/kpts',
        }
    },
    'attributes': {
        "atoms_elements":{
              "h5path": "/atoms/atomicNumbers",
                "description": "Atomic numbers"
            },
            "atoms_position": {
                "h5path": "/atoms/positions",
                "description": "Atom coordinates per atom",
            },
        'atom_groups': {
            'h5path': '/atoms/equivAtomsGroup',
            'transforms': [Transformation(name='move_to_memory')]
        },
        "bravaisMatrix": {
                "h5path": "/cell/bravaisMatrix",
                "description": "Coordinate transformation internal to physical for atoms",
                "transforms": [Transformation(name='scale_with_constant', args=(BOHR_A,))]
            },
        'reciprocal_cell': {
            'h5path': '/cell/reciprocalCell',
            'transforms': [Transformation(name='move_to_memory')]
        },
        'special_kpoint_indices': {
            'h5path': '/kpts/specialPointIndices'
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
            'transforms':
            [Transformation(name='get_attribute', args=('lastFermiEnergy',)),
             Transformation(name='get_first_element')]
        },
        'spins': {
            'h5path': '/general',
            'description': 'number of distinct spin directions in the system',
            'transforms':
            [Transformation(name='get_attribute', args=('spins',)),
             Transformation(name='get_first_element')]
        }
    }
}
