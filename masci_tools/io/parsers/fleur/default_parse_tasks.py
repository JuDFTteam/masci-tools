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
This module contains the dictionary with all defined tasks for the outxml_parser.
The entries in the TASK_DEFINITION dict specify how to parse specific attributes tags.

This needs to be maintained if the specifications do not work for a new schema version
because of changed attribute names for example.

Each entry in the TASK_DEFINITION dict can contain a series of keys, which by default
correspond to the keys in the output dictionary

The following keys are expected in each entry:
    :param parse_type: str, defines which methods to use when extracting the information
    :param path_spec: dict with all the arguments that should be passed to get_tag_xpath
                      or get_attrib_xpath to get the correct path
    :param subdict: str, if present the parsed values are put into this key in the output dictionary
    :param overwrite_last: bool, if True no list is inserted and each entry overwrites the last

For the allAttribs parse_type there are more keys that can appear:
    :param base_value: str, optional. If given the attribute
                       with this name will be inserted into the key from the task_definition
                       all other keys are formatted as {task_key}_{attribute_name}
    :param ignore: list of str, these attributes will be ignored
    :param overwrite: list of str, these attributes will not create a list and overwrite any value
                      that might be there
    :param flat: bool, if False the dict parsed from the tag is inserted as a dict into the correspondin key
                       if True the values will be extracted and put into the output dictionary with the
                       format {task_key}_{attribute_name}

The following keys are configured at the moment:
    - 'fleur_modes' specifies how to identify the type of the calculation (e.g. SOC, magnetic, lda+u)
      this is used to determine, whether additional things should be parsed
    - 'general_inp_info' gets information from the input section of the out.xml like number of symmnetries
    - 'general_out_info' gets information from the section of the out.xml outside iterations, like timing
      basis information, ...
    - All other keys are parsed for each iteration. (total_energy, distances, ...)

"""

__working_out_versions__ = {'0.33'}

TASKS_DEFINITION = {
    'fleur_modes': {
        'jspin': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'jspins'
            }
        },
        'relax': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'l_f'
            }
        },
        'ldau': {
            'parse_type': 'exists',
            'path_spec': {
                'name': 'ldaU',
                'contains': 'species'
            }
        },
        'soc': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'l_soc'
            }
        },
        'noco': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'l_noco'
            }
        },
        'film': {
            'parse_type': 'exists',
            'path_spec': {
                'name': 'filmPos'
            }
        }
    },
    'general_out_info': {
        'creator_name': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'version',
                'not_contains': 'git'
            }
        },
        'creator_target_architecture': {
            'parse_type': 'text',
            'path_spec': {
                'name': 'targetComputerArchitectures'
            }
        },
        'creator_target_structure': {
            'parse_type': 'text',
            'path_spec': {
                'name': 'targetStructureClass'
            }
        },
        'output_file_version': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'fleurOutputVersion'
            }
        },
        'number_of_iterations': {
            'parse_type': 'numberNodes',
            'path_spec': {
                'name': 'iteration'
            }
        },
        'number_of_atoms': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'nat'
            }
        },
        'number_of_atom_types': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'ntype'
            }
        },
        'start_date': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'startDateAndTime'
            },
            'ignore': ['zone'],
            'flat': False,
        },
        'end_date': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'endDateAndTime'
            },
            'ignore': ['zone'],
            'flat': False,
        }
    },
    'general_inp_info': {
        'title': {
            'parse_type': 'text',
            'path_spec': {
                'name': 'comment'
            }
        },
        'kmax': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'Kmax'
            }
        },
        'gmax': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'Gmax'
            }
        },
        'number_of_spin_components': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'jspins'
            }
        },
        'number_of_symmetries': {
            'parse_type': 'numberNodes',
            'path_spec': {
                'name': 'symOp'
            }
        },
        'number_of_species': {
            'parse_type': 'numberNodes',
            'path_spec': {
                'name': 'species'
            }
        }
    },
    'ldau_info': {
        'parsed_ldau': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'ldaU',
                'contains': 'species'
            },
            'subdict': 'ldau_info',
            'flat': False,
        },
        'ldau_species': {
            'parse_type': 'parentAttribs',
            'path_spec': {
                'name': 'ldaU',
                'contains': 'species'
            },
            'subdict': 'ldau_info',
            'flat': False,
        }
    },
    'iteration_number': {
        'number_of_iterations_total': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'overallNumber'
            },
            'overwrite_last': True,
        }
    },
    'total_energy': {
        'energy_hartree': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'totalEnergy'
            }
        },
    },
    'distances': {},
    'total_energy_contributions': {
        'sum_of_eigenvalues': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'sumOfEigenvalues'
            }
        },
        'energy_core_electrons': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'coreElectrons'
            }
        },
        'energy_valence_electrons': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'valenceElectrons'
            }
        },
        'charge_den_xc_den_integral': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'chargeDenXCDenIntegral'
            }
        },
    },
    'ldau_energy_correction': {
        'ldau_energy_correction': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'dftUCorrection'
            },
            'subdict': 'ldau_info'
        },
    },
    'nmmp_distances': {
        'density_matrix_distance': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'distance',
                'contains': 'ldaUDensityMatrixConvergence'
            },
            'subdict': 'ldau_info'
        },
    },
    'fermi_energy': {
        'fermi_energy': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'FermiEnergy'
            },
        }
    },
    'bandgap': {
        'bandgap': {
            'parse_type': 'singleValue',
            'path_spec': {
                'name': 'bandgap'
            },
        }
    },
    'magnetic_moments': {
        'magnetic_moments': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'magneticMoment'
            },
            'base_value': 'moment',
            'ignore': ['atomType']
        }
    },
    'orbital_magnetic_moments': {
        'orbital_magnetic_moments': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'orbMagMoment'
            },
            'base_value': 'moment',
            'ignore': ['atomType']
        }
    },
    'forcetheorem_dmi': {
        'force_dmi': {
            'parse_type': 'allAttribs',
            'path_spec': {
                'name': 'Entry',
                'contains': 'DMI'
            }
        },
        'force_dmi_qs': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'qpoints',
                'contains': 'Forcetheorem_DMI'
            }
        },
        'force_dmi_angles': {
            'parse_type': 'attrib',
            'path_spec': {
                'name': 'Angles',
                'contains': 'Forcetheorem_DMI'
            }
        }
    }
}
