# -*- coding: utf-8 -*-
"""
This module defines commonly used recipes for the HDF5Reader
"""

def dos_recipe_format(group):
    from masci_tools.util.constants import HTR_TO_EV

    return {
        'datasets': {
            'dos': {
                'h5path': f'/{group}/DOS',
                'transforms': [('get_all_child_datasets', 'energyGrid'), ('scale_with_constant', 1.0 / HTR_TO_EV)]
            },
            'energy_grid': {
                'h5path': f'/{group}/DOS/energyGrid',
                'transforms': [('scale_with_constant', HTR_TO_EV)]
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

#DOS Recipes
FleurDOSRecipe = dos_recipe_format('Local')
FleurJDOSRecipe = dos_recipe_format('jDOS')
FleurORBCOMPRecipe = dos_recipe_format('Orbcomp')
FleurMCDRecipe = dos_recipe_format('mcd')