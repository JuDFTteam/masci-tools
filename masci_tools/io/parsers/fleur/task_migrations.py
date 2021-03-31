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
In this module migration functions for the task definitions are collected
"""
import copy
from masci_tools.util.parse_tasks_decorators import register_migration


@register_migration(base_version='0.33', target_version=['0.31', '0.30', '0.29'])
def migrate_033_to_031(definition_dict):
    """
    Migrate definitions for MaX5 release to MaX4 release

    Changes:
        - LDA+U density matrix distance output did not exist
    """

    new_dict = copy.deepcopy(definition_dict)
    new_dict.pop('nmmp_distances')

    return new_dict


@register_migration(base_version='0.34', target_version='0.33')
def migrate_034_to_033(definition_dict):
    """
    Migrate definitions for MaX5 bugfix release to MaX5 release

    Changes:
        - forcetheorem units attribute did not exist (get from 'sumValenceSingleParticleEnergies')
    """

    new_dict = copy.deepcopy(definition_dict)

    force_units = {
        'parse_type': 'attrib',
        'path_spec': {
            'name': 'units',
            'tag_name': 'sumValenceSingleParticleEnergies'
        }
    }

    new_dict['forcetheorem_mae']['mae_force_units'] = copy.deepcopy(force_units)
    new_dict['forcetheorem_ssdisp']['spst_force_units'] = copy.deepcopy(force_units)
    new_dict['forcetheorem_jij']['jij_force_units'] = copy.deepcopy(force_units)
    new_dict['forcetheorem_dmi']['dmi_force_units'] = copy.deepcopy(force_units)

    return new_dict
