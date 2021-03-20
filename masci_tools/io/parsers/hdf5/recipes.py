# -*- coding: utf-8 -*-
"""
This module defines commonly used recipes for the HDF5Reader
"""

from masci_tools.util.constants import HTR_TO_EV


def dos_recipe_format(group):

    return {
        'datasets': {
            'dos': {
                'h5path': f'/{group}/DOS',
                'transforms': [('get_all_child_datasets', 'energyGrid'), ('scale_with_constant', 1.0 / HTR_TO_EV)],
                'unpack_dict': True,
            },
            'energy_grid': {
                'h5path': f'/{group}/DOS/energyGrid',
                'transforms': [('scale_with_constant', HTR_TO_EV)]
            }
        },
        'attributes': {
            'fermi_energy': {
                'h5path': '/general',
                'description': 'fermi_energy of the system',
                'transforms': [('get_attribute', 'lastFermiEnergy'), 'get_first_element']
            },
            'spins': {
                'h5path': '/general',
                'description': 'number of distinct spin directions in the system',
                'transforms': [('get_attribute', 'spins'), 'get_first_element']
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
            'h5path': '/Local/BS',
            'transforms': [('get_all_child_datasets', ['eigenvalues', 'kpts'])],
            'unpack_dict': True
        },
        'eigenvalues': {
            'h5path': '/Local/BS/eigenvalues',
            'transforms': [('scale_with_constant', HTR_TO_EV)]
        },
        'kpoints': {
            'h5path':
            'Local/BS/kpts',
            'transforms': [('multiply_by_attribute', 'reciprocal_cell', True, True), ('calculate_norm', True),
                           'cumulative_sum']
        }
    },
    'attributes': {
        'atom_groups': {
            'h5path': '/atoms/equivAtomsGroup'
        },
        'reciprocal_cell': {
            'h5path': 'cell/reciprocalCell',
            'transforms': ['move_to_memory']
        },
        'special_kpoint_indices': {
            'h5path': 'kpts/specialPointIndices'
        },
        'special_kpoint_labels': {
            'h5path': 'kpts/specialPointLabels',
            'transforms': ['convert_to_str']
        },
        'fermi_energy': {
            'h5path': '/general',
            'description': 'fermi_energy of the system',
            'transforms': [('get_attribute', 'lastFermiEnergy'), 'get_first_element']
        },
        'spins': {
            'h5path': '/general',
            'description': 'number of distinct spin directions in the system',
            'transforms': [('get_attribute', 'spins'), 'get_first_element']
        }
    }
}
