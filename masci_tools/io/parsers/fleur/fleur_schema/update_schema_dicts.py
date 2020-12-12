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
Contains utility to update the schema dicts.
"""
try:
    from .inpschema_todict import create_inpschema_dict
    from .outschema_todict import create_outschema_dict
except ImportError:
    #These are here so that the scripts can be used from the commandline
    from masci_tools.io.parsers.fleur.fleur_schema import create_inpschema_dict  # pylint: disable=cyclic-import
    from masci_tools.io.parsers.fleur.fleur_schema import create_outschema_dict  # pylint: disable=cyclic-import
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def update_schema_dicts():
    """
    Reruns the parsing for all fleur schema files present in the version folders
    """
    for root, dirs, files in os.walk(PACKAGE_DIRECTORY):
        for file in files:
            path = os.path.abspath(root)
            if file == 'FleurInputSchema.xsd':
                create_inpschema_dict(path)
            elif file == 'FleurOutputSchema.xsd':
                if not os.path.isfile(os.path.join(path, 'inpschema_dict.py')):
                    create_inpschema_dict(path)
                create_outschema_dict(path)


if __name__ == '__main__':
    update_schema_dicts()
