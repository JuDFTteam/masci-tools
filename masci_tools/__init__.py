###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the masci-tools package.                               #
#                                                                             #
# The code is hosted on GitHub at https://github.com/JuDFTteam/masci-tools    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit                                        #
###############################################################################
"""
masci-tools is a collection of tools for materials science.
Mainly for the use with the Fleur (https://flapw.de) and juKKR (https://jukkr.fz-juelich.de) code
developed at the Forschungszentrum Jülich (see <http://judft.de>).

Contains IO and parsers utitlies for these codes and
vis contains wrappers of matplotlib functionality to visualize common material science data.
Plus wrappers of visualisation for aiida-fleur workflow nodes
"""
import logging

__copyright__ = ('Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany. '
                 'All rights reserved.')
__license__ = 'MIT license, see LICENSE.txt file.'
__version__ = '0.13.0'
__authors__ = 'The JuDFT team. Also see AUTHORS.txt file.'

logging.getLogger(__name__).addHandler(logging.NullHandler())


def load_ipython_extension(ipython):
    """
    Load ipython extensions in this package
    """
    from masci_tools.util.ipython import register_formatters

    register_formatters(ipython)
